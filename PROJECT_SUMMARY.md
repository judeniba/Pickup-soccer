# Pickup Soccer - Spark Analytics Platform

A comprehensive pickup soccer management system built with PySpark! 🚀⚽

## What I Built

This is a complete data analytics platform for managing pickup soccer games using Apache Spark's distributed computing capabilities. Here's what's included:

### Core Components

1. **Data Models** ([src/models.py](src/models.py))
   - Player schema with attributes like skill level, position, stats
   - Game schema with team compositions, scores, conditions
   - Helper functions for creating sample records

2. **Main Application** ([src/main.py](src/main.py))
   - Spark session initialization and management
   - Data loading/saving with Parquet format
   - Player and game management functions
   - Statistics dashboard

3. **Analytics Engine** ([src/analytics.py](src/analytics.py))
   - Player performance analysis
   - Position distribution metrics
   - Skill level analysis
   - Top performers tracking
   - Game statistics by location and weather
   - Player consistency scoring
   - Win rate analysis

4. **Team Balancer** ([src/team_balancer.py](src/team_balancer.py))
   - Skill-based team balancing
   - Position-aware team formation
   - Team statistics calculation
   - Balance verification

5. **Data Generator** ([scripts/generate_data.py](scripts/generate_data.py))
   - Generates sample player data (100 players)
   - Creates realistic game records (50 games)
   - Randomized stats and attributes

### Configuration

- **[src/config.py](src/config.py)**: Spark settings, paths, and application constants
- **[requirements.txt](requirements.txt)**: All Python dependencies including PySpark 3.5.0

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data
```bash
python scripts/generate_data.py
```

### 3. Run Analytics
```bash
python src/analytics.py --analysis full
```

### 4. Balance Teams
```bash
python src/team_balancer.py --team-size 5 --method skill
```

## Features Highlights

✅ **Distributed Processing**: Leverages Spark for scalable data processing  
✅ **Comprehensive Analytics**: Player stats, game insights, performance metrics  
✅ **Smart Team Balancing**: Algorithm-based team formation  
✅ **Flexible Storage**: Parquet format for efficient data storage  
✅ **Rich Schemas**: Structured data models for players, games, and stats  
✅ **Sample Data**: Built-in generator for testing and demos  

## Project Structure

```
pickup-soccer/
├── src/
│   ├── main.py              # Main Spark application
│   ├── models.py            # Data schemas
│   ├── analytics.py         # Analytics engine
│   ├── team_balancer.py     # Team formation
│   └── config.py            # Configuration
├── scripts/
│   └── generate_data.py     # Sample data generator
├── data/
│   ├── players/            # Player data storage
│   ├── games/              # Game records storage
│   └── sample/             # Sample datasets
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Technology Stack

- **Apache Spark 3.5.0**: Distributed data processing engine
- **PySpark**: Python API for Spark
- **Pandas & NumPy**: Data manipulation
- **PyArrow & Parquet**: Efficient columnar storage
- **Matplotlib & Seaborn**: Visualization (future use)

## Usage Examples

### Generate Custom Data
```python
from scripts.generate_data import generate_players, generate_games
players = generate_players(num_players=200)
games = generate_games(player_ids, num_games=100)
```

### Run Specific Analytics
```bash
# Player-focused analysis
python src/analytics.py --analysis players

# Game-focused analysis
python src/analytics.py --analysis games

# Performance metrics
python src/analytics.py --analysis performance
```

### Balance Teams with Different Methods
```bash
# Skill-based balancing
python src/team_balancer.py --method skill --team-size 7

# Position-aware balancing
python src/team_balancer.py --method position --team-size 5
```

## Next Steps

Potential enhancements:
- Add real-time game tracking
- Implement ML models for player skill prediction
- Create interactive dashboards with Plotly
- Add Delta Lake for ACID transactions
- Build REST API for data access
- Integrate with scheduling systems

## License

MIT License - Feel free to use and modify!

---

Built with ⚡ PySpark and ❤️ for pickup soccer!
