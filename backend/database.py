"""
Database configuration and models for SQL Server
"""
import pyodbc
import os
from datetime import datetime
import json

# SQL Server Configuration
class DatabaseConfig:
    """Configure SQL Server connection"""
    DRIVER = "ODBC Driver 17 for SQL Server"
    SERVER = "localhost\\SQLEXPRESS"  # or your server name
    DATABASE = "HealthPredictionDB"
    
    # Option 1: Windows Authentication (with SSL disabled)
    CONNECTION_STRING = f"Driver={DRIVER};Server={SERVER};Database={DATABASE};Trusted_Connection=yes;Encrypt=no"

class Database:
    """Handles all database operations"""
    
    @staticmethod
    def connect():
        """Create database connection"""
        try:
            conn = pyodbc.connect(DatabaseConfig.CONNECTION_STRING)
            return conn
        except pyodbc.Error as e:
            print(f"Database Connection Error: {e}")
            return None
    
    @staticmethod
    def initialize():
        """Create database and tables if they don't exist"""
        try:
            # Connect to master to create database (with autocommit)
            master_conn = pyodbc.connect(
                f"Driver={DatabaseConfig.DRIVER};Server={DatabaseConfig.SERVER};Database=master;Trusted_Connection=yes;Encrypt=no"
            )
            master_conn.autocommit = True
            master_cursor = master_conn.cursor()
            
            # Create database
            try:
                master_cursor.execute(f"CREATE DATABASE [{DatabaseConfig.DATABASE}]")
                print(f"✅ Created database {DatabaseConfig.DATABASE}")
            except pyodbc.Error as db_error:
                if "already exists" in str(db_error):
                    print(f"✅ Database {DatabaseConfig.DATABASE} already exists")
                else:
                    raise
            master_cursor.close()
            master_conn.close()
            
            # Connect to the new database and create tables
            conn = Database.connect()
            cursor = conn.cursor()
            
            # Create Predictions table
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Predictions')
                BEGIN
                    CREATE TABLE Predictions (
                        PredictionID INT PRIMARY KEY IDENTITY(1,1),
                        PredictionDate DATETIME DEFAULT GETDATE(),
                        DiabetesResult BIT NULL,
                        DiabetesProbability FLOAT NULL,
                        HeartResult BIT NULL,
                        HeartProbability FLOAT NULL,
                        ParkinsonsResult BIT NULL,
                        ParkinsonsProbability FLOAT NULL,
                        BreastCancerResult BIT NULL,
                        BreastCancerProbability FLOAT NULL,
                        UserID NVARCHAR(100),
                        Notes NVARCHAR(MAX)
                    )
                END
                ELSE
                BEGIN
                    -- Add new columns if they don't exist
                    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Predictions') AND name = 'ParkinsonsResult')
                    BEGIN
                        ALTER TABLE Predictions ADD ParkinsonsResult BIT NULL;
                        ALTER TABLE Predictions ADD ParkinsonsProbability FLOAT NULL;
                        ALTER TABLE Predictions ADD BreastCancerResult BIT NULL;
                        ALTER TABLE Predictions ADD BreastCancerProbability FLOAT NULL;
                    END
                END
            """)
            
            # Create PatientData table
            # Adding columns for Parkinson's and Breast Cancer features
            # This is a bit messy but works for a flat structure
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'PatientData')
                BEGIN
                    CREATE TABLE PatientData (
                        PatientDataID INT PRIMARY KEY IDENTITY(1,1),
                        PredictionID INT NOT NULL,
                        Pregnancies INT, Glucose INT, BloodPressure INT, SkinThickness INT, Insulin INT, BMI FLOAT, DiabetesPedigree FLOAT, Age INT,
                        Sex INT, ChestPainType INT, RestingBP INT, Cholesterol INT, FastingBloodSugar INT, RestingECG INT, MaxHeartRate INT, ExerciseAngina INT, Oldpeak FLOAT, Slope INT, CA INT, Thal INT,
                        Park_AvgF0 FLOAT, Park_Jitter FLOAT, Park_Shimmer FLOAT, Park_NHR FLOAT, Park_HNR FLOAT, Park_RPDE FLOAT, Park_DFA FLOAT, Park_Spread1 FLOAT,
                        BC_Radius FLOAT, BC_Texture FLOAT, BC_Perimeter FLOAT, BC_Area FLOAT, BC_Smoothness FLOAT, BC_Compactness FLOAT, BC_Concavity FLOAT, BC_ConcavePoints FLOAT, BC_Symmetry FLOAT, BC_FractalDim FLOAT,
                        FOREIGN KEY (PredictionID) REFERENCES Predictions(PredictionID)
                    )
                END
                ELSE
                BEGIN
                    -- Add new columns to PatientData if they don't exist
                    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('PatientData') AND name = 'Park_AvgF0')
                    BEGIN
                        ALTER TABLE PatientData ADD Park_AvgF0 FLOAT, Park_Jitter FLOAT, Park_Shimmer FLOAT, Park_NHR FLOAT, Park_HNR FLOAT, Park_RPDE FLOAT, Park_DFA FLOAT, Park_Spread1 FLOAT;
                        ALTER TABLE PatientData ADD BC_Radius FLOAT, BC_Texture FLOAT, BC_Perimeter FLOAT, BC_Area FLOAT, BC_Smoothness FLOAT, BC_Compactness FLOAT, BC_Concavity FLOAT, BC_ConcavePoints FLOAT, BC_Symmetry FLOAT, BC_FractalDim FLOAT;
                    END
                END
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Database initialized successfully!")
            return True
        except pyodbc.Error as e:
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
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (diabetes_result, diabetes_prob, heart_result, heart_prob, 
                  park_result, park_prob, bc_result, bc_prob, user_id, notes))
            
            cursor.execute("SELECT @@IDENTITY")
            prediction_id = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO PatientData (PredictionID, Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigree, Age,
                                        Sex, ChestPainType, RestingBP, Cholesterol, FastingBloodSugar, RestingECG, MaxHeartRate, ExerciseAngina, Oldpeak, Slope, CA, Thal,
                                        Park_AvgF0, Park_Jitter, Park_Shimmer, Park_NHR, Park_HNR, Park_RPDE, Park_DFA, Park_Spread1,
                                        BC_Radius, BC_Texture, BC_Perimeter, BC_Area, BC_Smoothness, BC_Compactness, BC_Concavity, BC_ConcavePoints, BC_Symmetry, BC_FractalDim)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        except pyodbc.Error as e:
            print(f"Insert Prediction Error: {e}")
            return None

    @staticmethod
    def get_all_predictions(limit=1000):
        try:
            conn = Database.connect()
            if not conn: return []
            cursor = conn.cursor()
            cursor.execute(f"SELECT TOP {limit} * FROM Predictions ORDER BY PredictionDate DESC")
            columns = [description[0] for description in cursor.description]
            predictions = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.close(); conn.close()
            return predictions
        except pyodbc.Error as e:
            print(f"Get Predictions Error: {e}"); return []

    @staticmethod
    def get_predictions_with_patient_data(limit=1000):
        try:
            conn = Database.connect()
            if not conn: return []
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT TOP {limit} 
                    p.*, pd.Age, pd.BMI, pd.Glucose, pd.BloodPressure, pd.Cholesterol, pd.MaxHeartRate
                FROM Predictions p
                LEFT JOIN PatientData pd ON p.PredictionID = pd.PredictionID
                ORDER BY p.PredictionDate DESC
            """)
            columns = [description[0] for description in cursor.description]
            predictions = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.close(); conn.close()
            return predictions
        except pyodbc.Error as e:
            print(f"Get Predictions with Patient Data Error: {e}"); return []

    @staticmethod
    def get_statistics():
        try:
            conn = Database.connect()
            if not conn: return {}
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as Total,
                    SUM(CASE WHEN DiabetesResult = 1 THEN 1 ELSE 0 END),
                    SUM(CASE WHEN HeartResult = 1 THEN 1 ELSE 0 END),
                    SUM(CASE WHEN ParkinsonsResult = 1 THEN 1 ELSE 0 END),
                    SUM(CASE WHEN BreastCancerResult = 1 THEN 1 ELSE 0 END),
                    AVG(DiabetesProbability),
                    AVG(HeartProbability),
                    AVG(ParkinsonsProbability),
                    AVG(BreastCancerProbability)
                FROM Predictions
            """)
            row = cursor.fetchone()
            stats = {
                "total_predictions": row[0] or 0,
                "positive_diabetes": row[1] or 0,
                "positive_heart": row[2] or 0,
                "positive_parkinsons": row[3] or 0,
                "positive_breast_cancer": row[4] or 0,
                "avg_diabetes_probability": float(row[5]) if row[5] else 0,
                "avg_heart_probability": float(row[6]) if row[6] else 0,
                "avg_parkinsons_probability": float(row[7]) if row[7] else 0,
                "avg_breast_cancer_probability": float(row[8]) if row[8] else 0
            }
            cursor.close(); conn.close()
            return stats
        except pyodbc.Error as e:
            print(f"Get Statistics Error: {e}"); return {}
