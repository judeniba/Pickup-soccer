"""
Generate sample data for Pickup Soccer application
"""
from pyspark.sql import SparkSession
from datetime import datetime, timedelta
import random
import uuid
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import PlayerSchema, GameSchema, create_player_record, create_game_record
from src.config import SPARK_CONFIG, SAMPLE_DIR, MIN_SKILL_LEVEL, MAX_SKILL_LEVEL


# Sample data
FIRST_NAMES = [
    "John", "Michael", "David", "James", "Robert", "William", "Alex", "Chris",
    "Daniel", "Matthew", "Andrew", "Ryan", "Kevin", "Brian", "Steven", "Jason",
    "Justin", "Brandon", "Eric", "Kyle", "Tyler", "Josh", "Nick", "Adam",
    "Sarah", "Emily", "Jessica", "Ashley", "Amanda", "Maria", "Lisa", "Rachel"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Martinez", "Davis",
    "Rodriguez", "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Jackson", "Lee",
    "Walker", "Hall", "Allen", "Young", "King", "Wright", "Lopez", "Hill"
]

POSITIONS = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
PREFERRED_FEET = ["Right", "Left", "Both"]
LOCATIONS = ["Main Field", "North Park", "South Stadium", "East Arena", "West Ground"]
WEATHER_CONDITIONS = ["Clear", "Cloudy", "Light Rain", "Sunny", "Partly Cloudy"]
FIELD_CONDITIONS = ["Excellent", "Good", "Fair", "Wet"]


def generate_players(num_players: int = 100) -> list:
    """Generate sample player data"""
    players = []
    
    for i in range(num_players):
        player_id = f"P{str(uuid.uuid4())[:8]}"
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        
        player = create_player_record(
            player_id=player_id,
            name=name,
            skill_level=random.randint(MIN_SKILL_LEVEL, MAX_SKILL_LEVEL),
            position=random.choice(POSITIONS),
            preferred_foot=random.choice(PREFERRED_FEET),
            age=random.randint(18, 45),
            height_cm=random.randint(160, 195),
            weight_kg=random.randint(60, 95),
            active=random.random() > 0.1,  # 90% active
            joined_date=datetime.now() - timedelta(days=random.randint(1, 1000)),
            total_games=random.randint(0, 200),
            total_goals=random.randint(0, 50),
            total_assists=random.randint(0, 40)
        )
        
        players.append(player)
    
    return players


def generate_games(player_ids: list, num_games: int = 50, team_size: int = 5) -> list:
    """Generate sample game data"""
    games = []
    
    for i in range(num_games):
        # Randomly select players for both teams
        available_players = random.sample(player_ids, team_size * 2)
        team_a_players = available_players[:team_size]
        team_b_players = available_players[team_size:]
        
        game_id = f"G{str(uuid.uuid4())[:8]}"
        game_date = datetime.now() - timedelta(days=random.randint(0, 365))
        
        game = create_game_record(
            game_id=game_id,
            team_a_players=team_a_players,
            team_b_players=team_b_players,
            location=random.choice(LOCATIONS),
            date=game_date,
            team_a_score=random.randint(0, 8),
            team_b_score=random.randint(0, 8),
            duration_minutes=random.choice([60, 75, 90]),
            weather=random.choice(WEATHER_CONDITIONS),
            field_condition=random.choice(FIELD_CONDITIONS),
            completed=True
        )
        
        games.append(game)
    
    return games


def main():
    """Generate and save sample data"""
    print("="*60)
    print("GENERATING SAMPLE DATA FOR PICKUP SOCCER")
    print("="*60)
    
    # Create Spark session
    spark = SparkSession.builder \
        .appName("DataGenerator") \
        .master("local[*]") \
        .getOrCreate()
    
    try:
        # Generate players
        print("\n📝 Generating players...")
        players_data = generate_players(num_players=100)
        players_df = spark.createDataFrame(players_data, PlayerSchema.get_schema())
        
        print(f"✅ Generated {players_df.count()} players")
        print("\nSample players:")
        players_df.select("player_id", "name", "position", "skill_level").show(5)
        
        # Save players
        players_path = str(SAMPLE_DIR / "players")
        print(f"\n💾 Saving players to: {players_path}")
        players_df.write.format("parquet").mode("overwrite").save(players_path)
        
        # Generate games
        print("\n📝 Generating games...")
        player_ids = [row.player_id for row in players_df.select("player_id").collect()]
        games_data = generate_games(player_ids, num_games=50, team_size=5)
        games_df = spark.createDataFrame(games_data, GameSchema.get_schema())
        
        print(f"✅ Generated {games_df.count()} games")
        print("\nSample games:")
        games_df.select("game_id", "date", "location", "team_a_score", "team_b_score").show(5)
        
        # Save games
        games_path = str(SAMPLE_DIR / "games")
        print(f"\n💾 Saving games to: {games_path}")
        games_df.write.format("parquet").mode("overwrite").save(games_path)
        
        print("\n" + "="*60)
        print("✅ SAMPLE DATA GENERATION COMPLETE!")
        print("="*60)
        print(f"\nPlayers saved to: {players_path}")
        print(f"Games saved to: {games_path}")
        print("\nYou can now run the main application:")
        print("  python src/main.py --sample-data")
        
    except Exception as e:
        print(f"\n❌ Error generating data: {e}")
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
