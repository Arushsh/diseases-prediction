"""
Database configuration and models for PostgreSQL (Cloud-Ready)
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path)

# Database Configuration
class DatabaseConfig:
    """Configure PostgreSQL connection"""
    # Use DATABASE_URL from environment (provided by Render)
    # Fallback to local postgres if needed
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/health_prediction_db")

class Database:
    """Handles all database operations using PostgreSQL"""
    
    @staticmethod
    def connect():
        """Create database connection"""
        try:
            conn = psycopg2.connect(DatabaseConfig.DATABASE_URL)
            return conn
        except Exception as e:
            print(f"Database Connection Error: {e}")
            return None
    
    @staticmethod
    def initialize():
        """Create tables if they don't exist"""
        try:
            conn = Database.connect()
            if not conn:
                print("⚠️ Could not connect to database for initialization. Ensure DATABASE_URL is correct.")
                return False
                
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Create Predictions table
            # PostgreSQL uses SERIAL for auto-increment and BOOLEAN for bit
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Predictions (
                    PredictionID SERIAL PRIMARY KEY,
                    PredictionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    DiabetesResult BOOLEAN NULL,
                    DiabetesProbability FLOAT NULL,
                    HeartResult BOOLEAN NULL,
                    HeartProbability FLOAT NULL,
                    ParkinsonsResult BOOLEAN NULL,
                    ParkinsonsProbability FLOAT NULL,
                    BreastCancerResult BOOLEAN NULL,
                    BreastCancerProbability FLOAT NULL,
                    UserID VARCHAR(100),
                    Notes TEXT
                )
            """)
            
            # Create PatientData table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS PatientData (
                    PatientDataID SERIAL PRIMARY KEY,
                    PredictionID INT NOT NULL REFERENCES Predictions(PredictionID),
                    Pregnancies INT, Glucose INT, BloodPressure INT, SkinThickness INT, Insulin INT, BMI FLOAT, DiabetesPedigree FLOAT, Age INT,
                    Sex INT, ChestPainType INT, RestingBP INT, Cholesterol INT, FastingBloodSugar INT, RestingECG INT, MaxHeartRate INT, ExerciseAngina INT, Oldpeak FLOAT, Slope INT, CA INT, Thal INT,
                    Park_AvgF0 FLOAT, Park_Jitter FLOAT, Park_Shimmer FLOAT, Park_NHR FLOAT, Park_HNR FLOAT, Park_RPDE FLOAT, Park_DFA FLOAT, Park_Spread1 FLOAT,
                    BC_Radius FLOAT, BC_Texture FLOAT, BC_Perimeter FLOAT, BC_Area FLOAT, BC_Smoothness FLOAT, BC_Compactness FLOAT, BC_Concavity FLOAT, BC_ConcavePoints FLOAT, BC_Symmetry FLOAT, BC_FractalDim FLOAT
                )
            """)
            
            cursor.close()
            conn.close()
            print("✅ Database initialized successfully!")
            return True
        except Exception as e:
            print(f"Database Initialization Error: {e}")
            return False

    @staticmethod
    def insert_prediction(diabetes_result=None, diabetes_prob=None, heart_result=None, heart_prob=None,
                         park_result=None, park_prob=None, bc_result=None, bc_prob=None,
                         diabetes_inputs=None, heart_inputs=None, park_inputs=None, bc_inputs=None,
                         user_id=None, notes=None):
        """Insert a prediction record"""
        try:
            conn = Database.connect()
            if not conn: return None
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO Predictions (DiabetesResult, DiabetesProbability, 
                                        HeartResult, HeartProbability, 
                                        ParkinsonsResult, ParkinsonsProbability,
                                        BreastCancerResult, BreastCancerProbability,
                                        UserID, Notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING PredictionID
            """, (diabetes_result, diabetes_prob, heart_result, heart_prob, 
                  park_result, park_prob, bc_result, bc_prob, user_id, notes))
            
            prediction_id = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO PatientData (PredictionID, Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigree, Age,
                                        Sex, ChestPainType, RestingBP, Cholesterol, FastingBloodSugar, RestingECG, MaxHeartRate, ExerciseAngina, Oldpeak, Slope, CA, Thal,
                                        Park_AvgF0, Park_Jitter, Park_Shimmer, Park_NHR, Park_HNR, Park_RPDE, Park_DFA, Park_Spread1,
                                        BC_Radius, BC_Texture, BC_Perimeter, BC_Area, BC_Smoothness, BC_Compactness, BC_Concavity, BC_ConcavePoints, BC_Symmetry, BC_FractalDim)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                prediction_id,
                diabetes_inputs[0] if diabetes_inputs else None, diabetes_inputs[1] if diabetes_inputs else None, diabetes_inputs[2] if diabetes_inputs else None,
                diabetes_inputs[3] if diabetes_inputs else None, diabetes_inputs[4] if diabetes_inputs else None, diabetes_inputs[5] if diabetes_inputs else None,
                diabetes_inputs[6] if diabetes_inputs else None, diabetes_inputs[7] if diabetes_inputs else (heart_inputs[0] if heart_inputs else (park_inputs[8] if park_inputs else None)),
                heart_inputs[1] if heart_inputs else None, heart_inputs[2] if heart_inputs else None, heart_inputs[3] if heart_inputs else None,
                heart_inputs[4] if heart_inputs else None, heart_inputs[5] if heart_inputs else None, heart_inputs[6] if heart_inputs else None,
                heart_inputs[7] if heart_inputs else None, heart_inputs[8] if heart_inputs else None, heart_inputs[9] if heart_inputs else None,
                heart_inputs[10] if heart_inputs else None, heart_inputs[11] if heart_inputs else None, heart_inputs[12] if heart_inputs else None,
                park_inputs[0] if park_inputs else None, park_inputs[1] if park_inputs else None, park_inputs[2] if park_inputs else None,
                park_inputs[3] if park_inputs else None, park_inputs[4] if park_inputs else None, park_inputs[5] if park_inputs else None,
                park_inputs[6] if park_inputs else None, park_inputs[7] if park_inputs else None,
                bc_inputs[0] if bc_inputs else None, bc_inputs[1] if bc_inputs else None, bc_inputs[2] if bc_inputs else None,
                bc_inputs[3] if bc_inputs else None, bc_inputs[4] if bc_inputs else None, bc_inputs[5] if bc_inputs else None,
                bc_inputs[6] if bc_inputs else None, bc_inputs[7] if bc_inputs else None, bc_inputs[8] if bc_inputs else None, bc_inputs[9] if bc_inputs else None
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            return prediction_id
        except Exception as e:
            print(f"Insert Prediction Error: {e}")
            return None

    @staticmethod
    def get_predictions_with_patient_data(limit=1000):
        try:
            conn = Database.connect()
            if not conn: return []
            # Use RealDictCursor for compatibility with existing JSON response expectations
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT 
                    p.*, pd.Age, pd.BMI, pd.Glucose, pd.BloodPressure, pd.Cholesterol, pd.MaxHeartRate
                FROM Predictions p
                LEFT JOIN PatientData pd ON p.PredictionID = pd.PredictionID
                ORDER BY p.PredictionDate DESC
                LIMIT %s
            """, (limit,))
            predictions = cursor.fetchall()
            
            # Convert datetime to ISO string for JSON serialization
            for row in predictions:
                if row.get('predictiondate'):
                    row['predictiondate'] = row['predictiondate'].isoformat()
                elif row.get('PredictionDate'):
                    row['PredictionDate'] = row['PredictionDate'].isoformat()
                    
            cursor.close(); conn.close()
            return predictions
        except Exception as e:
            print(f"Get Predictions Error: {e}"); return []

    @staticmethod
    def get_statistics():
        try:
            conn = Database.connect()
            if not conn: return {}
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_predictions,
                    SUM(CASE WHEN DiabetesResult = TRUE THEN 1 ELSE 0 END) as positive_diabetes,
                    SUM(CASE WHEN HeartResult = TRUE THEN 1 ELSE 0 END) as positive_heart,
                    SUM(CASE WHEN ParkinsonsResult = TRUE THEN 1 ELSE 0 END) as positive_parkinsons,
                    SUM(CASE WHEN BreastCancerResult = TRUE THEN 1 ELSE 0 END) as positive_breast_cancer,
                    AVG(DiabetesProbability) as avg_diabetes_probability,
                    AVG(HeartProbability) as avg_heart_probability,
                    AVG(ParkinsonsProbability) as avg_parkinsons_probability,
                    AVG(BreastCancerProbability) as avg_breast_cancer_probability
                FROM Predictions
            """)
            stats = cursor.fetchone()
            
            # Convert decimal to float for JSON serialization if needed
            for key in stats:
                if stats[key] is None: stats[key] = 0
                elif not isinstance(stats[key], (int, float)):
                    stats[key] = float(stats[key])
                    
            cursor.close(); conn.close()
            return stats
        except Exception as e:
            print(f"Get Statistics Error: {e}"); return {}
