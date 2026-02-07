"""
Data models and schemas for Pickup Soccer application
"""
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, 
    DoubleType, TimestampType, BooleanType, ArrayType
)
from datetime import datetime
from typing import Dict, Any


class PlayerSchema:
    """Schema for player data"""
    
    @staticmethod
    def get_schema() -> StructType:
        return StructType([
            StructField("player_id", StringType(), False),
            StructField("name", StringType(), False),
            StructField("email", StringType(), True),
            StructField("skill_level", IntegerType(), False),
            StructField("position", StringType(), True),
            StructField("preferred_foot", StringType(), True),
            StructField("age", IntegerType(), True),
            StructField("height_cm", IntegerType(), True),
            StructField("weight_kg", IntegerType(), True),
            StructField("active", BooleanType(), False),
            StructField("joined_date", TimestampType(), False),
            StructField("total_games", IntegerType(), False),
            StructField("total_goals", IntegerType(), False),
            StructField("total_assists", IntegerType(), False)
        ])


class CoachSchema:
    """Schema for coach data"""
    
    @staticmethod
    def get_schema() -> StructType:
        return StructType([
            StructField("coach_id", StringType(), False),
            StructField("name", StringType(), False),
            StructField("email", StringType(), True),
            StructField("phone", StringType(), True),
            StructField("specialization", StringType(), True),
            StructField("years_experience", IntegerType(), True),
            StructField("active", BooleanType(), False)
        ])


class RefereeSchema:
    """Schema for referee data"""
    
    @staticmethod
    def get_schema() -> StructType:
        return StructType([
            StructField("referee_id", StringType(), False),
            StructField("name", StringType(), False),
            StructField("email", StringType(), True),
            StructField("phone", StringType(), True),
            StructField("certification_level", StringType(), True),
            StructField("years_experience", IntegerType(), True),
            StructField("active", BooleanType(), False)
        ])


class GameSchema:
    """Schema for game data"""
    
    @staticmethod
    def get_schema() -> StructType:
        return StructType([
            StructField("game_id", StringType(), False),
            StructField("date", TimestampType(), False),
            StructField("location", StringType(), False),
            StructField("team_a_players", ArrayType(StringType()), False),
            StructField("team_b_players", ArrayType(StringType()), False),
            StructField("coach_a_id", StringType(), True),
            StructField("coach_b_id", StringType(), True),
            StructField("referee_ids", ArrayType(StringType()), False),
            StructField("referee_payment_amount", DoubleType(), True),
            StructField("team_a_score", IntegerType(), False),
            StructField("team_b_score", IntegerType(), False),
            StructField("duration_minutes", IntegerType(), False),
            StructField("weather", StringType(), True),
            StructField("field_condition", StringType(), True),
            StructField("completed", BooleanType(), False)
        ])


class PlayerStatsSchema:
    """Schema for player statistics"""
    
    @staticmethod
    def get_schema() -> StructType:
        return StructType([
            StructField("player_id", StringType(), False),
            StructField("game_id", StringType(), False),
            StructField("goals", IntegerType(), False),
            StructField("assists", IntegerType(), False),
            StructField("shots", IntegerType(), False),
            StructField("passes_completed", IntegerType(), False),
            StructField("passes_attempted", IntegerType(), False),
            StructField("tackles", IntegerType(), False),
            StructField("interceptions", IntegerType(), False),
            StructField("fouls", IntegerType(), False),
            StructField("yellow_cards", IntegerType(), False),
            StructField("red_cards", IntegerType(), False),
            StructField("minutes_played", IntegerType(), False),
            StructField("man_of_match", BooleanType(), False)
        ])


class TeamSchema:
    """Schema for team data"""
    
    @staticmethod
    def get_schema() -> StructType:
        return StructType([
            StructField("team_id", StringType(), False),
            StructField("team_name", StringType(), False),
            StructField("players", ArrayType(StringType()), False),
            StructField("avg_skill_level", DoubleType(), False),
            StructField("formation", StringType(), True),
            StructField("created_date", TimestampType(), False)
        ])


# Helper functions for creating sample records
def create_player_record(
    player_id: str,
    name: str,
    skill_level: int,
    position: str = "Midfielder",
    email: str = None,
    **kwargs
) -> Dict[str, Any]:
    """Create a player record dictionary"""
    return {
        "player_id": player_id,
        "name": name,
        "email": email or f"{name.lower().replace(' ', '.')}@example.com",
        "skill_level": skill_level,
        "position": position,
        "preferred_foot": kwargs.get("preferred_foot", "Right"),
        "age": kwargs.get("age", 25),
        "height_cm": kwargs.get("height_cm", 175),
        "weight_kg": kwargs.get("weight_kg", 70),
        "active": kwargs.get("active", True),
        "joined_date": kwargs.get("joined_date", datetime.now()),
        "total_games": kwargs.get("total_games", 0),
        "total_goals": kwargs.get("total_goals", 0),
        "total_assists": kwargs.get("total_assists", 0)
    }


def create_coach_record(
    coach_id: str,
    name: str,
    email: str = None,
    **kwargs
) -> Dict[str, Any]:
    """Create a coach record dictionary"""
    return {
        "coach_id": coach_id,
        "name": name,
        "email": email or f"{name.lower().replace(' ', '.')}@coach.example.com",
        "phone": kwargs.get("phone", None),
        "specialization": kwargs.get("specialization", "General"),
        "years_experience": kwargs.get("years_experience", 5),
        "active": kwargs.get("active", True)
    }


def create_referee_record(
    referee_id: str,
    name: str,
    email: str = None,
    **kwargs
) -> Dict[str, Any]:
    """Create a referee record dictionary"""
    return {
        "referee_id": referee_id,
        "name": name,
        "email": email or f"{name.lower().replace(' ', '.')}@referee.example.com",
        "phone": kwargs.get("phone", None),
        "certification_level": kwargs.get("certification_level", "Regional"),
        "years_experience": kwargs.get("years_experience", 3),
        "active": kwargs.get("active", True)
    }


def create_game_record(
    game_id: str,
    team_a_players: list,
    team_b_players: list,
    location: str = "Main Field",
    **kwargs
) -> Dict[str, Any]:
    """Create a game record dictionary"""
    return {
        "game_id": game_id,
        "date": kwargs.get("date", datetime.now()),
        "location": location,
        "team_a_players": team_a_players,
        "team_b_players": team_b_players,
        "coach_a_id": kwargs.get("coach_a_id", None),
        "coach_b_id": kwargs.get("coach_b_id", None),
        "referee_ids": kwargs.get("referee_ids", []),
        "referee_payment_amount": kwargs.get("referee_payment_amount", 50.0),
        "team_a_score": kwargs.get("team_a_score", 0),
        "team_b_score": kwargs.get("team_b_score", 0),
        "duration_minutes": kwargs.get("duration_minutes", 90),
        "weather": kwargs.get("weather", "Clear"),
        "field_condition": kwargs.get("field_condition", "Good"),
        "completed": kwargs.get("completed", False)
    }
