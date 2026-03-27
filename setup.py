"""
Setup Script for Health Prediction System
This script sets up the database and prepares the system for use.
"""

import sys
import subprocess
import os

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_sql_server():
    """Check if SQL Server is accessible"""
    print_header("Checking SQL Server Connection")
    try:
        import pyodbc
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};Server=localhost\\SQLEXPRESS;Database=master;Trusted_Connection=yes'
        )
        conn.close()
        print("✅ SQL Server is running and accessible")
        return True
    except ImportError:
        print("❌ pyodbc not installed. Install with: pip install pyodbc")
        return False
    except Exception as e:
        print(f"❌ Cannot connect to SQL Server: {e}")
        print("   Make sure SQL Server Express is running")
        print("   Open: Services.msc and start 'SQL Server (SQLEXPRESS)'")
        return False

def initialize_database():
    """Initialize the database"""
    print_header("Initializing Database")
    try:
        os.chdir("backend")
        from database import Database
        if Database.initialize():
            print("✅ Database initialized successfully")
            os.chdir("..")
            return True
        else:
            print("❌ Failed to initialize database")
            os.chdir("..")
            return False
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        os.chdir("..")
        return False

def check_models():
    """Check if ML models exist"""
    print_header("Checking ML Models")
    models_needed = [
        "model/diabetes_model.pkl",
        "model/diabetes_scaler.pkl",
        "model/diabetes_imputer.pkl",
        "model/heart_model.pkl",
        "model/heart_scaler.pkl",
        "model/heart_imputer.pkl"
    ]
    
    all_exist = True
    for model in models_needed:
        if os.path.exists(model):
            print(f"✅ Found: {model}")
        else:
            print(f"❌ Missing: {model}")
            all_exist = False
    
    if not all_exist:
        print("\n⚠️  Some models are missing. Run: python model/train.py")
        return False
    
    return True

def test_api():
    """Test if API can be reached"""
    print_header("Testing API Connection")
    try:
        import requests
        response = requests.get("http://127.0.0.1:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and responding")
            return True
    except:
        print("⚠️  API not running yet. It will start when you run: python backend/app.py")
        return False

def print_next_steps():
    """Print setup completion message and next steps"""
    print_header("Setup Complete! 🎉")
    print("""
Next Steps:

1. START THE BACKEND SERVER:
   cd backend
   python app.py
   
2. OPEN THE DASHBOARD:
   Open frontend/index.html in your web browser
   (or drag it to your browser window)

3. CONNECT POWER BI:
   ✓ Open Power BI Desktop
   ✓ Go to Get Data → SQL Server
   ✓ Server: localhost\\SQLEXPRESS
   ✓ Database: HealthPredictionDB
   ✓ Load the 'Predictions' and 'PatientData' tables

4. MAKE SOME PREDICTIONS:
   Fill in the form and click "Run Prediction Analysis"
   Each prediction is saved to SQL Server for Power BI analytics

5. CREATE POWER BI VISUALIZATIONS:
   See POWERBI_SETUP.md for detailed instructions

Available API Endpoints:
   http://127.0.0.1:5000/health                    - Health check
   http://127.0.0.1:5000/api/predictions           - All predictions (JSON)
   http://127.0.0.1:5000/api/statistics            - Aggregate statistics
   http://127.0.0.1:5000/api/predictions/diabetes  - Diabetes only
   http://127.0.0.1:5000/api/predictions/heart     - Heart only

Database Details:
   Server: localhost\\SQLEXPRESS
   Database: HealthPredictionDB
   Tables: Predictions, PatientData

Need Help?
   Check POWERBI_SETUP.md for troubleshooting

Questions?
   See the documentation in the project root
""")

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     Health Prediction System - Power BI Setup             ║
    ║     ML Models + Dashboard + Analytics                     ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    steps = [
        ("Checking SQL Server", check_sql_server),
        ("Checking ML Models", check_models),
        ("Initializing Database", initialize_database),
    ]
    
    all_passed = True
    for step_name, step_func in steps:
        try:
            if not step_func():
                all_passed = False
                if "Database" not in step_name:
                    continue
        except Exception as e:
            print(f"❌ Error in {step_name}: {e}")
            all_passed = False
    
    # Test API connection (it's okay if this fails, API hasn't started yet)
    try:
        test_api()
    except:
        pass
    
    print_next_steps()
    
    if all_passed:
        print("✅ All checks passed! Ready to go!\n")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
