# Launch Pickup Soccer REST API
# This script activates the environment and starts the FastAPI server

Write-Host "🚀 Launching Pickup Soccer API..." -ForegroundColor Cyan

# Activate Python 3.11 virtual environment
.\venv311\Scripts\Activate.ps1

# Set environment variables
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.0.17.10-hotspot"
$env:HADOOP_HOME = "C:\hadoop"
$env:PATH = "$env:JAVA_HOME\bin;$env:HADOOP_HOME\bin;$env:PATH"

Write-Host "✅ Environment configured!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Starting API server..." -ForegroundColor Yellow
Write-Host "   API will be available at:" -ForegroundColor Gray
Write-Host "   - Local: http://localhost:8000" -ForegroundColor Cyan
Write-Host "   - Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "   - ReDoc: http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Launch FastAPI with Uvicorn
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
