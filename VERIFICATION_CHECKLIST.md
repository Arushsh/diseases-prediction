# Installation & Verification Checklist ✅

Use this checklist to verify your Health Prediction System is working correctly.

## Pre-Installation Checklist

- [ ] **Windows OS** (Windows 10 or later recommended)
- [ ] **Python 3.8+** installed (verify: `python --version`)
- [ ] **Internet connection** (to download packages)
- [ ] **Administrator access** (for SQL Server installation)

## Step 1: Install SQL Server Express

- [ ] Downloaded SQL Server Express from Microsoft
- [ ] Ran installer with default settings
- [ ] **SQL Server (SQLEXPRESS)** appears in Windows Services
- [ ] **ODBC Driver 17 for SQL Server** is installed
  - Verify: Open "ODBC Data Source Administrator"
  - Look for "ODBC Driver 17 for SQL Server"

## Step 2: Install Python Dependencies

- [ ] Opened PowerShell in project folder
- [ ] Ran: `pip install -r requirements.txt`
- [ ] No error messages in console
- [ ] All packages installed successfully:
  - [ ] flask
  - [ ] flask-cors
  - [ ] joblib
  - [ ] scikit-learn
  - [ ] pandas
  - [ ] pyodbc
  - [ ] numpy

## Step 3: Verify ML Models

- [ ] File exists: `model/diabetes_model.pkl`
- [ ] File exists: `model/diabetes_scaler.pkl`
- [ ] File exists: `model/diabetes_imputer.pkl`
- [ ] File exists: `model/heart_model.pkl`
- [ ] File exists: `model/heart_scaler.pkl`
- [ ] File exists: `model/heart_imputer.pkl`

If missing, run:
```bash
cd model
python train.py
```

## Step 4: Initialize Database

- [ ] Ran: `python setup.py`
- [ ] Output shows: `✅ All checks passed!`
- [ ] No error messages
- [ ] Database **HealthPredictionDB** was created
  - Verify in: SQL Server Management Studio → Object Explorer

## Step 5: Verify Database Tables

Open **SQL Server Management Studio** (SSMS):

- [ ] Connect to `localhost\SQLEXPRESS`
- [ ] Navigate to: Databases → HealthPredictionDB → Tables
- [ ] Tables exist:
  - [ ] dbo.Predictions
  - [ ] dbo.PatientData

Verify table structure:
```sql
-- Run in SSMS
USE HealthPredictionDB
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
```

Should show both `Predictions` and `PatientData`

## Step 6: Start API Server

- [ ] Opened new PowerShell window
- [ ] Navigated to: `cd backend`
- [ ] Ran: `python app.py`
- [ ] Output shows:
  - [ ] `🚀 Health Prediction API starting...`
  - [ ] `📊 Database initialized`
  - [ ] `📈 API endpoints available at http://127.0.0.1:5000`

## Step 7: Test API Endpoints

Open browser and test each URL:

- [ ] **Health Check**: http://127.0.0.1:5000/health
  - Expect: `{"status": "API is running", "version": "2.0"}`

- [ ] **Get Statistics**: http://127.0.0.1:5000/api/statistics
  - Expect: `{"total_predictions": 0, "positive_diabetes": 0, ...}`

- [ ] **Get Predictions**: http://127.0.0.1:5000/api/predictions
  - Expect: `{"count": 0, "data": []}`

## Step 8: Test Web Dashboard

- [ ] Opened: `frontend/index.html` in web browser
- [ ] Page loads without errors
- [ ] Form displays correctly with:
  - [ ] Diabetes inputs section
  - [ ] Heart inputs section
  - [ ] "Run Prediction Analysis" button
  - [ ] Database save checkbox

## Step 9: Make a Test Prediction

- [ ] Filled in sample values:
  - **Diabetes**: 1, 100, 70, 20, 50, 25, 0.5, 30
  - **Heart**: 45, 1, 3, 140, 200, 0, 1, 150, 0, 2, 1, 0, 7
- [ ] Ensured "Save to database" is checked
- [ ] Clicked "Run Prediction Analysis"
- [ ] Loading indicator appeared
- [ ] Results displayed with:
  - [ ] Diabetes risk (High/Low)
  - [ ] Diabetes probability (as %)
  - [ ] Heart risk (High/Low)
  - [ ] Heart probability (as %)
  - [ ] Comparison chart
- [ ] No console errors

## Step 10: Verify Data Saved

In SSMS, run:
```sql
USE HealthPredictionDB
SELECT * FROM Predictions
SELECT * FROM PatientData
```

- [ ] Prediction appeared in database
- [ ] DiabetesResult and DiabetesProb values match
- [ ] HeartResult and HeartProb values match
- [ ] Patient data row associated with prediction

## Step 11: Dashboard Appearance

Frontend dashboard should show:

- [ ] Professional gradient background (purple/pink)
- [ ] Navigation bar at top with title
- [ ] Tabbed navigation for Predictions, Diabetes Reports, and Heart Reports
- [ ] Two input cards (Diabetes & Heart)
- [ ] Properly labeled input fields
- [ ] Save to database checkbox
- [ ] Predict button
- [ ] Result cards (after prediction)
- [ ] Comparison chart (after prediction)
- [ ] Responsive layout (works on mobile)

## Step 12: Verify Internal Reports

- [ ] Clicked on "Diabetes Reports" tab
- [ ] Overview Statistics populated correctly
- [ ] Risk Distribution chart rendered
- [ ] Prediction History table shows recent predictions
- [ ] Clicked on "Heart Reports" tab
- [ ] Heart-specific analytics populated correctly
- [ ] No errors when switching between tabs

## Step 13: API Consistency

Run multiple predictions and verify:

- [ ] Each prediction gets a unique ID
- [ ] Timestamps are correct
- [ ] Data integrity maintained
- [ ] No duplicate records

## Troubleshooting Verification

### If SQL Server Connection Fails
- [ ] Check Services.msc - SQL Server running?
- [ ] Try with IP: `Server=127.0.0.1,1433`
- [ ] Verify Windows user has access
- [ ] Check SQL Server error log

### If API Won't Start
- [ ] Port 5000 not in use: `netstat -ano | findstr :5000`
- [ ] Models exist in model/ folder
- [ ] Database initialized successfully
- [ ] Flask and dependencies installed

### If Dashboard Won't Load Data
- [ ] API server running?
- [ ] Database has predictions?
- [ ] CORS enabled? (check `CORS(app)` in app.py)
- [ ] No network blocking?

### If Power BI Can't Connect
- [ ] SQL Server running?
- [ ] Database exists?
- [ ] Windows user has database access?
- [ ] Try with different authentication method?

## Performance Verification

- [ ] Dashboard loads in < 2 seconds
- [ ] Prediction completes in < 3 seconds
- [ ] Database queries complete in < 1 second
- [ ] Power BI loads data in < 5 seconds
- [ ] No memory leaks (resource monitor)

## Security Checklist

- [ ] Using Windows Authentication (no hardcoded passwords)
- [ ] API only listening on localhost (127.0.0.1)
- [ ] CORS enabled for frontend
- [ ] No sensitive data logged to console
- [ ] Database credentials not in source code

## Final Verification

- [ ] All checkboxes above are checked
- [ ] No error messages in any console
- [ ] All API endpoints responding
- [ ] Database functioning correctly
- [ ] Dashboard displays predictions
- [ ] Power BI connects to database
- [ ] System ready for production use ✅

## Next Steps (If All Verified)

1. **Create Power BI Dashboards**
   - Follow [POWERBI_SETUP.md](POWERBI_SETUP.md)
   - Create summary, demographics, trends pages

2. **Gather Real Data**
   - Run predictions with real patient data
   - Build comprehensive dataset for analytics

3. **Deploy to Production**
   - Move to SQL Server (not Express)
   - Add user authentication
   - Implement HTTPS
   - Set up monitoring

4. **Extend Features**
   - Add more ML models
   - Implement patient database
   - Add prediction history
   - Create mobile app

## Support Resources

- **Setup Issues**: See [POWERBI_SETUP.md](POWERBI_SETUP.md)
- **Quick Start**: See [POWERBI_QUICKSTART.md](POWERBI_QUICKSTART.md)
- **General Info**: See [README.md](README.md)
- **SQL Server Help**: https://docs.microsoft.com/sql/
- **Power BI Help**: https://docs.microsoft.com/power-bi/

---

**Status**: Ready for use when all checkboxes are completed ✅

**Date Verified**: [Enter date]  
**Verified By**: [Your name]  
**System Version**: 2.0 (Power BI Integration)
