import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import json
import os

def train_and_save(df, target_col, model_name, drop_cols=None):
    print(f"--- Training {model_name} ---")
    if drop_cols:
        df = df.drop(drop_cols, axis=1, errors='ignore')
    
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    # Simple preprocessing for numeric data
    imputer = SimpleImputer(strategy="mean")
    scaler = StandardScaler()
    
    X_processed = imputer.fit_transform(X)
    X_processed = scaler.fit_transform(X_processed)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.2, random_state=42
    )
    
    model = LogisticRegression(max_iter=2000)
    model.fit(X_train, y_train)
    
    joblib.dump(model, f"{model_name}_model.pkl")
    joblib.dump(scaler, f"{model_name}_scaler.pkl")
    joblib.dump(imputer, f"{model_name}_imputer.pkl")
    print(f"✅ {model_name} trained and saved.")

# 1. Diabetes
df_diabetes = pd.read_csv("../diabetes.csv")
train_and_save(df_diabetes, "Outcome", "diabetes")

# 2. Heart (Special handling for encoding)
df_heart = pd.read_csv("../heart.csv")
if "id" in df_heart.columns: df_heart = df_heart.drop("id", axis=1)
if "dataset" in df_heart.columns: df_heart = df_heart.drop("dataset", axis=1)

y_h = df_heart["num"].apply(lambda x: 1 if x > 0 else 0) if "num" in df_heart.columns else df_heart["target"]
X_h = df_heart.drop("num", axis=1, errors='ignore').drop("target", axis=1, errors='ignore')

categorical_cols = X_h.select_dtypes(include=['object']).columns.tolist()
X_h_encoded = pd.get_dummies(X_h)
encoded_columns = X_h_encoded.columns.tolist()

imputer_h = SimpleImputer(strategy="mean")
scaler_h = StandardScaler()
X_h_proc = imputer_h.fit_transform(X_h_encoded)
X_h_proc = scaler_h.fit_transform(X_h_proc)

X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(X_h_proc, y_h, test_size=0.2, random_state=42)
model_h = LogisticRegression(max_iter=2000)
model_h.fit(X_train_h, y_train_h)

joblib.dump(model_h, "heart_model.pkl")
joblib.dump(scaler_h, "heart_scaler.pkl")
joblib.dump(imputer_h, "heart_imputer.pkl")
with open("heart_metadata.json", "w") as f:
    json.dump({"encoded_columns": encoded_columns}, f)
print("✅ Heart model trained and saved.")

# 3. Parkinson's (New)
if os.path.exists("../parkinsons.csv"):
    df_p = pd.read_csv("../parkinsons.csv")
    train_and_save(df_p, "status", "parkinsons")

# 4. Breast Cancer (New)
if os.path.exists("../breast_cancer.csv"):
    df_bc = pd.read_csv("../breast_cancer.csv")
    train_and_save(df_bc, "diagnosis", "breast_cancer")

print("\n🚀 All models trained and saved successfully!")