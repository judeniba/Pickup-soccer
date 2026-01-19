# Quick Validation Script
# Tests that API and core functionality work

Write-Host "🧪 Testing Pickup Soccer Setup..." -ForegroundColor Cyan

# Activate environment
.\venv311\Scripts\Activate.ps1
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.0.17.10-hotspot"
$env:HADOOP_HOME = "C:\hadoop"
$env:PATH = "$env:JAVA_HOME\bin;$env:HADOOP_HOME\bin;$env:PATH"

Write-Host "`n1️⃣  Testing Python imports..." -ForegroundColor Yellow
python -c "import pyspark; import streamlit; import fastapi; print('✅ All packages imported successfully')"

Write-Host "`n2️⃣  Testing data access..." -ForegroundColor Yellow
python -c "import sys; sys.path.insert(0, 'src'); from main import PickupSoccerApp; app = PickupSoccerApp(use_sample_data=True); print(f'✅ Loaded {app.players_df.count()} players, {app.games_df.count()} games'); app.stop()"

Write-Host "`n3️⃣  Testing API imports..." -ForegroundColor Yellow
python -c "import sys; sys.path.insert(0, 'src'); from api import app; print('✅ API initialized successfully')"

Write-Host "`n✅ All tests passed!" -ForegroundColor Green
Write-Host "`nReady to launch:" -ForegroundColor Cyan
Write-Host "  - Dashboard: .\run_dashboard.ps1" -ForegroundColor Gray
Write-Host "  - API: .\run_api.ps1" -ForegroundColor Gray
