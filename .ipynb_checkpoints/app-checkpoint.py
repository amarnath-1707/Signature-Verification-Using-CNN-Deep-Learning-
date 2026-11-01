from flask import Flask, request, jsonify, render_template, url_for
import os
import json
import numpy as np
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
import cv2

# Constants
IMG_HEIGHT = 128
IMG_WIDTH = 128
UPLOAD_FOLDER = 'uploads'
MODEL_FOLDER = 'models'
LABEL_MAP_FOLDER = 'label_maps'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Flask App Configuration
app = Flask(__name__, template_folder='template', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure Upload Directory Exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#  Load All Trained Models
models = {}
model_files = sorted([f for f in os.listdir(MODEL_FOLDER) if f.endswith('.h5')])
for model_file in model_files:
    model_name = model_file.split('.')[0]
    models[model_name] = load_model(os.path.join(MODEL_FOLDER, model_file))
print(f" Loaded {len(models)} models successfully!")

# Load & Merge All Label Maps
label_map = {}
reverse_label_map = {}

if os.path.exists(LABEL_MAP_FOLDER):
    label_map_files = sorted([f for f in os.listdir(LABEL_MAP_FOLDER) if f.endswith('.json')])

    for label_map_file in label_map_files:
        label_map_path = os.path.join(LABEL_MAP_FOLDER, label_map_file)

        try:
            with open(label_map_path, "r") as file:
                data = json.load(file)
                label_map.update(data)  # Merge into main dictionary

                # Reverse lookup to find user
                for key, class_index in data.items():
                    user_id, label_type = key.split('_')
                    reverse_label_map[class_index] = (int(user_id), label_type.capitalize())

            print(f" Loaded {label_map_file} successfully!")

        except Exception as e:
            print(f" Error loading {label_map_file}: {e}")
else:
    print(f" Error: Directory '{LABEL_MAP_FOLDER}' not found!")

#  Function to Check Allowed File Extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#  Function to Preprocess the Input Image
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not read image from {image_path}")
    
    img = cv2.resize(img, (IMG_HEIGHT, IMG_WIDTH))  # Resize
    img = img / 255.0  # Normalize
    img = img.reshape(1, IMG_HEIGHT, IMG_WIDTH, 1)  # Reshape for Model Input
    return img

#  Compare Signature Against All Models & Return Best Match
def compare_signature(image_path):
    try:
        input_image = preprocess_image(image_path)
        best_prediction = {"user_id": "Unknown", "authenticity": "Unknown", "confidence": 0}

        for model_name, model in models.items():
            pred = model.predict(input_image)
            predicted_class = np.argmax(pred)
            confidence = float(pred[0][predicted_class]) * 100  

            #  Reverse Lookup to Find User & Authenticity
            if predicted_class in reverse_label_map:
                user_id, authenticity = reverse_label_map[predicted_class]
                if confidence > best_prediction["confidence"]:  # Select Best Match
                    best_prediction = {
                        "user_id": int(user_id),
                        "authenticity": authenticity,
                        "confidence": confidence
                    }

        return best_prediction

    except Exception as e:
        print(f" Error during prediction: {e}")
        return {"user_id": "Error", "authenticity": "Error", "confidence": 0}

#  Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            best_result = compare_signature(filepath)  # Get the Best Match
            return jsonify({
                'user': f"User {best_result['user_id']}",
                'result': best_result["authenticity"],
                'accuracy': best_result["confidence"]
            })
        except Exception as e:
            return jsonify({'error': f"Prediction failed: {str(e)}"}), 500

    return jsonify({'error': 'Invalid file type'}), 400

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)





# from flask import Flask, request, jsonify, render_template
# import os
# from werkzeug.utils import secure_filename
# import cv2
# import numpy as np
# from tensorflow.keras.models import load_model
# import json

# # Constants
# IMG_HEIGHT = 128
# IMG_WIDTH = 128
# UPLOAD_FOLDER = 'uploads'
# MODEL_FOLDER = 'models'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# # Flask app configuration
# app = Flask(__name__, template_folder='template', static_folder='static')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Ensure upload directory exists
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# # Load all trained models
# models = {}
# model_files = [f for f in os.listdir(MODEL_FOLDER) if f.endswith('.h5')]
# for model_file in model_files:
#     model_name = model_file.split('.')[0]
#     models[model_name] = load_model(os.path.join(MODEL_FOLDER, model_file))

# print(f"Loaded {len(models)} models successfully!")

# # Generate label map for 150 users
# label_map = {}
# reverse_label_map = {}  # Reverse lookup to get user from class index
# class_index = 0
# for user_id in range(1, 181):  # User IDs from 1 to 150
#     genuine_label = f"{user_id}_genuine"
#     forgery_label = f"{user_id}_forgery"
#     label_map[genuine_label] = class_index
#     label_map[forgery_label] = class_index + 1
#     reverse_label_map[class_index] = (user_id, "Genuine")
#     reverse_label_map[class_index + 1] = (user_id, "Forgery")
#     class_index += 2

# # Save label map for reference
# with open('label_map.json', 'w') as file:
#     json.dump(label_map, file)

# # Function to check allowed file extensions
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # Preprocess the input image
# def preprocess_image(image_path):
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if img is None:
#         raise ValueError(f"Could not read image from {image_path}")
#     img = cv2.resize(img, (IMG_HEIGHT, IMG_WIDTH))  # Resize
#     img = img / 255.0  # Normalize
#     img = img.reshape(1, IMG_HEIGHT, IMG_WIDTH, 1)  # Reshape for model input
#     return img

# # Function to compare signature with all models
# def compare_signature(image_path):
#     try:
#         input_image = preprocess_image(image_path)
#         best_prediction = {"user_id": "Unknown", "authenticity": "Unknown", "confidence": 0}
#         all_predictions = {}

#         for model_name, model in models.items():
#             pred = model.predict(input_image)
#             predicted_class = np.argmax(pred)
#             confidence = float(pred[0][predicted_class]) * 100

#             if predicted_class in reverse_label_map:
#                 user_id, authenticity = reverse_label_map[predicted_class]
#                 all_predictions[model_name] = {
#                     "user_id": user_id,
#                     "authenticity": authenticity,
#                     "confidence": confidence
#                 }
#                 if confidence > best_prediction["confidence"]:
#                     best_prediction = all_predictions[model_name]

#         return best_prediction, all_predictions

#     except Exception as e:
#         print(f"Error during prediction: {e}")
#         return {"user_id": "Error", "authenticity": "Error", "confidence": 0}, {}



# # Flask routes
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/verify', methods=['POST'])
# def verify():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400

#     file = request.files['file']

#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)

#         try:
#             best_result, all_results = compare_signature(filepath)
#             return jsonify({
#                 'result': best_result["authenticity"],
#                 'user': f"User {best_result['user_id']}",
#                 'accuracy': best_result["confidence"],
#                 'all_predictions': all_results
#             })
#         except Exception as e:
#             return jsonify({'error': f"Prediction failed: {str(e)}"}), 500

#     return jsonify({'error': 'Invalid file type'}), 400

# # Run Flask app
# if __name__ == '__main__':
#     app.run(debug=True)
