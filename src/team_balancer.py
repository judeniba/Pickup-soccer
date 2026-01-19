"""
Team balancing algorithm using PySpark
"""
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, avg, sum as spark_sum, array, lit, explode, struct
import random
from typing import List, Tuple

from config import SPARK_CONFIG, DEFAULT_TEAM_SIZE
from models import PlayerSchema, TeamSchema


class TeamBalancer:
    """Intelligent team balancing based on player skills"""
    
    def __init__(self, spark: SparkSession):
        self.spark = spark
    
    def balance_teams_by_skill(
        self, 
        players_df: DataFrame, 
        team_size: int = DEFAULT_TEAM_SIZE
    ) -> Tuple[DataFrame, DataFrame]:
        """
        Balance two teams based on player skill levels
        Uses greedy algorithm to minimize skill difference
        """
        # Validate team_size
        if team_size < 1:
            raise ValueError(f"Team size must be positive, got {team_size}")
        
        # Get active players and sort by skill level
        active_players = players_df.filter(col("active") == True) \
            .orderBy(col("skill_level").desc()) \
            .collect()
        
        if len(active_players) < team_size * 2:
            raise ValueError(
                f"Not enough active players. Need {team_size * 2}, have {len(active_players)}"
            )
        
        # Select players for this game
        selected_players = active_players[:team_size * 2]
        
        # Initialize teams
        team_a = []
        team_b = []
        team_a_skill = 0
        team_b_skill = 0
        
        # Greedy balancing: assign each player to team with lower total skill
        for player in selected_players:
            if team_a_skill <= team_b_skill:
                team_a.append(player)
                team_a_skill += player.skill_level
            else:
                team_b.append(player)
                team_b_skill += player.skill_level
        
        # Convert back to DataFrames
        team_a_df = self.spark.createDataFrame(team_a, PlayerSchema.get_schema())
        team_b_df = self.spark.createDataFrame(team_b, PlayerSchema.get_schema())
        
        return team_a_df, team_b_df
    
    def balance_teams_by_position(
        self,
        players_df: DataFrame,
        team_size: int = DEFAULT_TEAM_SIZE
    ) -> Tuple[DataFrame, DataFrame]:
        """
        Balance teams considering both skill and position
        Ensures each team has balanced positions
        """
        # Validate team_size
        if team_size < 1:
            raise ValueError(f"Team size must be positive, got {team_size}")
        
        active_players = players_df.filter(col("active") == True).collect()
        
        if len(active_players) < team_size * 2:
            raise ValueError(
                f"Not enough active players. Need {team_size * 2}, have {len(active_players)}"
            )
        
        # Group players by position
        positions = {}
        for player in active_players:
            pos = player.position
            if pos not in positions:
                positions[pos] = []
            positions[pos].append(player)
        
        # Sort each position by skill level
        for pos in positions:
            positions[pos].sort(key=lambda p: p.skill_level, reverse=True)
        
        team_a = []
        team_b = []
        
        # Distribute players by position
        for pos, players_list in positions.items():
            for i, player in enumerate(players_list):
                if len(team_a) >= team_size and len(team_b) >= team_size:
                    break
                
                if i % 2 == 0 and len(team_a) < team_size:
                    team_a.append(player)
                elif len(team_b) < team_size:
                    team_b.append(player)
                elif len(team_a) < team_size:
                    team_a.append(player)
        
        team_a_df = self.spark.createDataFrame(team_a, PlayerSchema.get_schema())
        team_b_df = self.spark.createDataFrame(team_b, PlayerSchema.get_schema())
        
        return team_a_df, team_b_df
    
    def get_team_stats(self, team_df: DataFrame) -> dict:
        """Calculate team statistics"""
        stats = team_df.agg(
            avg("skill_level").alias("avg_skill"),
            spark_sum("skill_level").alias("total_skill"),
            avg("age").alias("avg_age")
        ).collect()[0]
        
        positions = team_df.groupBy("position").count().collect()
        position_dist = {row.position: row['count'] for row in positions}
        
        return {
            "avg_skill": round(stats.avg_skill, 2),
            "total_skill": stats.total_skill,
            "avg_age": round(stats.avg_age, 1),
            "positions": position_dist,
            "size": team_df.count()
        }
    
    def display_teams(self, team_a_df: DataFrame, team_b_df: DataFrame):
        """Display team compositions and statistics"""
        print("\n" + "="*80)
        print("TEAM BALANCING RESULTS")
        print("="*80)
        
        print("\n🔵 TEAM A")
        print("-" * 80)
        team_a_df.select("name", "position", "skill_level", "age").show(truncate=False)
        
        team_a_stats = self.get_team_stats(team_a_df)
        print(f"Average Skill: {team_a_stats['avg_skill']}")
        print(f"Total Skill: {team_a_stats['total_skill']}")
        print(f"Average Age: {team_a_stats['avg_age']}")
        print(f"Position Distribution: {team_a_stats['positions']}")
        
        print("\n🔴 TEAM B")
        print("-" * 80)
        team_b_df.select("name", "position", "skill_level", "age").show(truncate=False)
        
        team_b_stats = self.get_team_stats(team_b_df)
        print(f"Average Skill: {team_b_stats['avg_skill']}")
        print(f"Total Skill: {team_b_stats['total_skill']}")
        print(f"Average Age: {team_b_stats['avg_age']}")
        print(f"Position Distribution: {team_b_stats['positions']}")
        
        skill_diff = abs(team_a_stats['avg_skill'] - team_b_stats['avg_skill'])
        print(f"\n⚖️  Skill Difference: {skill_diff:.2f}")
        
        if skill_diff < 0.5:
            print("✅ Teams are well balanced!")
        elif skill_diff < 1.0:
            print("✓ Teams are reasonably balanced")
        else:
            print("⚠️  Teams may need rebalancing")
        
        print("="*80 + "\n")


def main():
    """Main team balancing entry point"""
    import argparse
    from pathlib import Path
    from config import SAMPLE_DIR
    
    parser = argparse.ArgumentParser(description="Balance pickup soccer teams")
    parser.add_argument(
        "--data-dir",
        type=str,
        default=str(SAMPLE_DIR),
        help="Directory containing player data"
    )
    parser.add_argument(
        "--team-size",
        type=int,
        default=DEFAULT_TEAM_SIZE,
        help="Number of players per team"
    )
    parser.add_argument(
        "--method",
        type=str,
        choices=["skill", "position"],
        default="skill",
        help="Balancing method: skill or position-based"
    )
    
    args = parser.parse_args()
    
    # Create Spark session
    spark = SparkSession.builder \
        .appName("TeamBalancer") \
        .master("local[*]") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    
    try:
        # Load players
        players_path = f"{args.data_dir}/players"
        players_df = spark.read.format("parquet").load(players_path)
        
        print(f"\n✅ Loaded {players_df.count()} players")
        
        # Initialize balancer
        balancer = TeamBalancer(spark)
        
        # Balance teams
        if args.method == "skill":
            print(f"\n⚖️  Balancing teams by skill level (team size: {args.team_size})")
            team_a, team_b = balancer.balance_teams_by_skill(players_df, args.team_size)
        else:
            print(f"\n⚖️  Balancing teams by position and skill (team size: {args.team_size})")
            team_a, team_b = balancer.balance_teams_by_position(players_df, args.team_size)
        
        # Display results
        balancer.display_teams(team_a, team_b)
        
    except Exception as e:
        print(f"\n❌ Error balancing teams: {e}")
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
