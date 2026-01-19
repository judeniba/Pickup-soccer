# Pickup Soccer - Environment Setup Script
# Run this before working with the project

Write-Host "🚀 Setting up Pickup Soccer environment..." -ForegroundColor Cyan

# Activate Python 3.11 virtual environment
.\venv311\Scripts\Activate.ps1

# Set Java environment
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.0.17.10-hotspot"

# Set Hadoop home for Windows compatibility  
$env:HADOOP_HOME = "C:\hadoop"

# Update PATH
$env:PATH = "$env:JAVA_HOME\bin;$env:HADOOP_HOME\bin;$env:PATH"

Write-Host "✅ Environment configured!" -ForegroundColor Green
Write-Host "   Python: " -NoNewline
python --version
Write-Host "   Java:   " -NoNewline  
java -version 2>&1 | Select-String "version" | Select-Object -First 1
Write-Host ""
Write-Host "📚 Available commands:" -ForegroundColor Yellow
Write-Host "   python scripts/generate_data.py       - Generate sample data"
Write-Host "   python run_all_tests.py               - Run all tests"
Write-Host "   python run_integration.py             - Run integration workflow"
Write-Host "   python src/main.py --sample-data      - Run main application"
Write-Host ""
