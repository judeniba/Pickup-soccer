# Setup and Installation Guide
# Pickup Soccer - Spark Analytics Platform

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB for application and dependencies
- **Java**: JDK 8 or 11 (required for Spark)

### Recommended Requirements
- **Python**: 3.9 or 3.10
- **RAM**: 16GB for optimal performance
- **CPU**: Multi-core processor (4+ cores)
- **Java**: JDK 11 (LTS version)

## Installation Steps

### Step 1: Install Python

#### Windows
```powershell
# Download Python from python.org
# Or use Windows Store
# Or use Chocolatey
choco install python --version=3.10.11

# Verify installation
python --version
```

#### macOS
```bash
# Using Homebrew
brew install python@3.10

# Verify installation
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3-pip python3-venv
python3 --version
```

### Step 2: Install Java (Required for Spark)

#### Windows
```powershell
# Using Chocolatey
choco install openjdk11

# Or download from: https://adoptium.net/
```

#### macOS
```bash
brew install openjdk@11
```

#### Linux
```bash
sudo apt install openjdk-11-jdk
```

**Verify Java Installation:**
```bash
java -version
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd C:\Users\judeniba\Documents\GitHub\Pickup-soccer

# Create virtual environment
python -m venv venv

# Activate virtual environment

# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows CMD:
venv\Scripts\activate.bat

# macOS/Linux:
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify PySpark installation
python -c "import pyspark; print(f'PySpark {pyspark.__version__} installed')"
```

### Step 5: Configure Environment

**Windows - Set JAVA_HOME:**
```powershell
# Add to system environment variables
[System.Environment]::SetEnvironmentVariable('JAVA_HOME', 'C:\Program Files\Java\jdk-11', 'User')

# Or add to PowerShell profile
$env:JAVA_HOME = "C:\Program Files\Java\jdk-11"
```

**macOS/Linux - Set JAVA_HOME:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

## Quick Start

### 1. Generate Sample Data
```bash
python scripts/generate_data.py
```

**Expected Output:**
```
Generating 100 players... ✅
Generating 50 games... ✅
Data saved to: data/sample/
```

### 2. Run Integration Tests
```bash
python tests/test_integration.py
```

**Expected Output:**
```
✅ PASS: PlayerSchema creation
✅ PASS: Generate sample players
✅ PASS: Team balancing
... (18 total tests)
Success Rate: 100%
```

### 3. Run Performance Benchmarks
```bash
python tests/test_performance.py
```

**Expected Output:**
```
⏱️  Benchmarking: Generate 1000 players
   ✅ Completed in 0.8432 seconds
... (20+ benchmarks)
```

### 4. Run Full Integration Workflow
```bash
python run_integration.py
```

**Expected Output:**
```
📍 STEP 1: Initialize Application ✅
📍 STEP 2: Load Data ✅
... (7 steps)
✅ END-TO-END WORKFLOW COMPLETED SUCCESSFULLY
```

## Testing Guide

### Test Suite Overview

| Test Type | File | Duration | Purpose |
|-----------|------|----------|---------|
| Integration | `tests/test_integration.py` | ~45s | Component integration |
| Performance | `tests/test_performance.py` | ~120s | Performance benchmarks |
| End-to-End | `run_integration.py` | ~60s | Complete workflow |

### Running Individual Test Suites

#### Integration Tests
```bash
python tests/test_integration.py
```

Tests covered:
- ✅ Data model schemas (4 tests)
- ✅ Sample data creation (2 tests)
- ✅ Main application (3 tests)
- ✅ Team balancer (3 tests)
- ✅ Analytics engine (5 tests)
- ✅ Data persistence (3 tests)

#### Performance Tests
```bash
python tests/test_performance.py
```

Benchmarks:
- ⏱️ Data generation (4 sizes)
- ⏱️ Read/write operations
- ⏱️ Filtering operations
- ⏱️ Aggregations
- ⏱️ Team balancing
- ⏱️ Analytics queries

### Expected Test Results

**Integration Tests:**
```
Total Tests: 18
✅ Passed: 18
❌ Failed: 0
Success Rate: 100%
```

**Performance Benchmarks:**
- Data generation (1000 records): < 2 seconds
- Read operations (10k records): < 1 second
- Aggregations (20k records): < 3 seconds
- Team balancing (200 players): < 500ms
- Full analytics: < 5 seconds

## Running the Application

### Main Application
```bash
# Run main application with sample data
python src/main.py
```

### Analytics
```bash
# Run full analytics suite
python src/analytics.py --analysis full --data-dir data/sample

# Run specific analytics
python src/analytics.py --analysis players --data-dir data/sample
python src/analytics.py --analysis games --data-dir data/sample
python src/analytics.py --analysis performance --data-dir data/sample
```

### Team Balancer
```bash
# Balance teams using skill-based algorithm
python src/team_balancer.py --team-size 5 --method skill --data-dir data/sample

# Balance teams using position-based algorithm
python src/team_balancer.py --team-size 5 --method position --data-dir data/sample
```

## Troubleshooting

### Common Issues

#### Issue: "Python was not found"
**Solution:**
```powershell
# Windows: Add Python to PATH
# Or use py launcher
py --version
py -m pip install -r requirements.txt
```

#### Issue: "JAVA_HOME is not set"
**Solution:**
```bash
# Find Java installation
# Windows:
where java

# macOS/Linux:
which java

# Set JAVA_HOME to the parent directory of /bin
export JAVA_HOME=/path/to/jdk
```

#### Issue: "Module 'pyspark' not found"
**Solution:**
```bash
# Ensure virtual environment is activated
# Reinstall PySpark
pip install --force-reinstall pyspark==3.5.0
```

#### Issue: "Permission denied" on data directories
**Solution:**
```bash
# Ensure write permissions
# Windows:
icacls data /grant Users:F /t

# macOS/Linux:
chmod -R 755 data/
```

#### Issue: Spark runs slowly
**Solution:**
```python
# Adjust Spark configuration in src/config.py
SPARK_CONFIG = {
    "spark.executor.memory": "4g",  # Increase memory
    "spark.driver.memory": "2g",
    "spark.sql.shuffle.partitions": "8",  # Increase partitions
}
```

## Validation Checklist

Use this checklist to verify installation:

- [ ] Python 3.8+ installed and accessible
- [ ] Java JDK 8/11 installed (verify with `java -version`)
- [ ] JAVA_HOME environment variable set
- [ ] Virtual environment created and activated
- [ ] All dependencies installed from requirements.txt
- [ ] PySpark imports successfully
- [ ] Sample data generated successfully
- [ ] Integration tests pass (18/18)
- [ ] Performance tests complete without errors
- [ ] End-to-end workflow executes successfully

## Performance Tuning

### For Small Datasets (<10k records)
```python
SPARK_CONFIG = {
    "spark.sql.shuffle.partitions": "2",
    "spark.executor.memory": "1g",
    "spark.driver.memory": "512m"
}
```

### For Medium Datasets (10k-100k records)
```python
SPARK_CONFIG = {
    "spark.sql.shuffle.partitions": "4",
    "spark.executor.memory": "2g",
    "spark.driver.memory": "1g"
}
```

### For Large Datasets (100k+ records)
```python
SPARK_CONFIG = {
    "spark.sql.shuffle.partitions": "8",
    "spark.executor.memory": "4g",
    "spark.driver.memory": "2g",
    "spark.sql.adaptive.enabled": "true"
}
```

## Next Steps

After successful installation:

1. ✅ Generate sample data
2. ✅ Run integration tests
3. ✅ Explore analytics features
4. ✅ Test team balancing
5. 📊 Start using with your own data
6. 🚀 Deploy to production

## Support

For issues or questions:
1. Check this setup guide
2. Review CODE_REVIEW_REPORT.md
3. Check logs in console output
4. Review Spark UI at http://localhost:4040 (when running)

## Additional Resources

- **PySpark Documentation**: https://spark.apache.org/docs/latest/api/python/
- **Spark Configuration**: https://spark.apache.org/docs/latest/configuration.html
- **Python Virtual Environments**: https://docs.python.org/3/library/venv.html
- **Java Installation**: https://adoptium.net/installation/

---

**Last Updated**: January 12, 2026
**Version**: 1.0.0
