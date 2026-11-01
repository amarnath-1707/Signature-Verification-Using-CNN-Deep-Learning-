# Signature Verification System Using CNN (Deep Learning)

A deep-learning-based handwritten signature verification system that uses a Convolutional Neural Network (CNN) to classify signature images. The application is designed to distinguish genuine signatures from forged signatures and to handle signatures from users who are not recognized by the trained model.

## Key Features

- CNN-based handwritten signature classification.
- Image preprocessing using grayscale conversion and resizing.
- Image augmentation to improve model generalization.
- Noise reduction and image preparation before prediction.
- Prediction output for a recognized user's signature, such as **Genuine** or **Forgery**.
- **Unknown User** handling for signatures that do not match a supported/recognized user.
- Flask-based web interface for submitting a signature image and viewing the result.

## Model Performance

The project has achieved approximately:

- **Validation accuracy:** 92%
- **F1-score:** 89%

These are project-reported validation results. Actual performance may vary depending on the dataset, train/validation split, image quality, and threshold or decision logic used by the application. Do not interpret validation accuracy as a guarantee of real-world performance.

## Tech Stack

- Python
- TensorFlow / Keras
- CNN (Convolutional Neural Network)
- Flask
- NumPy
- Pandas
- OpenCV
- Pillow
- Scikit-learn
- Matplotlib

## How It Works

1. The user uploads a handwritten signature image through the web interface.
2. The application reads the image and preprocesses it.
3. The image is converted to grayscale and resized to the dimensions expected by the model (the project configuration has used **128 × 128** images).
4. The processed image is passed to the trained CNN model.
5. The application interprets the model output and displays the predicted user/class and signature status.
6. If the signature cannot be associated with a supported user, the application can display **Unknown User**, according to the project's unknown-user handling logic.

## Project Structure

The exact filenames can differ between versions of the project. A typical structure is:

```text
signature-verification/
│
├── app.py                  # Flask application / prediction interface
├── models/
│   └── signature_model.h5  # Trained Keras model 
│
├── signatures/              # Dataset 
│   ├── user_1/
│   │   ├── genuine/
│   │   └── forgery/
│   ├── user_2/
│   │   ├── genuine/
│   │   └── forgery/
│   └── ...
│
├── static/                  # CSS, images, and other static assets
├── templates/               # Flask HTML templates
├── requirements.txt
└── README.md
```

Update the example model filename and folder names above to match your actual project.
## Using the Application

1. Open the web application in your browser.
2. Upload a clear signature image.
3. Submit the image for verification.
4. Review the predicted user and result shown by the application.

## Author

**Amarnath**

---

