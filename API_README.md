# 🌐 Pickup Soccer REST API

## Quick Start

```powershell
# Install dependencies (one time)
.\venv311\Scripts\Activate.ps1
pip install fastapi "uvicorn[standard]"

# Launch API
.\run_api.ps1
```

## API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Base URL**: http://localhost:8000

## Example Requests

### Get All Players
```bash
GET http://localhost:8000/api/players
```

### Get Players by Position
```bash
GET http://localhost:8000/api/players?position=Forward&min_skill=7
```

### Get Top Scorers
```bash
GET http://localhost:8000/api/analytics/top-scorers?limit=10
```

### Balance Teams
```bash
POST http://localhost:8000/api/teams/balance?team_size=5&method=skill
```

### Get Summary Statistics
```bash
GET http://localhost:8000/api/stats/summary
```

## Response Format

All responses are in JSON format:

```json
{
  "player_id": "P123abc",
  "name": "John Smith",
  "position": "Forward",
  "skill_level": 8,
  "total_games": 45,
  "total_goals": 67,
  "total_assists": 23
}
```

## Try It Now!

After starting the API, open your browser to:
**http://localhost:8000/docs**

You'll see an interactive interface where you can test all endpoints!
