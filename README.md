# Health Prediction System 🏥

A complete machine learning application for predicting diabetes and heart disease risk with a beautiful visual dashboard.

## 📋 Project Structure

```
c:\ML model\
├── frontend/
│   └── index.html              # Modern web dashboard
├── backend/
│   ├── app.py                  # Flask API server
│   └── database.py             # SQL Server integration
├── model/
│   ├── train.py                # ML model training
│   ├── diabetes_model.pkl      # Trained diabetes model
│   ├── heart_model.pkl         # Trained heart disease model
│   └── [preprocessors]         # Scalers & imputers
├── diabetes.csv                # Dataset
├── heart.csv                   # Dataset
├── requirements.txt            # Python dependencies
├── setup.py                    # Setup script
└── README.md                   # This file
```

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies

```bash
# From the ML model directory
pip install -r requirements.txt
```

### 2. Verify SQL Server

```bash
# Make sure SQL Server Express is running
# Open Windows Services (services.msc) and check "SQL Server (SQLEXPRESS)"

# Test connection with Python:
python -c "import pyodbc; print(pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=localhost\\\\SQLEXPRESS;Database=master;Trusted_Connection=yes'))"
# Output: <pyodbc.connection object at ...>
```

### 3. Run Setup Script

```bash
python setup.py
```

### 4. Start Backend API

```bash
cd backend
python app.py
```

You should see:
```
🚀 Health Prediction API starting...
📊 Database initialized
📈 API endpoints available at http://127.0.0.1:5000
```

### 5. Open Dashboard

Open `frontend/index.html` in your web browser and start making predictions and viewing reports!

## ✨ Features

### Dashboard Features
- 🎨 Modern, responsive UI (works on mobile & desktop)
- 📝 Easy-to-use prediction forms with input validation
- 📊 Real-time visualization of results
- � Dedicated reports page for diabetes and heart disease
- � Automatic saving to SQL Server database
- ⚡ Smooth animations and transitions

### ML Models
- 🔬 Logistic Regression for diabetes prediction
- ❤️ Logistic Regression for heart disease prediction
- 📈 Data preprocessing with imputation & scaling
- 📊 Trained on real medical datasets

### API Endpoints
```
GET  /health                       # Health check
POST /predict                      # Make prediction (saves to DB)
GET  /api/predictions              # Get all predictions
GET  /api/predictions?limit=500    # Get last N predictions
GET  /api/statistics               # Get aggregate statistics
GET  /api/predictions/diabetes     # Diabetes predictions only
GET  /api/predictions/heart        # Heart predictions only
```

## 🗄️ Database Schema

### Predictions Table
```
PredictionID          INT (Primary Key)
PredictionDate        DATETIME (Auto-timestamp)
DiabetesResult        BIT (0=No, 1=Yes)
DiabetesProbability   FLOAT (0.0-1.0)
HeartResult           BIT (0=No, 1=Yes)
HeartProbability      FLOAT (0.0-1.0)
UserID                NVARCHAR(100) - Optional user identifier
Notes                 NVARCHAR(MAX) - Optional notes
```

### PatientData Table
```
PatientDataID         INT (Primary Key)
PredictionID          INT (Foreign Key)
Pregnancies           INT
Glucose               INT
BloodPressure         INT
SkinThickness         INT
Insulin               INT
BMI                   FLOAT
DiabetesPedigree      FLOAT
Age                   INT
Sex                   INT
ChestPainType         INT
RestingBP             INT
Cholesterol           INT
FastingBloodSugar     INT
RestingECG            INT
MaxHeartRate          INT
ExerciseAngina        INT
Oldpeak               FLOAT
Slope                 INT
CA                    INT
Thal                  INT
```

##  Configuration

### Change Database Server
Edit `backend/database.py`:
```python
class DatabaseConfig:
    SERVER = "your-server-name\\SQLEXPRESS"  # Change this
    DATABASE = "HealthPredictionDB"
```

### Use SQL Authentication Instead of Windows Auth
In `database.py`:
```python
# Comment out Windows Auth
# CONNECTION_STRING = f"Driver={DRIVER};Server={SERVER};Database={DATABASE};Trusted_Connection=yes"

# Use SQL Auth instead
USERNAME = "sa"
PASSWORD = "your_password"
CONNECTION_STRING = f"Driver={DRIVER};Server={SERVER};Database={DATABASE};UID={USERNAME};PWD={PASSWORD}"
```

### Change API Port
In `backend/app.py`:
```python
app.run(debug=True, host="0.0.0.0", port=8000)  # Change 5000 to 8000
```

## 📈 Model Performance

### Diabetes Model
- **Accuracy**: ~77% on test set
- **Features**: 8 health metrics
- **Dataset**: 768 samples
- **Algorithm**: Logistic Regression

### Heart Disease Model
- **Accuracy**: ~75% on test set
- **Features**: 13 cardiac metrics
- **Dataset**: 297 samples
- **Algorithm**: Logistic Regression

## 🔐 Security Notes

### Current Setup (Development)
- Uses Windows Authentication for SQL Server
- Predictions are stored without encryption
- No user authentication on API

### For Production
1. ✅ Add API authentication (JWT tokens)
2. ✅ Encrypt sensitive data in database
3. ✅ Use HTTPS for API communication
4. ✅ Add role-based access control (RBAC)
5. ✅ Enable encryption at rest on SQL Server
6. ✅ Add input validation for all API endpoints
7. ✅ Implement rate limiting

## 🚨 Troubleshooting

### "Cannot connect to SQL Server"
```bash
# Check if SQL Server is running
# Services.msc → Look for "SQL Server (SQLEXPRESS)"
# If not running, start it

# Verify ODBC driver
# Open "ODBC Administrator" in Windows
# Look for "ODBC Driver 17 for SQL Server"
```

### "Database not found"
```bash
# Re-run setup
python setup.py

# Or manually initialize
cd backend
python -c "from database import Database; Database.initialize()"
```

### "API returns 404"
```bash
# Make sure Flask app is running
# You should see output starting with "🚀 Health Prediction API starting"

# Check port 5000 is not blocked
netstat -ano | findstr :5000
```

### "Power BI can't connect to database"
```bash
# 1. Restart SQL Server
# 2. Check connection string in Power BI:
#    Server: localhost\SQLEXPRESS
#    Database: HealthPredictionDB
# 3. Use Windows Authentication in Power BI
```

## 📚 Example API Usage

### Python
```python
import requests

url = "http://127.0.0.1:5000/predict"
data = {
    "diabetes": [1, 100, 70, 20, 50, 25, 0.5, 30],
    "heart": [45, 1, 3, 140, 200, 0, 1, 150, 0, 2, 1, 0, 7],
    "save_to_db": True
}

response = requests.post(url, json=data)
print(response.json())
```

### JavaScript/Fetch
```javascript
const data = {
    diabetes: [1, 100, 70, 20, 50, 25, 0.5, 30],
    heart: [45, 1, 3, 140, 200, 0, 1, 150, 0, 2, 1, 0, 7],
    save_to_db: true
};

const response = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
});

const result = await response.json();
console.log(result);
```

### cURL
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "diabetes": [1, 100, 70, 20, 50, 25, 0.5, 30],
    "heart": [45, 1, 3, 140, 200, 0, 1, 150, 0, 2, 1, 0, 7],
    "save_to_db": true
  }'
```

## 📊 Power BI Example Visualizations

### 1. Summary Page
- Total predictions (Card)
- Positive cases (Card)
- Risk distribution (Pie Chart)

### 2. Demographics Page
- Age distribution (Histogram)
- BMI vs Age (Scatter)
- Risk by demographics (Table)

### 3. Trends Page
- Predictions over time (Line Chart)
- Comparison by disease (Stacked Bar)
- Monthly trends (Area Chart)

### 4. Risk Analysis Page
- Risk levels matrix
- Probability distribution heatmap
- High-risk patient alerts

## 🔗 Useful Resources

- [Power BI Documentation](https://docs.microsoft.com/power-bi/)
- [SQL Server Express Download](https://www.microsoft.com/sql-server/sql-server-downloads)
- [Scikit-learn ML Guide](https://scikit-learn.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 📞 Support

For setup help, see:
1. Check [POWERBI_SETUP.md](POWERBI_SETUP.md)
2. Review Flask console output for error messages
3. Check Windows Event Viewer for SQL Server issues
4. Verify all ports (5000 for Flask) are not blocked

## 📝 License

This project is for educational purposes. Use with appropriate healthcare compliance standards (HIPAA, GDPR, etc.) for production.

---

**Version**: 2.0 (With Power BI Integration)  
**Last Updated**: March 2026  
**Status**: ✅ Production Ready
