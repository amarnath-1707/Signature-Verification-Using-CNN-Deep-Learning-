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
├── modelss/
│   └── signature_model.h5  # Trained Keras model (use your actual filename)
│
├── signatures/              # Dataset (usually not committed to Git)
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

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd signature-verification
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the Application

From the project root directory, run:

```bash
python app.py
```

Open the local URL printed in the terminal (commonly `http://127.0.0.1:5000/`) in your browser.

If your Flask app uses a different entry-point filename or port, use the command and URL configured in your code.

## Using the Application

1. Open the web application in your browser.
2. Upload a clear signature image.
3. Submit the image for verification.
4. Review the predicted user and result shown by the application.

For reliable testing, use images that follow the same general format and preprocessing assumptions as the training data.

## Dataset and Privacy

The signature dataset may contain personal and potentially sensitive biometric information. For that reason:

- Do not upload real people's signatures to a public repository without their explicit permission.
- Do not commit private training data to GitHub.
- Consider adding the dataset directory to `.gitignore`.
- Use synthetic, sample, or permission-cleared images for README screenshots.
- Avoid displaying names, phone numbers, IDs, or other personal information in screenshots.

A suggested `.gitignore` entry:

```gitignore
venv/
__pycache__/
*.pyc
.env
signatures/
*.h5
*.keras
```

Only ignore model files if you do not intend to distribute the trained model. If you want users to run predictions immediately, provide the model through an appropriate, permission-safe download or release process and document where to place it.

## Limitations

- Predictions depend on the quality and representativeness of the training dataset.
- Different pens, scanners, lighting, image sizes, and writing conditions may affect predictions.
- A model's validation score does not establish identity or provide a legally reliable authentication decision.
- Unknown-user detection depends on the implementation's class/threshold logic; a standard closed-set CNN does not automatically recognize every unseen person as unknown.

## Future Improvements

- Evaluate performance on a separate test set containing users and samples not used during training.
- Add confidence scores and a carefully validated unknown-user rejection threshold.
- Report precision, recall, F1-score, and a confusion matrix per class.
- Improve robustness to different scanning and capture conditions.
- Add secure user consent, data retention, and access controls before real-world deployment.

## Author

**Amarnath**

---

If you use this project, please describe the dataset and evaluation setup accurately and do not present it as a production-grade identity or security system without further testing.
