# Launch Pickup Soccer Dashboard
# This script activates the environment and starts the Streamlit dashboard

Write-Host "🚀 Launching Pickup Soccer Dashboard..." -ForegroundColor Cyan

# Activate Python 3.11 virtual environment
.\venv311\Scripts\Activate.ps1

# Set environment variables
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.0.17.10-hotspot"
$env:HADOOP_HOME = "C:\hadoop"
$env:PATH = "$env:JAVA_HOME\bin;$env:HADOOP_HOME\bin;$env:PATH"

Write-Host "✅ Environment configured!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Starting dashboard..." -ForegroundColor Yellow
Write-Host "   The dashboard will open in your browser automatically" -ForegroundColor Gray
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Launch Streamlit
streamlit run dashboard.py
