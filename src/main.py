"""
Main Spark application for Pickup Soccer management
"""
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, avg, count, sum as spark_sum, max as spark_max
import logging
from pathlib import Path

from config import SPARK_CONFIG, PLAYERS_DIR, GAMES_DIR, OUTPUT_FORMAT
from models import PlayerSchema, GameSchema


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PickupSoccerApp:
    """Main application class for Pickup Soccer management"""
    
    def __init__(self, use_sample_data: bool = False):
        """Initialize Spark session and application
        
        Args:
            use_sample_data: If True, use sample data directory
        """
        self.spark = self._create_spark_session()
        self.use_sample_data = use_sample_data
        logger.info("Pickup Soccer Spark application initialized")
    
    def _create_spark_session(self) -> SparkSession:
        """Create and configure Spark session"""
        builder = SparkSession.builder
        
        # Apply all configuration settings
        for key, value in SPARK_CONFIG.items():
            builder = builder.config(key, value)
        
        spark = builder.getOrCreate()
        spark.sparkContext.setLogLevel("WARN")
        
        logger.info(f"Spark session created: {spark.version}")
        return spark
    
    def load_players(self, path: str = None) -> DataFrame:
        """Load player data from storage"""
        if path is None:
            path = str(Path("data/sample/players") if self.use_sample_data else PLAYERS_DIR)
        logger.info(f"Loading players from: {path}")
        
        try:
            df = self.spark.read.format(OUTPUT_FORMAT).load(path)
            logger.info(f"Loaded {df.count()} players")
            return df
        except Exception as e:
            logger.warning(f"Could not load players: {e}")
            # Return empty DataFrame with schema
            return self.spark.createDataFrame([], PlayerSchema.get_schema())
    
    def load_games(self, path: str = None) -> DataFrame:
        """Load game data from storage"""
        if path is None:
            path = str(Path("data/sample/games") if self.use_sample_data else GAMES_DIR)
        logger.info(f"Loading games from: {path}")
        
        try:
            df = self.spark.read.format(OUTPUT_FORMAT).load(path)
            logger.info(f"Loaded {df.count()} games")
            return df
        except Exception as e:
            logger.warning(f"Could not load games: {e}")
            # Return empty DataFrame with schema
            return self.spark.createDataFrame([], GameSchema.get_schema())
    
    def save_players(self, df: DataFrame, path: str = None, mode: str = "overwrite"):
        """Save player data to storage"""
        path = path or str(PLAYERS_DIR)
        logger.info(f"Saving players to: {path}")
        
        df.write.format(OUTPUT_FORMAT).mode(mode).save(path)
        logger.info(f"Saved {df.count()} players")
    
    def save_games(self, df: DataFrame, path: str = None, mode: str = "overwrite"):
        """Save game data to storage"""
        path = path or str(GAMES_DIR)
        logger.info(f"Saving games to: {path}")
        
        df.write.format(OUTPUT_FORMAT).mode(mode).save(path)
        logger.info(f"Saved {df.count()} games")
    
    def get_active_players(self, skill_level_min: int = None) -> DataFrame:
        """Get all active players, optionally filtered by minimum skill level"""
        players_df = self.load_players()
        
        # Filter active players
        result = players_df.filter(col("active") == True)
        
        # Apply skill level filter if specified
        if skill_level_min is not None:
            result = result.filter(col("skill_level") >= skill_level_min)
        
        logger.info(f"Found {result.count()} active players")
        return result
    
    def get_player_summary(self) -> DataFrame:
        """Get summary statistics for all players"""
        players_df = self.load_players()
        
        summary = players_df.groupBy("position").agg(
            count("player_id").alias("total_players"),
            avg("skill_level").alias("avg_skill_level"),
            avg("age").alias("avg_age"),
            spark_sum("total_goals").alias("total_goals"),
            spark_sum("total_assists").alias("total_assists"),
            spark_sum("total_games").alias("total_games")
        ).orderBy(col("total_players").desc())
        
        return summary
    
    def get_top_scorers(self, limit: int = 10) -> DataFrame:
        """Get top goal scorers"""
        players_df = self.load_players()
        
        top_scorers = players_df.select(
            "player_id", "name", "position", "total_goals", "total_games"
        ).orderBy(
            col("total_goals").desc()
        ).limit(limit)
        
        return top_scorers
    
    def get_game_summary(self) -> DataFrame:
        """Get summary statistics for games"""
        games_df = self.load_games()
        
        summary = games_df.agg(
            count("game_id").alias("total_games"),
            avg("team_a_score").alias("avg_team_a_score"),
            avg("team_b_score").alias("avg_team_b_score"),
            avg("duration_minutes").alias("avg_duration"),
            spark_max("team_a_score").alias("max_score_team_a"),
            spark_max("team_b_score").alias("max_score_team_b")
        )
        
        return summary
    
    def show_statistics(self):
        """Display application statistics"""
        print("\n" + "="*60)
        print("PICKUP SOCCER - STATISTICS DASHBOARD")
        print("="*60)
        
        # Player statistics
        print("\n📊 PLAYER SUMMARY BY POSITION:")
        player_summary = self.get_player_summary()
        player_summary.show(truncate=False)
        
        # Top scorers
        print("\n⚽ TOP 10 SCORERS:")
        top_scorers = self.get_top_scorers()
        top_scorers.show(truncate=False)
        
        # Game statistics
        print("\n🏆 GAME SUMMARY:")
        game_summary = self.get_game_summary()
        game_summary.show(truncate=False)
        
        print("="*60 + "\n")
    
    @property
    def players_df(self) -> DataFrame:
        """Lazy-load players DataFrame"""
        if not hasattr(self, '_players_df'):
            self._players_df = self.load_players()
        return self._players_df
    
    @property
    def games_df(self) -> DataFrame:
        """Lazy-load games DataFrame"""
        if not hasattr(self, '_games_df'):
            self._games_df = self.load_games()
        return self._games_df
    
    def stop(self):
        """Stop Spark session"""
        logger.info("Stopping Spark session")
        self.spark.stop()


def main():
    """Main entry point"""
    logger.info("Starting Pickup Soccer application")
    
    # Initialize application
    app = PickupSoccerApp()
    
    try:
        # Display statistics
        app.show_statistics()
        
        # Keep application running for interactive use
        print("Application ready. Press Ctrl+C to exit.")
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
    finally:
        app.stop()
        logger.info("Application stopped")


if __name__ == "__main__":
    main()
