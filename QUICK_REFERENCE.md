# Quick Reference Guide ⚡

A complete one-page reference for all commands and steps.

## Installation (One-Time)

```powershell
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Initialize database
python setup.py

# 3. Train models (if missing)
cd model
python train.py
cd ..
```

## Daily Startup (3 steps)

```powershell
# 1. Start API server
cd backend
python app.py
# Leave this running! You'll see "Running on http://127.0.0.1:5000 Press CTRL+C to quit"

# 2. Open dashboard
# Open: frontend/index.html in web browser

# 3. (Optional) Open Power BI Desktop
# Connect to: localhost\SQLEXPRESS / HealthPredictionDB
```

## Folder Navigation

```powershell
# Terminal shortcuts
cd backend        # Go to API (Flask)
cd model          # Go to ML models
cd ..             # Go up one level
dir               # List files (Windows)
ls                # List files (Unix)
```

## API Endpoints (Use in Browser or Power BI)

| Command | URL | Purpose |
|---------|-----|---------|
| Health Check | `http://127.0.0.1:5000/health` | Is server running? |
| Get All Data | `http://127.0.0.1:5000/api/predictions` | All predictions (for Power BI) |
| Get Stats | `http://127.0.0.1:5000/api/statistics` | Summary statistics |
| Diabetes Only | `http://127.0.0.1:5000/api/predictions/diabetes` | Diabetes predictions |
| Heart Only | `http://127.0.0.1:5000/api/predictions/heart` | Heart predictions |

## Test Prediction Values

Copy and paste these to test:

**Diabetes Inputs**:
```
1, 100, 70, 20, 50, 25, 0.5, 30
```

**Heart Inputs**:
```
45, 1, 3, 140, 200, 0, 1, 150, 0, 2, 1, 0, 7
```

## Database Queries (SQL Server Management Studio)

```sql
-- Check database exists
SELECT * FROM sys.databases WHERE name = 'HealthPredictionDB'

-- View all predictions
USE HealthPredictionDB
SELECT * FROM Predictions

-- View patient data
SELECT * FROM PatientData

-- Count predictions
SELECT COUNT(*) as Total FROM Predictions

-- High-risk cases
SELECT * FROM Predictions 
WHERE DiabetesResult = 1 OR HeartResult = 1

-- Statistics
SELECT 
    COUNT(*) as Total,
    SUM(CASE WHEN DiabetesResult = 1 THEN 1 ELSE 0 END) as DiabetesRisk,
    SUM(CASE WHEN HeartResult = 1 THEN 1 ELSE 0 END) as HeartRisk
FROM Predictions
```

## Common Problems & Fixes

| Problem | Command to Check | Fix |
|---------|------------------|-----|
| API won't start | `python app.py` | Check port 5000 free: `netstat -ano \| findstr :5000` |
| DB not found | `python setup.py` | Re-run setup, check SQL Server running |
| Models missing | `dir model\*.pkl` | Run: `cd model && python train.py` |
| Can't connect SQL Server | `sqlcmd -S localhost\SQLEXPRESS` | Check Services: `services.msc` |
| Power BI error | Check connection string | Server: `localhost\SQLEXPRESS` Database: `HealthPredictionDB` |

## Environment Variables (Optional)

```powershell
# To set environment variables (Windows PowerShell):
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"

# To persist them:
[Environment]::SetEnvironmentVariable("FLASK_ENV", "development", "User")
```

## File Locations

| File | Purpose | Location |
|------|---------|----------|
| Dashboard | Web UI | `frontend/index.html` |
| API Server | Backend | `backend/app.py` |
| Database | Data storage | SQL Server on `localhost\SQLEXPRESS` |
| Models | ML predictions | `model/*.pkl` |
| Datasets | Training data | `diabetes.csv`, `heart.csv` |

## Python Version Check

```powershell
# Check Python version
python --version

# Should be 3.8 or higher
# If not, install from: https://www.python.org/downloads/

# Verify installed packages
pip list
```

## Backup & Restore

```powershell
# Backup database (in SQL Server Management Studio)
# Right-click HealthPredictionDB → Tasks → Back Up

# Export data as CSV (in Power BI)
# Right-click table → Export data → Choose format

# Save models
# Backup the model/ folder with .pkl files
```

## Performance Optimization

```powershell
# Clear old predictions (SQL Server)
USE HealthPredictionDB
DELETE FROM Predictions WHERE PredictionDate < DATEADD(day, -90, GETDATE())

# Add index for faster queries
CREATE INDEX idx_date ON Predictions(PredictionDate)

# Check database size
EXEC sp_spaceused

# Find slow queries
SET STATISTICS IO ON
-- ... run query
SET STATISTICS IO OFF
```

## Port Usage

| Port | Service | Command to Check |
|------|---------|------------------|
| 5000 | Flask API | `netstat -ano \| findstr :5000` |
| 1433 | SQL Server | `netstat -ano \| findstr :1433` |
| 2433 | SQL Server Named Pipe | N/A |

## Useful Windows Commands

```powershell
# Check running services
Get-Service | Select-String -Pattern "SQL Server"

# Stop/Start SQL Server
Stop-Service -Name "MSSQL`$SQLEXPRESS"
Start-Service -Name "MSSQL`$SQLEXPRESS"

# View processes
Get-Process | Select-String -Pattern "python"

# Kill process on port 5000
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

## Git Commands (if using version control)

```powershell
# Initialize git (one-time)
git init

# Ignore large files
echo "*.pkl" >> .gitignore
echo "__pycache__/" >> .gitignore

# Commit changes
git add .
git commit -m "Update Power BI integration"

# Check status
git status
```

## Docker Commands (Optional - For Deployment)

```bash
# Build Docker image
docker build -t health-predictor .

# Run container
docker run -p 5000:5000 health-predictor

# Check logs
docker logs <container_id>
```

## Documentation Navigation

| Document | Purpose | When to Read |
|-----------|---------|--------------|
| [README.md](README.md) | Project overview | First time setup |
| [POWERBI_QUICKSTART.md](POWERBI_QUICKSTART.md) | Fast setup (15 min) | Getting Power BI running |
| [POWERBI_SETUP.md](POWERBI_SETUP.md) | Detailed Power BI | Creating dashboards |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Technical details | Understanding system |
| [VERIFICATION_CHECKLIST.md](VERIFICATION_CHECKLIST.md) | Testing | Verifying installation |
| [Quick Reference](Quick_Reference.md) | Commands | Daily use (this file) |

## Browser Shortcuts

```
Ctrl+Shift+I     -> Open Developer Tools
F5               -> Refresh page
Ctrl+Shift+Delete-> Clear cache
F12              -> Developer mode
```

## Important Paths

```
C:\ML model\                          # Project root
C:\ML model\frontend\index.html       # Dashboard
C:\ML model\backend\app.py            # API
C:\ML model\backend\database.py       # DB Layer
C:\ML model\model\*.pkl               # Models
localhost\SQLEXPRESS                  # SQL Server
HealthPredictionDB                    # Database name
http://127.0.0.1:5000                # API URL
```

## Emergency Stop

```powershell
# Stop API server
# In active terminal: Ctrl+C

# Stop SQL Server
Stop-Service -Name "MSSQL`$SQLEXPRESS"

# Kill stuck Flask process
Get-Process python | Stop-Process -Force
```

## Update & Upgrade

```powershell
# Update Python packages
pip install --upgrade -r requirements.txt

# Update individual package
pip install --upgrade flask

# Check for outdated packages
pip list --outdated
```

## Memory & Performance Monitoring

```powershell
# Check system resources
Get-WmiObject win32_processor
Get-WmiObject win32_operatingsystem | Select-Object FreePhysicalMemory

# Monitor Python memory
py -m memory_profiler script.py

# Check database size
# SQL: EXEC sp_spaceused
```

## Creating Shortcuts (Windows)

```powershell
# Right-click desktop → New → Shortcut
# Target: powershell -NoExit -Command "cd C:\ML model && python backend\app.py"
# Name: Start API Server
```

## VPN/Remote Access (If Needed)

```powershell
# Allow remote connections to Flask
# In app.py, change: app.run(host='0.0.0.0')

# Use ngrok for tunneling
# Download from: https://ngrok.com/
# Run: ngrok http 5000
# Share public URL
```

## Frequently Used Commands

```powershell
# Start everything with one command
cd backend; python app.py

# Or use batch file
start-server.bat

# Test API
Invoke-WebRequest http://127.0.0.1:5000/health | ConvertFrom-Json

# Check if API running
curl http://127.0.0.1:5000/health
```

---

**Keep this handy!** Screenshot it or save as bookmark.

**Need help?** Check the full documentation in README.md or POWERBI_SETUP.md
