"""
Integration tests for Pickup Soccer application
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pyspark.sql import SparkSession
from datetime import datetime
import logging

from config import SPARK_CONFIG, SAMPLE_DIR
from models import PlayerSchema, GameSchema, create_player_record, create_game_record
from main import PickupSoccerApp
from analytics import SoccerAnalytics
from team_balancer import TeamBalancer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IntegrationTest:
    """Integration test suite for all components"""
    
    def __init__(self):
        self.spark = self._create_spark_session()
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    def _create_spark_session(self) -> SparkSession:
        """Create Spark session for testing"""
        builder = SparkSession.builder
        for key, value in SPARK_CONFIG.items():
            builder = builder.config(key, value)
        
        spark = builder.getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        return spark
    
    def _log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        self.total_tests += 1
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            "test": test_name,
            "passed": passed,
            "message": message,
            "timestamp": datetime.now()
        }
        self.test_results.append(result)
        
        if passed:
            self.passed_tests += 1
            logger.info(f"{status}: {test_name}")
        else:
            self.failed_tests += 1
            logger.error(f"{status}: {test_name} - {message}")
        
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
    
    def test_data_models(self):
        """Test data model schemas"""
        print("\n" + "="*60)
        print("TEST SUITE: Data Models")
        print("="*60)
        
        try:
            # Test PlayerSchema
            player_schema = PlayerSchema.get_schema()
            assert len(player_schema.fields) == 14
            self._log_test("PlayerSchema creation", True)
        except Exception as e:
            self._log_test("PlayerSchema creation", False, str(e))
        
        try:
            # Test GameSchema
            game_schema = GameSchema.get_schema()
            assert len(game_schema.fields) == 11
            self._log_test("GameSchema creation", True)
        except Exception as e:
            self._log_test("GameSchema creation", False, str(e))
        
        try:
            # Test creating player record
            player = create_player_record("P001", "Test Player", 5)
            assert player["player_id"] == "P001"
            assert player["name"] == "Test Player"
            assert player["skill_level"] == 5
            self._log_test("Create player record", True)
        except Exception as e:
            self._log_test("Create player record", False, str(e))
        
        try:
            # Test creating game record
            game = create_game_record("G001", ["P1", "P2"], ["P3", "P4"])
            assert game["game_id"] == "G001"
            assert len(game["team_a_players"]) == 2
            assert len(game["team_b_players"]) == 2
            self._log_test("Create game record", True)
        except Exception as e:
            self._log_test("Create game record", False, str(e))
    
    def test_sample_data_creation(self):
        """Test sample data generation"""
        print("\n" + "="*60)
        print("TEST SUITE: Sample Data Generation")
        print("="*60)
        
        try:
            # Create sample players
            players = []
            for i in range(20):
                player = create_player_record(
                    f"TEST_P{i:03d}",
                    f"Test Player {i}",
                    (i % 10) + 1
                )
                players.append(player)
            
            players_df = self.spark.createDataFrame(players, PlayerSchema.get_schema())
            assert players_df.count() == 20
            self._log_test("Generate sample players", True, f"Created {players_df.count()} players")
        except Exception as e:
            self._log_test("Generate sample players", False, str(e))
        
        try:
            # Create sample games
            games = []
            for i in range(10):
                game = create_game_record(
                    f"TEST_G{i:03d}",
                    [f"TEST_P{i:03d}", f"TEST_P{i+1:03d}"],
                    [f"TEST_P{i+2:03d}", f"TEST_P{i+3:03d}"],
                    team_a_score=i % 5,
                    team_b_score=(i + 1) % 5
                )
                games.append(game)
            
            games_df = self.spark.createDataFrame(games, GameSchema.get_schema())
            assert games_df.count() == 10
            self._log_test("Generate sample games", True, f"Created {games_df.count()} games")
        except Exception as e:
            self._log_test("Generate sample games", False, str(e))
    
    def test_main_application(self):
        """Test main application functionality"""
        print("\n" + "="*60)
        print("TEST SUITE: Main Application")
        print("="*60)
        
        try:
            app = PickupSoccerApp()
            self._log_test("Initialize PickupSoccerApp", True)
            
            # Test loading players (may be empty)
            players_df = app.load_players()
            self._log_test("Load players", True, f"Loaded {players_df.count()} players")
            
            # Test loading games (may be empty)
            games_df = app.load_games()
            self._log_test("Load games", True, f"Loaded {games_df.count()} games")
            
        except Exception as e:
            self._log_test("Main application tests", False, str(e))
    
    def test_team_balancer(self):
        """Test team balancing functionality"""
        print("\n" + "="*60)
        print("TEST SUITE: Team Balancer")
        print("="*60)
        
        try:
            # Create test players
            players = []
            for i in range(10):
                player = create_player_record(
                    f"BALANCE_P{i:03d}",
                    f"Player {i}",
                    (i % 10) + 1,
                    position=["Goalkeeper", "Defender", "Midfielder", "Forward"][i % 4]
                )
                players.append(player)
            
            players_df = self.spark.createDataFrame(players, PlayerSchema.get_schema())
            balancer = TeamBalancer(self.spark)
            
            # Test skill-based balancing
            team_a, team_b = balancer.balance_teams_by_skill(players_df, team_size=5)
            assert team_a.count() == 5
            assert team_b.count() == 5
            self._log_test("Skill-based team balancing", True, f"Teams: {team_a.count()} vs {team_b.count()}")
            
            # Test position-based balancing
            team_a, team_b = balancer.balance_teams_by_position(players_df, team_size=5)
            assert team_a.count() == 5
            assert team_b.count() == 5
            self._log_test("Position-based team balancing", True, f"Teams: {team_a.count()} vs {team_b.count()}")
            
            # Test team stats calculation
            stats = balancer.get_team_stats(team_a)
            assert "avg_skill" in stats
            assert "total_skill" in stats
            self._log_test("Team statistics calculation", True)
            
        except Exception as e:
            self._log_test("Team balancer tests", False, str(e))
    
    def test_analytics(self):
        """Test analytics functionality"""
        print("\n" + "="*60)
        print("TEST SUITE: Analytics Engine")
        print("="*60)
        
        try:
            # Create test data
            players = []
            for i in range(50):
                player = create_player_record(
                    f"ANALYTICS_P{i:03d}",
                    f"Player {i}",
                    (i % 10) + 1,
                    position=["Goalkeeper", "Defender", "Midfielder", "Forward"][i % 4],
                    total_games=i + 5,
                    total_goals=i % 15,
                    total_assists=i % 10
                )
                players.append(player)
            
            players_df = self.spark.createDataFrame(players, PlayerSchema.get_schema())
            
            # Save to temp location
            temp_path = str(SAMPLE_DIR / "test_data")
            players_path = f"{temp_path}/players"
            players_df.write.format("parquet").mode("overwrite").save(players_path)
            
            # Create games
            games = []
            for i in range(20):
                game = create_game_record(
                    f"ANALYTICS_G{i:03d}",
                    [f"ANALYTICS_P{j:03d}" for j in range(i, i+5)],
                    [f"ANALYTICS_P{j:03d}" for j in range(i+5, i+10)],
                    location=["Field A", "Field B", "Field C"][i % 3],
                    weather=["Clear", "Cloudy", "Rain"][i % 3],
                    team_a_score=i % 5,
                    team_b_score=(i + 1) % 5
                )
                games.append(game)
            
            games_df = self.spark.createDataFrame(games, GameSchema.get_schema())
            games_path = f"{temp_path}/games"
            games_df.write.format("parquet").mode("overwrite").save(games_path)
            
            # Test analytics
            analytics = SoccerAnalytics(self.spark)
            analytics.load_data(temp_path)
            
            # Test various analytics functions
            perf_df = analytics.player_performance_analysis()
            assert perf_df.count() > 0
            self._log_test("Player performance analysis", True, f"Analyzed {perf_df.count()} players")
            
            pos_df = analytics.position_distribution()
            assert pos_df.count() > 0
            self._log_test("Position distribution", True, f"Found {pos_df.count()} positions")
            
            top_df = analytics.top_performers("goals", 10)
            assert top_df.count() <= 10
            self._log_test("Top performers analysis", True, f"Found {top_df.count()} top scorers")
            
            game_stats = analytics.game_statistics()
            assert game_stats.count() == 1
            self._log_test("Game statistics", True)
            
            location_df = analytics.games_by_location()
            assert location_df.count() > 0
            self._log_test("Games by location", True, f"Analyzed {location_df.count()} locations")
            
        except Exception as e:
            self._log_test("Analytics tests", False, str(e))
    
    def test_data_persistence(self):
        """Test data saving and loading"""
        print("\n" + "="*60)
        print("TEST SUITE: Data Persistence")
        print("="*60)
        
        try:
            # Create test data
            players = [create_player_record(f"PERSIST_P{i}", f"Player {i}", i % 10 + 1) for i in range(10)]
            players_df = self.spark.createDataFrame(players, PlayerSchema.get_schema())
            
            # Save data
            test_path = str(SAMPLE_DIR / "test_persistence" / "players")
            players_df.write.format("parquet").mode("overwrite").save(test_path)
            self._log_test("Save player data", True, f"Saved to {test_path}")
            
            # Load data back
            loaded_df = self.spark.read.format("parquet").load(test_path)
            assert loaded_df.count() == 10
            self._log_test("Load player data", True, f"Loaded {loaded_df.count()} records")
            
            # Verify data integrity
            original_ids = set(p["player_id"] for p in players)
            loaded_ids = set(row.player_id for row in loaded_df.collect())
            assert original_ids == loaded_ids
            self._log_test("Data integrity check", True, "All records match")
            
        except Exception as e:
            self._log_test("Data persistence tests", False, str(e))
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print("INTEGRATION TEST SUMMARY")
        print("="*80)
        
        print(f"\nTotal Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"\nSuccess Rate: {success_rate:.1f}%")
        
        if self.failed_tests > 0:
            print("\n⚠️  FAILED TESTS:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        print("\n" + "="*80)
        
        if self.failed_tests == 0:
            print("✅ ALL TESTS PASSED!")
        else:
            print("⚠️  SOME TESTS FAILED - Review required")
        print("="*80 + "\n")
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("\n" + "="*80)
        print("RUNNING INTEGRATION TEST SUITE")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        self.test_data_models()
        self.test_sample_data_creation()
        self.test_main_application()
        self.test_team_balancer()
        self.test_analytics()
        self.test_data_persistence()
        
        self.print_summary()
        
        return self.failed_tests == 0
    
    def cleanup(self):
        """Clean up resources"""
        self.spark.stop()


def main():
    """Run integration tests"""
    test_suite = IntegrationTest()
    
    try:
        success = test_suite.run_all_tests()
        exit_code = 0 if success else 1
    except Exception as e:
        logger.error(f"Test suite failed with error: {e}", exc_info=True)
        exit_code = 2
    finally:
        test_suite.cleanup()
    
    return exit_code


if __name__ == "__main__":
    exit(main())
