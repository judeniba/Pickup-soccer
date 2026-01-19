# 🎯 QUICK REFERENCE CARD
# Pickup Soccer - Spark Analytics Platform

## 📦 INSTALLATION (First Time Setup)

```bash
# 1. Install Python 3.8+ and Java JDK 8/11
# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate sample data
python scripts/generate_data.py

# 4. Run tests to verify
python run_all_tests.py
```

## 🚀 DAILY USAGE

### Run Full Integration
```bash
python run_integration.py
```

### Generate New Sample Data
```bash
python scripts/generate_data.py
```

### Analytics Commands
```bash
# Full analysis
python src/analytics.py --analysis full --data-dir data/sample

# Player analysis only
python src/analytics.py --analysis players --data-dir data/sample

# Game analysis only
python src/analytics.py --analysis games --data-dir data/sample

# Performance analysis
python src/analytics.py --analysis performance --data-dir data/sample
```

### Team Balancing
```bash
# Skill-based (default)
python src/team_balancer.py --team-size 5 --method skill --data-dir data/sample

# Position-based
python src/team_balancer.py --team-size 7 --method position --data-dir data/sample
```

## 🧪 TESTING COMMANDS

```bash
# Run all tests (recommended)
python run_all_tests.py

# Run specific test suites
python tests/test_integration.py        # Integration tests
python tests/test_performance.py        # Performance benchmarks
python run_integration.py               # End-to-end workflow

# Run specific test suite from master runner
python run_all_tests.py --suite integration
python run_all_tests.py --suite performance
python run_all_tests.py --suite e2e
```

## 📁 IMPORTANT FILES

### Core Application
- `src/main.py` - Main application
- `src/analytics.py` - Analytics engine
- `src/team_balancer.py` - Team formation
- `src/config.py` - Configuration

### Documentation
- `README.md` - Start here
- `SETUP_GUIDE.md` - Installation help
- `CODE_REVIEW_REPORT.md` - Code quality
- `TESTING_REPORT.md` - Test results
- `BUILD_COMPLETE.md` - Build summary

### Data Locations
- `data/sample/players` - Sample player data
- `data/sample/games` - Sample game data
- `data/players` - Production player data
- `data/games` - Production game data

## 🎯 COMMON TASKS

### Check System Status
```bash
# Verify Python
python --version

# Verify PySpark
python -c "import pyspark; print(f'PySpark {pyspark.__version__}')"

# Verify Java
java -version
```

### View Sample Data
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()
df = spark.read.parquet("data/sample/players")
df.show()
```

### Custom Analytics
```python
from src.analytics import SoccerAnalytics
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").getOrCreate()
analytics = SoccerAnalytics(spark)
analytics.load_data("data/sample")
analytics.player_performance_analysis()
```

## 🐛 TROUBLESHOOTING

### Python Not Found
```bash
# Windows: Use py launcher
py --version
py -m pip install -r requirements.txt
```

### JAVA_HOME Not Set
```bash
# Windows PowerShell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-11"

# macOS/Linux
export JAVA_HOME=/usr/lib/jvm/java-11
```

### PySpark Not Found
```bash
pip install --force-reinstall pyspark==3.5.0
```

### Data Not Found
```bash
# Regenerate sample data
python scripts/generate_data.py
```

## 📊 EXPECTED OUTPUTS

### Sample Data Generation
```
✅ Generated 100 players
✅ Generated 50 games
Data saved to: data/sample/
```

### Integration Tests
```
Total Tests: 18
✅ Passed: 18
Success Rate: 100%
```

### Performance Tests
```
⏱️  Benchmarking: Generate 1000 players
   ✅ Completed in 0.84 seconds
[20+ benchmarks complete]
```

## ⚡ PERFORMANCE TIPS

### For Faster Processing
```python
# In src/config.py, increase:
SPARK_CONFIG = {
    "spark.executor.memory": "4g",
    "spark.sql.shuffle.partitions": "8"
}
```

### For Large Datasets
```python
# Add caching
df.cache()
df.count()  # Trigger caching
```

## 🔗 QUICK LINKS

- Full Setup: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- Code Review: [CODE_REVIEW_REPORT.md](CODE_REVIEW_REPORT.md)
- Test Report: [TESTING_REPORT.md](TESTING_REPORT.md)
- Build Summary: [BUILD_COMPLETE.md](BUILD_COMPLETE.md)

## 📞 HELP

1. **Installation issues**: Read [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. **Feature questions**: Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
3. **Code questions**: Read [CODE_REVIEW_REPORT.md](CODE_REVIEW_REPORT.md)

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: January 12, 2026

💡 **Pro Tip**: Run `python run_all_tests.py` before deploying to production!
