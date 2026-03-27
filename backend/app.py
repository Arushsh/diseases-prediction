from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import json
from database import Database
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

@app.route("/")
def index():
    """Serve the dashboard"""
    return app.send_static_file("index.html")

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(os.path.dirname(BASE_DIR), "model")

# Initialize database
Database.initialize()

# Load models and preprocessors
def load_assets(name):
    model = joblib.load(os.path.join(MODEL_DIR, f"{name}_model.pkl"))
    scaler = joblib.load(os.path.join(MODEL_DIR, f"{name}_scaler.pkl"))
    imputer = joblib.load(os.path.join(MODEL_DIR, f"{name}_imputer.pkl"))
    return model, scaler, imputer

diabetes_model, diabetes_scaler, diabetes_imputer = load_assets("diabetes")
heart_model, heart_scaler, heart_imputer = load_assets("heart")
park_model, park_scaler, park_imputer = load_assets("parkinsons")
bc_model, bc_scaler, bc_imputer = load_assets("breast_cancer")

with open(os.path.join(MODEL_DIR, "heart_metadata.json"), "r") as f:
    heart_metadata = json.load(f)

def transform_heart_input(heart_values):
    heart_dict = {
        "age": [heart_values[0]],
        "sex": [1 if int(heart_values[1]) == 1 else 0],
        "cp": [int(heart_values[2])],
        "trestbps": [heart_values[3]],
        "chol": [heart_values[4]],
        "fbs": [int(heart_values[5])],
        "restecg": [int(heart_values[6])],
        "thalch": [heart_values[7]],
        "exang": [int(heart_values[8])],
        "oldpeak": [heart_values[9]],
        "slope": [int(heart_values[10])],
        "ca": [int(heart_values[11])],
        "thal": [int(heart_values[12])]
    }
    df = pd.DataFrame(heart_dict)
    df_encoded = pd.get_dummies(df)
    df_encoded = df_encoded.reindex(columns=heart_metadata["encoded_columns"], fill_value=0)
    return df_encoded.values

@app.route("/api/predict/diabetes", methods=["POST"])
def predict_diabetes():
    data = request.json
    vals = data.get("diabetes")
    inp = np.array(vals).reshape(1, -1)
    inp = diabetes_imputer.transform(inp)
    inp = diabetes_scaler.transform(inp)
    pred = diabetes_model.predict(inp)[0]
    prob = diabetes_model.predict_proba(inp)[0][1]
    if data.get("save_to_db", True):
        Database.insert_prediction(diabetes_result=bool(int(pred)), diabetes_prob=float(prob), diabetes_inputs=vals)
    return jsonify({"result": int(pred), "probability": float(prob)})

@app.route("/api/predict/heart", methods=["POST"])
def predict_heart():
    data = request.json
    vals = data.get("heart")
    h_trans = transform_heart_input(vals)
    inp = heart_imputer.transform(h_trans)
    inp = heart_scaler.transform(inp)
    pred = heart_model.predict(inp)[0]
    prob = heart_model.predict_proba(inp)[0][1]
    if data.get("save_to_db", True):
        Database.insert_prediction(heart_result=bool(int(pred)), heart_prob=float(prob), heart_inputs=vals)
    return jsonify({"result": int(pred), "probability": float(prob)})

@app.route("/api/predict/parkinsons", methods=["POST"])
def predict_parkinsons():
    data = request.json
    vals = data.get("parkinsons")
    inp = np.array(vals).reshape(1, -1)
    inp = park_imputer.transform(inp)
    inp = park_scaler.transform(inp)
    pred = park_model.predict(inp)[0]
    prob = park_model.predict_proba(inp)[0][1]
    if data.get("save_to_db", True):
        Database.insert_prediction(park_result=bool(int(pred)), park_prob=float(prob), park_inputs=vals)
    return jsonify({"result": int(pred), "probability": float(prob)})

@app.route("/api/predict/breast_cancer", methods=["POST"])
def predict_breast_cancer():
    data = request.json
    vals = data.get("breast_cancer")
    inp = np.array(vals).reshape(1, -1)
    inp = bc_imputer.transform(inp)
    inp = bc_scaler.transform(inp)
    pred = bc_model.predict(inp)[0]
    prob = bc_model.predict_proba(inp)[0][1]
    if data.get("save_to_db", True):
        Database.insert_prediction(bc_result=bool(int(pred)), bc_prob=float(prob), bc_inputs=vals)
    return jsonify({"result": int(pred), "probability": float(prob)})

@app.route("/api/statistics", methods=["GET"])
def get_statistics():
    return jsonify(Database.get_statistics())

@app.route("/api/predictions", methods=["GET"])
def get_predictions():
    limit = request.args.get("limit", 100, type=int)
    return jsonify({"data": Database.get_predictions_with_patient_data(limit)})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)