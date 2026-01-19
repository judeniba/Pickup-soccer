"""
Performance benchmarking for Pickup Soccer application
"""
import sys
import os
from pathlib import Path
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import logging

from config import SPARK_CONFIG, SAMPLE_DIR
from models import PlayerSchema, GameSchema, create_player_record, create_game_record
from analytics import SoccerAnalytics
from team_balancer import TeamBalancer

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class PerformanceBenchmark:
    """Performance benchmarking suite"""
    
    def __init__(self):
        self.spark = self._create_spark_session()
        self.benchmarks = []
    
    def _create_spark_session(self) -> SparkSession:
        """Create Spark session for benchmarking"""
        builder = SparkSession.builder
        for key, value in SPARK_CONFIG.items():
            builder = builder.config(key, value)
        
        spark = builder.getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        return spark
    
    def _time_operation(self, operation_name: str, operation_func, *args, **kwargs):
        """Time an operation and record results"""
        print(f"\n⏱️  Benchmarking: {operation_name}")
        
        start_time = time.time()
        result = operation_func(*args, **kwargs)
        end_time = time.time()
        
        duration = end_time - start_time
        
        benchmark = {
            "operation": operation_name,
            "duration_seconds": duration,
            "duration_ms": duration * 1000,
            "timestamp": datetime.now()
        }
        self.benchmarks.append(benchmark)
        
        print(f"   ✅ Completed in {duration:.4f} seconds ({duration*1000:.2f} ms)")
        
        return result, duration
    
    def benchmark_data_generation(self):
        """Benchmark data generation"""
        print("\n" + "="*60)
        print("BENCHMARK: Data Generation")
        print("="*60)
        
        def generate_players(n):
            players = []
            for i in range(n):
                player = create_player_record(
                    f"BENCH_P{i:06d}",
                    f"Player {i}",
                    (i % 10) + 1
                )
                players.append(player)
            return self.spark.createDataFrame(players, PlayerSchema.get_schema())
        
        # Benchmark different sizes
        for size in [100, 500, 1000, 5000]:
            df, duration = self._time_operation(
                f"Generate {size} players",
                generate_players,
                size
            )
            print(f"   Records/second: {size/duration:.2f}")
    
    def benchmark_data_operations(self):
        """Benchmark data read/write operations"""
        print("\n" + "="*60)
        print("BENCHMARK: Data Operations")
        print("="*60)
        
        # Create test dataset
        players = []
        for i in range(10000):
            player = create_player_record(
                f"PERF_P{i:06d}",
                f"Player {i}",
                (i % 10) + 1,
                total_games=i % 100,
                total_goals=i % 50
            )
            players.append(player)
        
        players_df = self.spark.createDataFrame(players, PlayerSchema.get_schema())
        
        # Benchmark write
        test_path = str(SAMPLE_DIR / "benchmark" / "players")
        _, write_duration = self._time_operation(
            "Write 10,000 records (Parquet)",
            lambda: players_df.write.format("parquet").mode("overwrite").save(test_path)
        )
        
        # Benchmark read
        read_df, read_duration = self._time_operation(
            "Read 10,000 records (Parquet)",
            lambda: self.spark.read.format("parquet").load(test_path)
        )
        
        # Benchmark count
        _, count_duration = self._time_operation(
            "Count records",
            lambda: read_df.count()
        )
        
        # Calculate throughput
        print(f"\n   Write throughput: {10000/write_duration:.2f} records/sec")
        print(f"   Read throughput: {10000/read_duration:.2f} records/sec")
    
    def benchmark_filtering(self):
        """Benchmark filtering operations"""
        print("\n" + "="*60)
        print("BENCHMARK: Filtering Operations")
        print("="*60)
        
        # Create large dataset
        players = []
        for i in range(50000):
            player = create_player_record(
                f"FILTER_P{i:06d}",
                f"Player {i}",
                (i % 10) + 1,
                active=(i % 5 != 0)
            )
            players.append(player)
        
        players_df = self.spark.createDataFrame(players, PlayerSchema.get_schema())
        
        # Benchmark different filters
        _, duration1 = self._time_operation(
            "Filter active players (50k records)",
            lambda: players_df.filter(col("active") == True).count()
        )
        
        _, duration2 = self._time_operation(
            "Filter by skill level (50k records)",
            lambda: players_df.filter(col("skill_level") >= 7).count()
        )
        
        _, duration3 = self._time_operation(
            "Complex filter (50k records)",
            lambda: players_df.filter(
                (col("active") == True) & 
                (col("skill_level") >= 5) & 
                (col("total_games") > 10)
            ).count()
        )
    
    def benchmark_aggregations(self):
        """Benchmark aggregation operations"""
        print("\n" + "="*60)
        print("BENCHMARK: Aggregation Operations")
        print("="*60)
        
        # Create dataset with various attributes
        players = []
        positions = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
        for i in range(20000):
            player = create_player_record(
                f"AGG_P{i:06d}",
                f"Player {i}",
                (i % 10) + 1,
                position=positions[i % 4],
                total_games=i % 200,
                total_goals=i % 50,
                total_assists=i % 40
            )
            players.append(player)
        
        players_df = self.spark.createDataFrame(players, PlayerSchema.get_schema())
        
        # Benchmark different aggregations
        _, duration1 = self._time_operation(
            "GroupBy position (20k records)",
            lambda: players_df.groupBy("position").count().collect()
        )
        
        _, duration2 = self._time_operation(
            "Multiple aggregations (20k records)",
            lambda: players_df.groupBy("position").agg(
                {"skill_level": "avg", "total_goals": "sum", "total_assists": "sum"}
            ).collect()
        )
        
        _, duration3 = self._time_operation(
            "Complex analytics query (20k records)",
            lambda: players_df.filter(col("total_games") > 0).groupBy("position").agg(
                {"skill_level": "avg", "total_goals": "avg", "age": "avg"}
            ).orderBy(col("avg(skill_level)").desc()).collect()
        )
    
    def benchmark_team_balancing(self):
        """Benchmark team balancing algorithms"""
        print("\n" + "="*60)
        print("BENCHMARK: Team Balancing")
        print("="*60)
        
        balancer = TeamBalancer(self.spark)
        
        # Test different player pool sizes
        for pool_size in [20, 50, 100, 200]:
            players = []
            positions = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
            for i in range(pool_size):
                player = create_player_record(
                    f"TEAM_P{i:06d}",
                    f"Player {i}",
                    (i % 10) + 1,
                    position=positions[i % 4]
                )
                players.append(player)
            
            players_df = self.spark.createDataFrame(players, PlayerSchema.get_schema())
            
            # Benchmark skill-based balancing
            _, duration = self._time_operation(
                f"Skill-based balancing ({pool_size} players)",
                lambda: balancer.balance_teams_by_skill(players_df, team_size=5)
            )
    
    def benchmark_analytics(self):
        """Benchmark analytics operations"""
        print("\n" + "="*60)
        print("BENCHMARK: Analytics Operations")
        print("="*60)
        
        # Create comprehensive dataset
        players = []
        for i in range(10000):
            player = create_player_record(
                f"ANALYTICS_P{i:06d}",
                f"Player {i}",
                (i % 10) + 1,
                position=["Goalkeeper", "Defender", "Midfielder", "Forward"][i % 4],
                total_games=i % 200 + 1,
                total_goals=i % 50,
                total_assists=i % 40,
                age=18 + (i % 27)
            )
            players.append(player)
        
        players_df = self.spark.createDataFrame(players, PlayerSchema.get_schema())
        
        # Save to temp location
        temp_path = str(SAMPLE_DIR / "benchmark_analytics")
        players_path = f"{temp_path}/players"
        players_df.write.format("parquet").mode("overwrite").save(players_path)
        
        # Create games
        games = []
        for i in range(1000):
            game = create_game_record(
                f"ANALYTICS_G{i:06d}",
                [f"ANALYTICS_P{j:06d}" for j in range(i*5, i*5+5)],
                [f"ANALYTICS_P{j:06d}" for j in range(i*5+5, i*5+10)],
                location=["Field A", "Field B", "Field C"][i % 3],
                weather=["Clear", "Cloudy", "Rain"][i % 3],
                team_a_score=i % 5,
                team_b_score=(i + 1) % 5
            )
            games.append(game)
        
        games_df = self.spark.createDataFrame(games, GameSchema.get_schema())
        games_path = f"{temp_path}/games"
        games_df.write.format("parquet").mode("overwrite").save(games_path)
        
        # Benchmark analytics
        analytics = SoccerAnalytics(self.spark)
        analytics.load_data(temp_path)
        
        _, duration1 = self._time_operation(
            "Player performance analysis (10k players)",
            lambda: analytics.player_performance_analysis()
        )
        
        _, duration2 = self._time_operation(
            "Position distribution (10k players)",
            lambda: analytics.position_distribution()
        )
        
        _, duration3 = self._time_operation(
            "Game statistics (1k games)",
            lambda: analytics.game_statistics()
        )
        
        _, duration4 = self._time_operation(
            "Games by location (1k games)",
            lambda: analytics.games_by_location()
        )
    
    def print_summary(self):
        """Print benchmark summary"""
        print("\n" + "="*80)
        print("PERFORMANCE BENCHMARK SUMMARY")
        print("="*80)
        
        print(f"\nTotal Operations Benchmarked: {len(self.benchmarks)}")
        
        # Calculate statistics
        durations = [b["duration_seconds"] for b in self.benchmarks]
        total_time = sum(durations)
        avg_time = total_time / len(durations) if durations else 0
        min_time = min(durations) if durations else 0
        max_time = max(durations) if durations else 0
        
        print(f"\nTotal Execution Time: {total_time:.4f} seconds")
        print(f"Average Operation Time: {avg_time:.4f} seconds")
        print(f"Fastest Operation: {min_time:.4f} seconds")
        print(f"Slowest Operation: {max_time:.4f} seconds")
        
        # Show top 5 slowest operations
        print("\n🐌 Top 5 Slowest Operations:")
        sorted_benchmarks = sorted(self.benchmarks, key=lambda x: x["duration_seconds"], reverse=True)
        for i, bench in enumerate(sorted_benchmarks[:5], 1):
            print(f"  {i}. {bench['operation']}: {bench['duration_seconds']:.4f}s ({bench['duration_ms']:.2f}ms)")
        
        # Show top 5 fastest operations
        print("\n⚡ Top 5 Fastest Operations:")
        for i, bench in enumerate(sorted_benchmarks[-5:][::-1], 1):
            print(f"  {i}. {bench['operation']}: {bench['duration_seconds']:.4f}s ({bench['duration_ms']:.2f}ms)")
        
        print("\n" + "="*80)
        print("✅ BENCHMARK COMPLETE")
        print("="*80 + "\n")
    
    def run_all_benchmarks(self):
        """Run complete benchmark suite"""
        print("\n" + "="*80)
        print("RUNNING PERFORMANCE BENCHMARK SUITE")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        start_total = time.time()
        
        self.benchmark_data_generation()
        self.benchmark_data_operations()
        self.benchmark_filtering()
        self.benchmark_aggregations()
        self.benchmark_team_balancing()
        self.benchmark_analytics()
        
        total_duration = time.time() - start_total
        print(f"\n⏱️  Total benchmark time: {total_duration:.2f} seconds")
        
        self.print_summary()
    
    def cleanup(self):
        """Clean up resources"""
        self.spark.stop()


def main():
    """Run performance benchmarks"""
    benchmark = PerformanceBenchmark()
    
    try:
        benchmark.run_all_benchmarks()
    except Exception as e:
        logger.error(f"Benchmark failed: {e}", exc_info=True)
        return 1
    finally:
        benchmark.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
