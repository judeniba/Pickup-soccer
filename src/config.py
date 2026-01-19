"""
Configuration settings for Pickup Soccer Spark application
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PLAYERS_DIR = DATA_DIR / "players"
GAMES_DIR = DATA_DIR / "games"
SAMPLE_DIR = DATA_DIR / "sample"

# Spark Configuration
SPARK_CONFIG = {
    "spark.app.name": "PickupSoccerAnalytics",
    "spark.master": "local[*]",  # Use all available cores
    "spark.sql.shuffle.partitions": "4",
    "spark.executor.memory": "2g",
    "spark.driver.memory": "1g",
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true"
}

# Application Settings
DEFAULT_TEAM_SIZE = 5
MIN_SKILL_LEVEL = 1
MAX_SKILL_LEVEL = 10
GAME_DURATION_MINUTES = 90

# Data Settings
DATE_FORMAT = "%Y-%m-%d"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# Output formats
OUTPUT_FORMAT = "parquet"  # Can be: parquet, delta, json, csv

# Create directories if they don't exist
for directory in [DATA_DIR, PLAYERS_DIR, GAMES_DIR, SAMPLE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
