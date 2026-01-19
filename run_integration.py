"""
End-to-end integration script for Pickup Soccer application
Demonstrates complete workflow using all components
"""
import sys
import os
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import logging

from config import SPARK_CONFIG, SAMPLE_DIR
from models import PlayerSchema, GameSchema
from main import PickupSoccerApp
from analytics import SoccerAnalytics
from team_balancer import TeamBalancer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EndToEndWorkflow:
    """Complete workflow integrating all application components"""
    
    def __init__(self, use_sample_data: bool = True):
        self.use_sample_data = use_sample_data
        self.data_dir = str(SAMPLE_DIR) if use_sample_data else None
        
        print("\n" + "="*80)
        print("PICKUP SOCCER - END-TO-END INTEGRATION")
        print("="*80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Using sample data: {use_sample_data}")
        print("="*80 + "\n")
    
    def step1_initialize_application(self):
        """Step 1: Initialize main application"""
        print("📍 STEP 1: Initialize Application")
        print("-" * 80)
        
        self.app = PickupSoccerApp()
        logger.info("✅ Application initialized")
        print()
    
    def step2_load_data(self):
        """Step 2: Load player and game data"""
        print("📍 STEP 2: Load Data")
        print("-" * 80)
        
        if self.use_sample_data:
            players_path = f"{self.data_dir}/players"
            games_path = f"{self.data_dir}/games"
            
            try:
                self.players_df = self.app.spark.read.format("parquet").load(players_path)
                self.games_df = self.app.spark.read.format("parquet").load(games_path)
                
                player_count = self.players_df.count()
                game_count = self.games_df.count()
                
                print(f"✅ Loaded {player_count} players")
                print(f"✅ Loaded {game_count} games")
                logger.info(f"Data loaded: {player_count} players, {game_count} games")
            except Exception as e:
                print(f"⚠️  Sample data not found: {e}")
                print("💡 Run: python scripts/generate_data.py")
                return False
        else:
            self.players_df = self.app.load_players()
            self.games_df = self.app.load_games()
            print(f"✅ Loaded {self.players_df.count()} players")
            print(f"✅ Loaded {self.games_df.count()} games")
        
        print()
        return True
    
    def step3_basic_statistics(self):
        """Step 3: Display basic statistics"""
        print("📍 STEP 3: Basic Statistics")
        print("-" * 80)
        
        print("\n📊 Player Summary:")
        player_summary = self.app.get_player_summary()
        player_summary.show(10, truncate=False)
        
        print("\n⚽ Top 10 Scorers:")
        top_scorers = self.app.get_top_scorers(10)
        top_scorers.show(10, truncate=False)
        
        print("\n🏆 Game Summary:")
        game_summary = self.app.get_game_summary()
        game_summary.show(truncate=False)
        
        print()
    
    def step4_advanced_analytics(self):
        """Step 4: Run advanced analytics"""
        print("📍 STEP 4: Advanced Analytics")
        print("-" * 80)
        
        analytics = SoccerAnalytics(self.app.spark)
        analytics.players_df = self.players_df
        analytics.games_df = self.games_df
        
        print("\n📈 Player Performance Analysis:")
        perf_df = analytics.player_performance_analysis()
        
        print("\n👥 Position Distribution:")
        pos_df = analytics.position_distribution()
        
        print("\n⭐ Skill Level Analysis:")
        skill_df = analytics.skill_level_analysis()
        
        print("\n🏅 Player Consistency Scores:")
        consistency_df = analytics.player_consistency_score()
        
        print("\n📍 Games by Location:")
        location_df = analytics.games_by_location()
        
        print("\n🌤️  Weather Impact:")
        weather_df = analytics.weather_impact()
        
        print()
    
    def step5_team_balancing(self):
        """Step 5: Demonstrate team balancing"""
        print("📍 STEP 5: Team Balancing")
        print("-" * 80)
        
        balancer = TeamBalancer(self.app.spark)
        
        # Get active players
        active_players = self.players_df.filter(col("active") == True)
        active_count = active_players.count()
        
        if active_count < 10:
            print(f"⚠️  Not enough active players for balancing (need 10, have {active_count})")
            print()
            return
        
        print(f"\n✅ Found {active_count} active players")
        
        # Skill-based balancing
        print("\n⚖️  Method 1: Skill-Based Balancing")
        team_a_skill, team_b_skill = balancer.balance_teams_by_skill(active_players, team_size=5)
        balancer.display_teams(team_a_skill, team_b_skill)
        
        # Position-based balancing
        print("\n⚖️  Method 2: Position-Based Balancing")
        team_a_pos, team_b_pos = balancer.balance_teams_by_position(active_players, team_size=5)
        balancer.display_teams(team_a_pos, team_b_pos)
        
        print()
    
    def step6_data_insights(self):
        """Step 6: Generate actionable insights"""
        print("📍 STEP 6: Actionable Insights")
        print("-" * 80)
        
        # Player engagement analysis
        total_players = self.players_df.count()
        active_players = self.players_df.filter(col("active") == True).count()
        inactive_players = total_players - active_players
        
        print(f"\n📊 Player Engagement:")
        print(f"   Total Players: {total_players}")
        print(f"   Active Players: {active_players} ({active_players/total_players*100:.1f}%)")
        print(f"   Inactive Players: {inactive_players} ({inactive_players/total_players*100:.1f}%)")
        
        # Skill distribution
        print(f"\n⭐ Skill Distribution:")
        skill_dist = self.players_df.groupBy("skill_level").count().orderBy("skill_level")
        skill_dist.show()
        
        # Most active positions
        print(f"\n👥 Most Active Positions:")
        position_activity = self.players_df.groupBy("position").agg(
            {"total_games": "sum", "total_goals": "sum"}
        ).orderBy(col("sum(total_games)").desc())
        position_activity.show()
        
        # Game frequency analysis
        total_games = self.games_df.count()
        completed_games = self.games_df.filter(col("completed") == True).count()
        
        print(f"\n🏆 Game Completion:")
        print(f"   Total Games: {total_games}")
        print(f"   Completed: {completed_games} ({completed_games/total_games*100:.1f}%)")
        
        print()
    
    def step7_recommendations(self):
        """Step 7: Generate recommendations"""
        print("📍 STEP 7: Recommendations")
        print("-" * 80)
        
        print("\n💡 System Recommendations:")
        
        # Check for inactive players
        inactive_count = self.players_df.filter(col("active") == False).count()
        if inactive_count > 0:
            print(f"   • Re-engage {inactive_count} inactive players")
        
        # Check for skill imbalance
        from pyspark.sql.functions import avg, stddev
        skill_stats = self.players_df.agg(
            avg("skill_level").alias("avg_skill"),
            stddev("skill_level").alias("stddev_skill")
        ).collect()[0]
        
        print(f"   • Average skill level: {skill_stats['avg_skill']:.2f}")
        print(f"   • Skill diversity: {'Good' if skill_stats['stddev_skill'] > 2 else 'Limited'}")
        
        # Check position balance
        position_counts = self.players_df.groupBy("position").count().collect()
        positions = {row.position: row['count'] for row in position_counts}
        
        min_position = min(positions.values())
        max_position = max(positions.values())
        
        if max_position > min_position * 2:
            print(f"   • Position imbalance detected - recruit more {min(positions, key=positions.get)}s")
        
        # Game frequency
        total_games = self.games_df.count()
        total_players = self.players_df.count()
        games_per_player = total_games / total_players if total_players > 0 else 0
        
        print(f"   • Games per player: {games_per_player:.2f}")
        if games_per_player < 5:
            print(f"   • Schedule more games to increase player engagement")
        
        print()
    
    def run_complete_workflow(self):
        """Execute complete end-to-end workflow"""
        try:
            self.step1_initialize_application()
            
            if not self.step2_load_data():
                print("❌ Workflow aborted: Data not available")
                return False
            
            self.step3_basic_statistics()
            self.step4_advanced_analytics()
            self.step5_team_balancing()
            self.step6_data_insights()
            self.step7_recommendations()
            
            print("="*80)
            print("✅ END-TO-END WORKFLOW COMPLETED SUCCESSFULLY")
            print("="*80 + "\n")
            
            return True
            
        except Exception as e:
            logger.error(f"Workflow failed: {e}", exc_info=True)
            print(f"\n❌ Workflow failed: {e}\n")
            return False
        finally:
            if hasattr(self, 'app'):
                self.app.stop()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run end-to-end integration workflow")
    parser.add_argument(
        "--use-sample-data",
        action="store_true",
        default=True,
        help="Use sample data from data/sample directory"
    )
    
    args = parser.parse_args()
    
    workflow = EndToEndWorkflow(use_sample_data=args.use_sample_data)
    success = workflow.run_complete_workflow()
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
