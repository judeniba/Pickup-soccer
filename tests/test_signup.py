"""
Tests for user signup and nearby games functionality
"""
import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import haversine_distance


class TestSignupFunctionality(unittest.TestCase):
    """Test cases for signup and nearby games features"""
    
    def test_haversine_distance_same_location(self):
        """Test distance calculation for same location"""
        lat, lon = 37.7749, -122.4194
        distance = haversine_distance(lat, lon, lat, lon)
        self.assertAlmostEqual(distance, 0.0, places=2)
    
    def test_haversine_distance_known_distance(self):
        """Test distance calculation between San Francisco and San Jose"""
        # San Francisco coordinates
        sf_lat, sf_lon = 37.7749, -122.4194
        # San Jose coordinates (approximately 68 km away)
        sj_lat, sj_lon = 37.3382, -121.8863
        
        distance = haversine_distance(sf_lat, sf_lon, sj_lat, sj_lon)
        
        # Distance should be approximately 68 km
        self.assertGreater(distance, 60)
        self.assertLess(distance, 75)
    
    def test_haversine_distance_different_hemispheres(self):
        """Test distance calculation across hemispheres"""
        # New York
        ny_lat, ny_lon = 40.7128, -74.0060
        # Tokyo
        tokyo_lat, tokyo_lon = 35.6762, 139.6503
        
        distance = haversine_distance(ny_lat, ny_lon, tokyo_lat, tokyo_lon)
        
        # Distance should be approximately 10,850 km
        self.assertGreater(distance, 10000)
        self.assertLess(distance, 11500)
    
    def test_haversine_distance_negative_coordinates(self):
        """Test distance calculation with negative coordinates"""
        lat1, lon1 = -33.8688, 151.2093  # Sydney
        lat2, lon2 = -37.8136, 144.9631  # Melbourne
        
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        
        # Distance should be approximately 713 km
        self.assertGreater(distance, 700)
        self.assertLess(distance, 750)
    
    def test_player_record_with_location(self):
        """Test creating player record with location data"""
        from models import create_player_record
        from datetime import datetime
        
        player = create_player_record(
            player_id="TEST001",
            name="Test Player",
            skill_level=7,
            position="Midfielder",
            email="test@example.com",
            latitude=37.7749,
            longitude=-122.4194,
            age=25,
            joined_date=datetime.now()
        )
        
        self.assertEqual(player["player_id"], "TEST001")
        self.assertEqual(player["name"], "Test Player")
        self.assertEqual(player["latitude"], 37.7749)
        self.assertEqual(player["longitude"], -122.4194)
        self.assertEqual(player["position"], "Midfielder")
    
    def test_game_record_with_location(self):
        """Test creating game record with location data"""
        from models import create_game_record
        from datetime import datetime
        
        game = create_game_record(
            game_id="GAME001",
            team_a_players=["P1", "P2", "P3"],
            team_b_players=["P4", "P5", "P6"],
            location="Main Field",
            latitude=37.7749,
            longitude=-122.4194,
            date=datetime.now()
        )
        
        self.assertEqual(game["game_id"], "GAME001")
        self.assertEqual(game["location"], "Main Field")
        self.assertEqual(game["latitude"], 37.7749)
        self.assertEqual(game["longitude"], -122.4194)


class TestLocationFiltering(unittest.TestCase):
    """Test cases for filtering games by location"""
    
    def test_nearby_games_filtering(self):
        """Test filtering games within radius"""
        from models import create_game_record
        from datetime import datetime
        
        user_lat, user_lon = 37.7749, -122.4194
        radius_km = 10
        
        # Create test games at various distances
        games = [
            create_game_record(
                game_id="G1",
                team_a_players=["P1"],
                team_b_players=["P2"],
                location="Near Field",
                latitude=37.7749,  # Same location (0 km)
                longitude=-122.4194,
                date=datetime.now()
            ),
            create_game_record(
                game_id="G2",
                team_a_players=["P1"],
                team_b_players=["P2"],
                location="Far Field",
                latitude=37.8744,  # ~11 km away
                longitude=-122.2590,
                date=datetime.now()
            ),
            create_game_record(
                game_id="G3",
                team_a_players=["P1"],
                team_b_players=["P2"],
                location="Medium Field",
                latitude=37.7577,  # ~8 km away
                longitude=-122.5076,
                date=datetime.now()
            ),
        ]
        
        # Filter games within radius
        nearby_games = []
        for game in games:
            if game["latitude"] and game["longitude"]:
                distance = haversine_distance(
                    user_lat, user_lon,
                    game["latitude"], game["longitude"]
                )
                if distance <= radius_km:
                    nearby_games.append((game["game_id"], distance))
        
        # Should find G1 (0 km) and G3 (~8 km), but not G2 (~11 km)
        self.assertEqual(len(nearby_games), 2)
        game_ids = [g[0] for g in nearby_games]
        self.assertIn("G1", game_ids)
        self.assertIn("G3", game_ids)
        self.assertNotIn("G2", game_ids)


if __name__ == '__main__':
    unittest.main()
