# 🚀 Pickup Soccer - Development Guide

## Current Status: ✅ Complete & Running

### What's Built:
1. ✅ **Core Spark Application** - Player & game management
2. ✅ **Analytics Engine** - 10+ analysis types
3. ✅ **Team Balancer** - Smart team formation
4. ✅ **Streamlit Dashboard** - Interactive web UI
5. ✅ **REST API** - FastAPI endpoints (NEW!)

---

## 🎯 Quick Start Commands

### Environment Setup (Run Once Per Session)
```powershell
.\setup_env.ps1
```

### Run Applications

**Dashboard (Interactive UI)**
```powershell
.\run_dashboard.ps1
# Opens at: http://localhost:8501
```

**REST API (Programmatic Access)**
```powershell
.\run_api.ps1
# Available at: http://localhost:8000
# Docs at: http://localhost:8000/docs
```

**Tests**
```powershell
python run_all_tests.py
```

**Data Generation**
```powershell
python scripts/generate_data.py
```

---

## 📡 REST API Endpoints

### Base URL: `http://localhost:8000`

#### Players
- `GET /api/players` - List all players
  - Query params: `position`, `min_skill`, `max_skill`, `limit`
- `GET /api/players/{player_id}` - Get specific player

#### Games
- `GET /api/games` - List all games
  - Query params: `location`, `weather`, `limit`
- `GET /api/games/{game_id}` - Get specific game

#### Analytics
- `GET /api/analytics/top-scorers?limit=10` - Top goal scorers
- `GET /api/analytics/top-assists?limit=10` - Top assist leaders
- `GET /api/analytics/position-stats` - Stats by position
- `GET /api/stats/summary` - Overall summary

#### Team Balancer
- `POST /api/teams/balance?team_size=5&method=skill` - Generate balanced teams

### Example API Calls

**Using PowerShell:**
```powershell
# Get all players
Invoke-RestMethod -Uri "http://localhost:8000/api/players" -Method GET

# Get top 5 scorers
Invoke-RestMethod -Uri "http://localhost:8000/api/analytics/top-scorers?limit=5" -Method GET

# Balance teams
Invoke-RestMethod -Uri "http://localhost:8000/api/teams/balance?team_size=5" -Method POST

# Get summary stats
Invoke-RestMethod -Uri "http://localhost:8000/api/stats/summary" -Method GET
```

**Using Python:**
```python
import requests

# Get all players
response = requests.get("http://localhost:8000/api/players")
players = response.json()

# Balance teams
response = requests.post("http://localhost:8000/api/teams/balance?team_size=5")
teams = response.json()
```

**Using Browser:**
- Visit: `http://localhost:8000/docs` for interactive API documentation
- Try out endpoints directly from the Swagger UI

---

## 🎨 Dashboard Features

### Pages Available:
1. **📊 Overview** - Key metrics and distributions
2. **👥 Players** - Player list with filters
3. **⚽ Games** - Game history and analysis
4. **📈 Analytics** - Advanced visualizations
5. **⚖️ Team Balancer** - Generate balanced teams

---

## 🛠️ Development Workflow

### 1. **Make Changes**
- Edit files in `src/` directory
- Add new analytics in `src/analytics.py`
- Add API endpoints in `api.py`
- Add dashboard pages in `dashboard.py`

### 2. **Test Changes**
```powershell
# Run tests
python run_all_tests.py

# Test specific module
python -m pytest tests/test_integration.py -v
```

### 3. **View Changes**
- **Dashboard**: Auto-reloads on save (if running with `--reload`)
- **API**: Auto-reloads on save (uvicorn --reload)

---

## 📂 Project Structure

```
Pickup-soccer/
├── src/                    # Core application
│   ├── main.py            # Main Spark app
│   ├── analytics.py       # Analytics engine
│   ├── team_balancer.py   # Team balancer
│   ├── models.py          # Data schemas
│   └── config.py          # Configuration
├── scripts/               # Utility scripts
│   └── generate_data.py   # Data generator
├── tests/                 # Test suite
├── data/                  # Data storage
│   └── sample/           # Sample data
├── dashboard.py           # Streamlit dashboard
├── api.py                 # FastAPI REST API
├── setup_env.ps1         # Environment setup
├── run_dashboard.ps1     # Launch dashboard
├── run_api.ps1           # Launch API
└── requirements.txt      # Dependencies
```

---

## 🔧 Troubleshooting

### Issue: Dashboard/API won't start
**Solution:**
```powershell
# Activate environment first
.\venv311\Scripts\Activate.ps1
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.0.17.10-hotspot"
$env:HADOOP_HOME = "C:\hadoop"
```

### Issue: "No module named 'config'"
**Solution:** Make sure you're running from the project root directory

### Issue: Java/Spark errors
**Solution:** Verify Java is installed and JAVA_HOME is set
```powershell
java -version
echo $env:JAVA_HOME
```

---

## 🎯 Next Development Steps

### Phase 1: Enhancements (Week 1-2)
- [ ] Add player rating system (ELO)
- [ ] Create player detail pages
- [ ] Add export functionality (CSV/PDF)
- [ ] Implement real-time updates

### Phase 2: Advanced Features (Week 3-6)
- [ ] Machine learning predictions
- [ ] Historical performance trends
- [ ] Head-to-head statistics
- [ ] Advanced team chemistry

### Phase 3: Production (Week 7-12)
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Cloud deployment
- [ ] Authentication & authorization

---

## 📚 Resources

### Documentation
- **Streamlit**: https://docs.streamlit.io/
- **FastAPI**: https://fastapi.tiangolo.com/
- **PySpark**: https://spark.apache.org/docs/latest/api/python/

### API Testing Tools
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Postman**: Download at https://www.postman.com/

---

## 🎉 You're Ready!

Your Pickup Soccer platform now has:
- ✅ Interactive web dashboard
- ✅ RESTful API for programmatic access
- ✅ Complete test suite
- ✅ Sample data
- ✅ Development environment

**Start exploring:**
1. Launch dashboard: `.\run_dashboard.ps1`
2. Launch API: `.\run_api.ps1`
3. Open browser and start building!

Happy coding! ⚽🚀
