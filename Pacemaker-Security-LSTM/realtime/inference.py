import os
import numpy as np
import pandas as pd
import joblib
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# ------------------------------------------------
# Locate project root directory
# ------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "models", "pacemaker_lstm_model.h5")
scaler_path = os.path.join(BASE_DIR, "scaler.pkl")

# ------------------------------------------------
# Rebuild the same model architecture used in training
# ------------------------------------------------
def build_model():

    model = Sequential()

    model.add(LSTM(100, return_sequences=True, input_shape=(1,9)))
    model.add(Dropout(0.2))

    model.add(LSTM(50))
    model.add(Dropout(0.2))

    model.add(Dense(32, activation="relu"))
    model.add(Dense(4, activation="softmax"))

    return model


# ------------------------------------------------
# Load model weights
# ------------------------------------------------
model = build_model()
model.load_weights(model_path)

# ------------------------------------------------
# Load scaler used during training
# ------------------------------------------------
scaler = joblib.load(scaler_path)

# ------------------------------------------------
# Feature column order
# ------------------------------------------------
columns = [
    "BMI",
    "Smoking",
    "Alcohol",
    "Stroke",
    "Sex",
    "Age_Category",
    "Diabetic",
    "PhysicalActivity",
    "HeartRate"
]

# ------------------------------------------------
# Prediction function
# ------------------------------------------------
def predict(data):

    df = pd.DataFrame([data], columns=columns)

    X = scaler.transform(df)

    X = X.reshape(1,1,X.shape[1])

    prediction = model.predict(X, verbose=0)

    return int(np.argmax(prediction))