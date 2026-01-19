"""
Pickup Soccer - Interactive Dashboard
Built with Streamlit and Plotly
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add src to path for absolute imports
project_root = os.path.abspath(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Now import with absolute imports
from main import PickupSoccerApp
from team_balancer import TeamBalancer
from config import SAMPLE_DIR
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Pickup Soccer Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_app():
    """Initialize the Pickup Soccer application"""
    return PickupSoccerApp(use_sample_data=True)

@st.cache_data
def load_players_data(_app):
    """Load players data as pandas DataFrame"""
    df = _app.players_df.toPandas() if _app.players_df else pd.DataFrame()
    return df

@st.cache_data
def load_games_data(_app):
    """Load games data as pandas DataFrame"""
    df = _app.games_df.toPandas() if _app.games_df else pd.DataFrame()
    return df

def main():
    # Header
    st.markdown('<h1 class="main-header">⚽ Pickup Soccer Dashboard</h1>', unsafe_allow_html=True)
    
    # Initialize app
    try:
        app = init_app()
        players_df = load_players_data(app)
        games_df = load_games_data(app)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Make sure sample data has been generated. Run: `python scripts/generate_data.py`")
        return
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["📊 Overview", "👥 Players", "⚽ Games", "📈 Analytics", "⚖️ Team Balancer"]
    )
    
    # Page routing
    if page == "📊 Overview":
        show_overview(players_df, games_df)
    elif page == "👥 Players":
        show_players(players_df)
    elif page == "⚽ Games":
        show_games(games_df)
    elif page == "📈 Analytics":
        show_analytics(app, players_df, games_df)
    elif page == "⚖️ Team Balancer":
        show_team_balancer(app, players_df)

def show_overview(players_df, games_df):
    """Overview dashboard"""
    st.header("Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Players", len(players_df))
    with col2:
        active_players = len(players_df[players_df['total_games'] > 0])
        st.metric("Active Players", active_players)
    with col3:
        st.metric("Total Games", len(games_df))
    with col4:
        avg_skill = players_df['skill_level'].mean()
        st.metric("Avg Skill Level", f"{avg_skill:.1f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Position Distribution")
        position_counts = players_df['position'].value_counts()
        fig = px.pie(
            values=position_counts.values,
            names=position_counts.index,
            title="Players by Position"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Skill Level Distribution")
        fig = px.histogram(
            players_df,
            x='skill_level',
            nbins=10,
            title="Skill Level Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent games
    st.subheader("Recent Games")
    if not games_df.empty:
        recent_games = games_df.sort_values('date', ascending=False).head(10)
        st.dataframe(
            recent_games[['date', 'location', 'team_a_score', 'team_b_score', 'weather']],
            use_container_width=True
        )

def show_players(players_df):
    """Players page"""
    st.header("Players")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        position_filter = st.multiselect(
            "Filter by Position",
            options=players_df['position'].unique(),
            default=players_df['position'].unique()
        )
    
    with col2:
        min_skill, max_skill = int(players_df['skill_level'].min()), int(players_df['skill_level'].max())
        skill_range = st.slider("Skill Level Range", min_skill, max_skill, (min_skill, max_skill))
    
    with col3:
        min_games = st.number_input("Min Games Played", min_value=0, value=0)
    
    # Filter data
    filtered_df = players_df[
        (players_df['position'].isin(position_filter)) &
        (players_df['skill_level'] >= skill_range[0]) &
        (players_df['skill_level'] <= skill_range[1]) &
        (players_df['total_games'] >= min_games)
    ]
    
    st.write(f"Showing {len(filtered_df)} players")
    
    # Display table
    st.dataframe(
        filtered_df[['name', 'position', 'age', 'skill_level', 'total_games', 'total_goals', 'total_assists']],
        use_container_width=True
    )
    
    # Top performers
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Scorers")
        top_scorers = filtered_df.nlargest(10, 'total_goals')
        fig = px.bar(
            top_scorers,
            x='name',
            y='total_goals',
            title="Top 10 Goal Scorers"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Assisters")
        top_assisters = filtered_df.nlargest(10, 'total_assists')
        fig = px.bar(
            top_assisters,
            x='name',
            y='total_assists',
            title="Top 10 Assist Leaders",
            color_discrete_sequence=['green']
        )
        st.plotly_chart(fig, use_container_width=True)

def show_games(games_df):
    """Games page"""
    st.header("Games")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        location_filter = st.multiselect(
            "Filter by Location",
            options=games_df['location'].unique(),
            default=games_df['location'].unique()
        )
    
    with col2:
        weather_filter = st.multiselect(
            "Filter by Weather",
            options=games_df['weather'].unique(),
            default=games_df['weather'].unique()
        )
    
    # Filter data
    filtered_games = games_df[
        (games_df['location'].isin(location_filter)) &
        (games_df['weather'].isin(weather_filter))
    ]
    
    st.write(f"Showing {len(filtered_games)} games")
    
    # Display table
    st.dataframe(
        filtered_games[['date', 'location', 'weather', 'team_a_score', 'team_b_score', 'duration']],
        use_container_width=True
    )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Games by Location")
        location_counts = filtered_games['location'].value_counts()
        fig = px.bar(
            x=location_counts.index,
            y=location_counts.values,
            labels={'x': 'Location', 'y': 'Number of Games'},
            title="Games Played by Location"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Score Distribution")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=filtered_games['team_a_score'], name='Team A', opacity=0.7))
        fig.add_trace(go.Histogram(x=filtered_games['team_b_score'], name='Team B', opacity=0.7))
        fig.update_layout(title='Score Distribution', barmode='overlay')
        st.plotly_chart(fig, use_container_width=True)

def show_analytics(app, players_df, games_df):
    """Analytics page"""
    st.header("Advanced Analytics")
    
    # Player performance
    st.subheader("Player Performance Metrics")
    
    # Goals per game
    players_df['goals_per_game'] = players_df.apply(
        lambda x: x['total_goals'] / x['total_games'] if x['total_games'] > 0 else 0,
        axis=1
    )
    players_df['assists_per_game'] = players_df.apply(
        lambda x: x['total_assists'] / x['total_games'] if x['total_games'] > 0 else 0,
        axis=1
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Goals per Game vs Skill Level")
        fig = px.scatter(
            players_df[players_df['total_games'] > 5],
            x='skill_level',
            y='goals_per_game',
            size='total_games',
            hover_data=['name', 'position'],
            title="Player Efficiency"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Performance by Position")
        position_stats = players_df.groupby('position').agg({
            'total_goals': 'mean',
            'total_assists': 'mean',
            'skill_level': 'mean'
        }).reset_index()
        
        fig = go.Figure(data=[
            go.Bar(name='Avg Goals', x=position_stats['position'], y=position_stats['total_goals']),
            go.Bar(name='Avg Assists', x=position_stats['position'], y=position_stats['total_assists'])
        ])
        fig.update_layout(title='Average Stats by Position', barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    # Game trends
    st.subheader("Game Trends")
    
    if not games_df.empty:
        games_df['total_goals'] = games_df['team_a_score'] + games_df['team_b_score']
        games_df['date'] = pd.to_datetime(games_df['date'])
        
        fig = px.line(
            games_df.sort_values('date'),
            x='date',
            y='total_goals',
            title='Goals Over Time'
        )
        st.plotly_chart(fig, use_container_width=True)

def show_team_balancer(app, players_df):
    """Team Balancer page"""
    st.header("Team Balancer")
    
    st.write("Create balanced teams based on player skills and positions")
    
    # Settings
    col1, col2 = st.columns(2)
    
    with col1:
        team_size = st.slider("Team Size", min_value=3, max_value=11, value=5)
    
    with col2:
        method = st.selectbox("Balancing Method", ["skill", "position"])
    
    # Player selection
    st.subheader("Select Players")
    
    active_players = players_df[players_df['total_games'] > 0].copy()
    selected_players = st.multiselect(
        "Choose players (leave empty for all active players)",
        options=active_players['player_id'].tolist(),
        format_func=lambda x: active_players[active_players['player_id'] == x]['name'].iloc[0]
    )
    
    if st.button("Generate Teams", type="primary"):
        try:
            with st.spinner("Balancing teams..."):
                # Get selected or all active players
                if selected_players:
                    player_ids = selected_players
                else:
                    player_ids = active_players['player_id'].tolist()
                
                # Balance teams using PySpark
                balancer = TeamBalancer(app.spark, app.players_df)
                teams = balancer.balance_teams_by_skill(team_size)
                
                if teams and len(teams) >= 2:
                    team_a, team_b = teams[0], teams[1]
                    
                    # Convert to pandas
                    team_a_pd = team_a.toPandas()
                    team_b_pd = team_b.toPandas()
                    
                    # Display teams
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🔵 Team A")
                        st.dataframe(
                            team_a_pd[['name', 'position', 'skill_level', 'age']],
                            use_container_width=True
                        )
                        avg_skill_a = team_a_pd['skill_level'].mean()
                        st.metric("Average Skill", f"{avg_skill_a:.1f}")
                    
                    with col2:
                        st.subheader("🔴 Team B")
                        st.dataframe(
                            team_b_pd[['name', 'position', 'skill_level', 'age']],
                            use_container_width=True
                        )
                        avg_skill_b = team_b_pd['skill_level'].mean()
                        st.metric("Average Skill", f"{avg_skill_b:.1f}")
                    
                    # Balance comparison
                    skill_diff = abs(avg_skill_a - avg_skill_b)
                    if skill_diff < 0.5:
                        st.success(f"✅ Teams are well balanced! (Skill difference: {skill_diff:.2f})")
                    else:
                        st.warning(f"⚠️ Skill difference: {skill_diff:.2f}")
                    
                else:
                    st.error("Not enough players to form teams")
                    
        except Exception as e:
            st.error(f"Error balancing teams: {e}")

if __name__ == "__main__":
    main()
