import os
import joblib
import numpy as np
from django.conf import settings
from hospitals.models import Hospital

# === Load models once on module import ===
HOSPITAL_MODEL_PATH = os.path.join(settings.BASE_DIR, 'hospital_prediction_model.sav')
DISEASE_MODEL_PATH = os.path.join(settings.BASE_DIR, 'disease_risk_model.sav')

try:
    hospital_model = joblib.load(HOSPITAL_MODEL_PATH)
except Exception as e:
    hospital_model = None
    print(f"[ERROR] Failed to load hospital prediction model: {e}")

try:
    disease_model = joblib.load(DISEASE_MODEL_PATH)
except Exception as e:
    disease_model = None
    print(f"[ERROR] Failed to load disease risk model: {e}")

# === Predict hospital from data ===
def predict_hospital(data):
    """
    Predict the most suitable hospital based on input features.
    `data` should be a dict or list of features in the same order used for training.
    """
    if hospital_model is None:
        return Hospital.objects.first()

    try:
        input_data = np.array([list(data.values())]) if isinstance(data, dict) else np.array([data])
        prediction = hospital_model.predict(input_data)

        # Example: prediction is hospital ID or index
        hospital_id = int(prediction[0])
        return Hospital.objects.get(id=hospital_id)
    except Exception as e:
        print(f"[ERROR] Hospital prediction failed: {e}")
        return Hospital.objects.first()  # Fallback


# === Assess disease risk from data ===
def assess_disease_risk(data):
    """
    Predict disease risk score from patient data.
    `data` should be a dict or list of features in the same order used for training.
    """
    if disease_model is None:
        return False

    try:
        input_data = np.array([list(data.values())]) if isinstance(data, dict) else np.array([data])
        prediction = disease_model.predict(input_data)
        return prediction[0]  # Could be score or binary class
    except Exception as e:
        print(f"[ERROR] Disease risk prediction failed: {e}")
        return False
