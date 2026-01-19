"""
Advanced analytics for Pickup Soccer using PySpark
"""
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import (
    col, avg, sum as spark_sum, count, max as spark_max, min as spark_min,
    stddev, percentile_approx, when, lit, explode, array, struct, 
    row_number, rank, dense_rank, datediff, current_date, concat_ws
)
from pyspark.sql.window import Window
import argparse
from datetime import datetime

from config import SPARK_CONFIG, SAMPLE_DIR
from models import PlayerSchema, GameSchema


class SoccerAnalytics:
    """Advanced analytics engine for pickup soccer data"""
    
    def __init__(self, spark: SparkSession):
        self.spark = spark
    
    def load_data(self, data_dir: str):
        """Load players and games data"""
        players_path = f"{data_dir}/players"
        games_path = f"{data_dir}/games"
        
        self.players_df = self.spark.read.format("parquet").load(players_path)
        self.games_df = self.spark.read.format("parquet").load(games_path)
        
        print(f"✅ Loaded {self.players_df.count()} players")
        print(f"✅ Loaded {self.games_df.count()} games")
    
    def player_performance_analysis(self) -> DataFrame:
        """Analyze player performance metrics"""
        print("\n📊 PLAYER PERFORMANCE ANALYSIS")
        print("-" * 60)
        
        analysis = self.players_df.filter(
            col("total_games") > 0
        ).select(
            "player_id",
            "name",
            "position",
            "skill_level",
            "total_games",
            "total_goals",
            "total_assists",
            (col("total_goals") / col("total_games")).alias("goals_per_game"),
            (col("total_assists") / col("total_games")).alias("assists_per_game"),
            ((col("total_goals") + col("total_assists")) / col("total_games")).alias("contributions_per_game")
        ).orderBy(
            col("contributions_per_game").desc()
        )
        
        analysis.show(20, truncate=False)
        return analysis
    
    def position_distribution(self) -> DataFrame:
        """Analyze player distribution by position"""
        print("\n👥 POSITION DISTRIBUTION")
        print("-" * 60)
        
        distribution = self.players_df.groupBy("position").agg(
            count("player_id").alias("player_count"),
            avg("skill_level").alias("avg_skill"),
            avg("age").alias("avg_age"),
            avg("total_goals").alias("avg_goals"),
            avg("total_assists").alias("avg_assists")
        ).orderBy(col("player_count").desc())
        
        distribution.show(truncate=False)
        return distribution
    
    def skill_level_analysis(self) -> DataFrame:
        """Analyze players by skill level"""
        print("\n⭐ SKILL LEVEL ANALYSIS")
        print("-" * 60)
        
        skill_analysis = self.players_df.groupBy("skill_level").agg(
            count("player_id").alias("player_count"),
            avg("total_games").alias("avg_games"),
            avg("total_goals").alias("avg_goals"),
            avg("age").alias("avg_age")
        ).orderBy("skill_level")
        
        skill_analysis.show(truncate=False)
        return skill_analysis
    
    def top_performers(self, metric: str = "goals", limit: int = 10) -> DataFrame:
        """Get top performers by specific metric"""
        print(f"\n🏆 TOP {limit} PERFORMERS BY {metric.upper()}")
        print("-" * 60)
        
        metric_col = f"total_{metric}"
        
        top = self.players_df.select(
            "player_id",
            "name",
            "position",
            "skill_level",
            "total_games",
            col(metric_col).alias(metric)
        ).orderBy(
            col(metric).desc()
        ).limit(limit)
        
        top.show(truncate=False)
        return top
    
    def game_statistics(self) -> DataFrame:
        """Analyze game statistics"""
        print("\n⚽ GAME STATISTICS")
        print("-" * 60)
        
        stats = self.games_df.agg(
            count("game_id").alias("total_games"),
            avg("team_a_score").alias("avg_score_team_a"),
            avg("team_b_score").alias("avg_score_team_b"),
            avg((col("team_a_score") + col("team_b_score"))).alias("avg_total_goals"),
            spark_max("team_a_score").alias("highest_score_team_a"),
            spark_max("team_b_score").alias("highest_score_team_b"),
            avg("duration_minutes").alias("avg_duration")
        )
        
        stats.show(truncate=False)
        return stats
    
    def games_by_location(self) -> DataFrame:
        """Analyze games by location"""
        print("\n📍 GAMES BY LOCATION")
        print("-" * 60)
        
        location_stats = self.games_df.groupBy("location").agg(
            count("game_id").alias("games_played"),
            avg("team_a_score").alias("avg_score_a"),
            avg("team_b_score").alias("avg_score_b"),
            avg((col("team_a_score") + col("team_b_score"))).alias("avg_total_goals")
        ).orderBy(col("games_played").desc())
        
        location_stats.show(truncate=False)
        return location_stats
    
    def weather_impact(self) -> DataFrame:
        """Analyze impact of weather on game outcomes"""
        print("\n🌤️ WEATHER IMPACT ON GAMES")
        print("-" * 60)
        
        weather_analysis = self.games_df.groupBy("weather").agg(
            count("game_id").alias("games_played"),
            avg((col("team_a_score") + col("team_b_score"))).alias("avg_total_goals"),
            avg("duration_minutes").alias("avg_duration")
        ).orderBy(col("games_played").desc())
        
        weather_analysis.show(truncate=False)
        return weather_analysis
    
    def player_consistency_score(self) -> DataFrame:
        """Calculate player consistency scores"""
        print("\n📈 PLAYER CONSISTENCY SCORES")
        print("-" * 60)
        
        # Calculate consistency based on games played and performance
        consistency = self.players_df.select(
            "player_id",
            "name",
            "position",
            "total_games",
            "total_goals",
            "total_assists",
            (
                (col("total_games") * 0.3) +
                ((col("total_goals") / col("total_games")) * 100 * 0.4) +
                ((col("total_assists") / col("total_games")) * 100 * 0.3)
            ).alias("consistency_score")
        ).filter(
            col("total_games") > 0
        ).orderBy(
            col("consistency_score").desc()
        )
        
        consistency.show(20, truncate=False)
        return consistency
    
    def win_rate_by_skill(self) -> DataFrame:
        """Analyze win rates based on team skill composition"""
        print("\n🎯 WIN RATE ANALYSIS")
        print("-" * 60)
        
        # Add win indicators
        games_with_winners = self.games_df.withColumn(
            "winner",
            when(col("team_a_score") > col("team_b_score"), "team_a")
            .when(col("team_b_score") > col("team_a_score"), "team_b")
            .otherwise("draw")
        )
        
        win_stats = games_with_winners.groupBy("winner").agg(
            count("game_id").alias("occurrences")
        )
        
        win_stats.show(truncate=False)
        return win_stats
    
    def run_full_analysis(self):
        """Run complete analysis suite"""
        print("\n" + "="*60)
        print("PICKUP SOCCER - COMPREHENSIVE ANALYTICS REPORT")
        print("="*60)
        
        self.player_performance_analysis()
        self.position_distribution()
        self.skill_level_analysis()
        self.top_performers("goals", 10)
        self.top_performers("assists", 10)
        self.player_consistency_score()
        self.game_statistics()
        self.games_by_location()
        self.weather_impact()
        self.win_rate_by_skill()
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)


def main():
    """Main analytics entry point"""
    parser = argparse.ArgumentParser(description="Pickup Soccer Analytics")
    parser.add_argument(
        "--data-dir",
        type=str,
        default=str(SAMPLE_DIR),
        help="Directory containing player and game data"
    )
    parser.add_argument(
        "--analysis",
        type=str,
        choices=["full", "players", "games", "performance"],
        default="full",
        help="Type of analysis to run"
    )
    
    args = parser.parse_args()
    
    # Create Spark session
    spark = SparkSession.builder \
        .appName("SoccerAnalytics") \
        .master("local[*]") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    
    try:
        analytics = SoccerAnalytics(spark)
        analytics.load_data(args.data_dir)
        
        if args.analysis == "full":
            analytics.run_full_analysis()
        elif args.analysis == "players":
            analytics.player_performance_analysis()
            analytics.position_distribution()
            analytics.skill_level_analysis()
        elif args.analysis == "games":
            analytics.game_statistics()
            analytics.games_by_location()
            analytics.weather_impact()
        elif args.analysis == "performance":
            analytics.top_performers("goals")
            analytics.top_performers("assists")
            analytics.player_consistency_score()
        
    except Exception as e:
        print(f"\n❌ Error running analytics: {e}")
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
