"""
Pickup Soccer REST API
FastAPI-based REST API for accessing player and game data
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import PickupSoccerApp
from team_balancer import TeamBalancer

# Initialize FastAPI app
app = FastAPI(
    title="Pickup Soccer API",
    description="REST API for managing pickup soccer games, players, and analytics",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Spark app
soccer_app = None

def get_app():
    """Get or create Spark application instance"""
    global soccer_app
    if soccer_app is None:
        try:
            soccer_app = PickupSoccerApp(use_sample_data=True)
        except Exception as e:
            print(f"Warning: Could not initialize Spark app: {e}")
            # Return None and handle in endpoints
            return None
    return soccer_app

@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    print("=" * 60)
    print("🚀 Pickup Soccer API Starting...")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"JAVA_HOME: {os.getenv('JAVA_HOME', 'Not set')}")
    print("=" * 60)

# Pydantic models for API responses
class Player(BaseModel):
    player_id: str
    name: str
    age: int
    position: str
    skill_level: int
    total_games: int
    total_goals: int
    total_assists: int

class Game(BaseModel):
    game_id: str
    date: str
    location: str
    weather: str
    team_a_score: int
    team_b_score: int
    duration: int

class PlayerStats(BaseModel):
    player_id: str
    name: str
    games_played: int
    goals: int
    assists: int
    goals_per_game: float
    assists_per_game: float

class TeamMember(BaseModel):
    name: str
    position: str
    skill_level: int
    age: int

class BalancedTeams(BaseModel):
    team_a: List[TeamMember]
    team_b: List[TeamMember]
    team_a_avg_skill: float
    team_b_avg_skill: float
    skill_difference: float

# API Endpoints

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve landing page"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="""
            <html>
                <head><title>Pickup Soccer API</title></head>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1>⚽ Pickup Soccer API</h1>
                    <p>Welcome to the Pickup Soccer REST API</p>
                    <p><a href="/docs">📖 View API Documentation</a></p>
                </body>
            </html>
        """)

@app.get("/api/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {"status": "healthy", "service": "pickup-soccer-api"}
    }

@app.get("/api/players", response_model=List[Player])
async def get_players(
    position: Optional[str] = Query(None, description="Filter by position"),
    min_skill: Optional[int] = Query(None, description="Minimum skill level"),
    max_skill: Optional[int] = Query(None, description="Maximum skill level"),
    limit: int = Query(100, description="Maximum number of players to return")
):
    """Get list of players with optional filters"""
    try:
        app = get_app()
        df = app.players_df
        
        # Apply filters
        if position:
            df = df.filter(df.position == position)
        if min_skill:
            df = df.filter(df.skill_level >= min_skill)
        if max_skill:
            df = df.filter(df.skill_level <= max_skill)
        
        # Convert to pandas and limit
        players = df.limit(limit).toPandas().to_dict('records')
        return players
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/players/{player_id}", response_model=Player)
async def get_player(player_id: str):
    """Get a specific player by ID"""
    try:
        app = get_app()
        player = app.players_df.filter(app.players_df.player_id == player_id).first()
        
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        
        return player.asDict()
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/games", response_model=List[Game])
async def get_games(
    location: Optional[str] = Query(None, description="Filter by location"),
    weather: Optional[str] = Query(None, description="Filter by weather"),
    limit: int = Query(50, description="Maximum number of games to return")
):
    """Get list of games with optional filters"""
    try:
        app = get_app()
        df = app.games_df
        
        # Apply filters
        if location:
            df = df.filter(df.location == location)
        if weather:
            df = df.filter(df.weather == weather)
        
        # Convert to pandas and limit
        games = df.limit(limit).toPandas().to_dict('records')
        return games
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/games/{game_id}", response_model=Game)
async def get_game(game_id: str):
    """Get a specific game by ID"""
    try:
        app = get_app()
        game = app.games_df.filter(app.games_df.game_id == game_id).first()
        
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        return game.asDict()
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/top-scorers")
async def get_top_scorers(limit: int = Query(10, description="Number of top scorers")):
    """Get top goal scorers"""
    try:
        app = get_app()
        top_scorers = (app.players_df
                      .orderBy(app.players_df.total_goals.desc())
                      .limit(limit)
                      .select('player_id', 'name', 'position', 'total_goals', 'total_games')
                      .toPandas()
                      .to_dict('records'))
        return top_scorers
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/top-assists")
async def get_top_assists(limit: int = Query(10, description="Number of top assisters")):
    """Get top assist leaders"""
    try:
        app = get_app()
        top_assists = (app.players_df
                      .orderBy(app.players_df.total_assists.desc())
                      .limit(limit)
                      .select('player_id', 'name', 'position', 'total_assists', 'total_games')
                      .toPandas()
                      .to_dict('records'))
        return top_assists
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/position-stats")
async def get_position_stats():
    """Get statistics by position"""
    try:
        app = get_app()
        from pyspark.sql.functions import avg, count
        
        stats = (app.players_df
                .groupBy('position')
                .agg(
                    count('*').alias('player_count'),
                    avg('skill_level').alias('avg_skill'),
                    avg('total_goals').alias('avg_goals'),
                    avg('total_assists').alias('avg_assists')
                )
                .toPandas()
                .to_dict('records'))
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/teams/balance", response_model=BalancedTeams)
async def balance_teams(
    team_size: int = Query(5, description="Number of players per team"),
    method: str = Query("skill", description="Balancing method: 'skill' or 'position'")
):
    """Generate balanced teams"""
    try:
        app = get_app()
        balancer = TeamBalancer(app.spark, app.players_df)
        
        if method == "skill":
            teams = balancer.balance_teams_by_skill(team_size)
        elif method == "position":
            teams = balancer.balance_teams_by_position(team_size, position="Forward")
        else:
            raise HTTPException(status_code=400, detail="Invalid method. Use 'skill' or 'position'")
        
        if not teams or len(teams) < 2:
            raise HTTPException(status_code=400, detail="Not enough players to form teams")
        
        team_a_df = teams[0].toPandas()
        team_b_df = teams[1].toPandas()
        
        return {
            "team_a": team_a_df[['name', 'position', 'skill_level', 'age']].to_dict('records'),
            "team_b": team_b_df[['name', 'position', 'skill_level', 'age']].to_dict('records'),
            "team_a_avg_skill": float(team_a_df['skill_level'].mean()),
            "team_b_avg_skill": float(team_b_df['skill_level'].mean()),
            "skill_difference": abs(float(team_a_df['skill_level'].mean() - team_b_df['skill_level'].mean()))
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats/summary")
async def get_summary_stats():
    """Get overall summary statistics"""
    try:
        app = get_app()
        
        total_players = app.players_df.count()
        total_games = app.games_df.count()
        active_players = app.players_df.filter(app.players_df.total_games > 0).count()
        
        from pyspark.sql.functions import avg
        avg_skill = app.players_df.select(avg('skill_level')).first()[0]
        avg_goals_per_game = app.games_df.select(
            avg((app.games_df.team_a_score + app.games_df.team_b_score))
        ).first()[0]
        
        return {
            "total_players": total_players,
            "active_players": active_players,
            "total_games": total_games,
            "average_skill_level": float(avg_skill) if avg_skill else 0,
            "average_goals_per_game": float(avg_goals_per_game) if avg_goals_per_game else 0
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
