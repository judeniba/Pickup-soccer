"""
Utility functions for testing
Shared test utilities to avoid code duplication
"""
from pyspark.sql import SparkSession
from typing import Dict


def create_test_spark_session(app_name: str = "TestSession") -> SparkSession:
    """Create a standardized Spark session for testing"""
    spark = SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "2") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.memory", "512m") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def assert_dataframe_not_empty(df, message: str = "DataFrame should not be empty"):
    """Assert that a DataFrame is not empty"""
    assert df is not None, f"{message}: DataFrame is None"
    count = df.count()
    assert count > 0, f"{message}: DataFrame has {count} rows"


def assert_dataframe_has_columns(df, required_columns: list, message: str = ""):
    """Assert that DataFrame has required columns"""
    actual_columns = set(df.columns)
    required_set = set(required_columns)
    missing = required_set - actual_columns
    
    assert not missing, f"{message} Missing columns: {missing}"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero"""
    return numerator / denominator if denominator != 0 else default


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string"""
    if seconds < 1:
        return f"{seconds*1000:.2f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds / 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.2f}s"
