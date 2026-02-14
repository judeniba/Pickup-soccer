# User Signup and Nearby Games Feature

## Overview
This feature allows users to sign up for the Pickup Soccer platform and immediately see available games in their vicinity based on their location.

## New Features

### 1. User Signup
- **Endpoint**: `POST /api/users/signup`
- **UI**: `/signup.html`
- Users can register by providing:
  - Name
  - Email
  - Age
  - Skill level (1-10)
  - Position (Goalkeeper, Defender, Midfielder, Forward)
  - Preferred foot
  - Location (latitude/longitude)

### 2. Nearby Games Discovery
- **Endpoint**: `GET /api/games/nearby`
- Upon signup, users automatically receive a list of games within their vicinity (default: 20km radius)
- Games are sorted by distance, showing the closest games first
- Each game entry shows:
  - Location name
  - Distance in kilometers
  - Date and time
  - Score
  - Weather conditions

### 3. Geolocation Support
- Signup page includes a "Use My Current Location" button
- Automatically detects user's current coordinates using browser geolocation API
- Manual coordinate entry is also supported

## API Endpoints

### Signup Endpoint
```
POST /api/users/signup
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 25,
  "skill_level": 7,
  "position": "Midfielder",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "preferred_foot": "Right"
}
```

**Response:**
```json
{
  "player_id": "P690b69b7",
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Welcome John Doe! You have been successfully registered.",
  "nearby_games": [
    {
      "game_id": "G1f17af9c",
      "date": "2026-01-15 04:44:50.131874",
      "location": "West Ground",
      "latitude": 37.7577,
      "longitude": -122.5076,
      "distance_km": 7.99,
      "weather": "Cloudy",
      "team_a_score": 4,
      "team_b_score": 0
    }
  ]
}
```

### Nearby Games Endpoint
```
GET /api/games/nearby?latitude=37.7749&longitude=-122.4194&radius_km=20&limit=10
```

**Response:**
```json
{
  "count": 28,
  "games": [
    {
      "game_id": "G1de77414",
      "date": "2025-03-02 04:44:50.131860",
      "location": "Main Field",
      "latitude": 37.7749,
      "longitude": -122.4194,
      "distance_km": 0.0,
      "weather": "Sunny",
      "team_a_score": 6,
      "team_b_score": 1
    }
  ]
}
```

## Schema Changes

### Player Schema
Added fields:
- `latitude` (DoubleType, nullable): Player's location latitude
- `longitude` (DoubleType, nullable): Player's location longitude

### Game Schema
Added fields:
- `latitude` (DoubleType, nullable): Game venue latitude
- `longitude` (DoubleType, nullable): Game venue longitude

## Usage

### Accessing the Signup Page
1. Start the API server: `uvicorn api:app --host 0.0.0.0 --port 8000`
2. Navigate to: `http://localhost:8000/signup.html`
3. Fill in your information
4. Click "Use My Current Location" or manually enter coordinates
5. Click "Sign Up"
6. View nearby games displayed on the same page

### Using the API Directly
```python
import requests

# Signup
response = requests.post('http://localhost:8000/api/users/signup', json={
    "name": "Jane Smith",
    "email": "jane@example.com",
    "age": 28,
    "skill_level": 8,
    "position": "Forward",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "preferred_foot": "Right"
})

data = response.json()
print(f"Player ID: {data['player_id']}")
print(f"Nearby games: {len(data['nearby_games'])}")

# Get nearby games later
response = requests.get('http://localhost:8000/api/games/nearby', params={
    "latitude": 37.7749,
    "longitude": -122.4194,
    "radius_km": 15,
    "limit": 5
})

games = response.json()
print(f"Found {games['count']} games within 15km")
```

## Distance Calculation
The system uses the Haversine formula to calculate great-circle distances between two points on Earth specified by latitude and longitude. This provides accurate distance calculations for finding nearby games.

## Data Generation
Sample data now includes location coordinates:
- Players: Random coordinates within ~20km of San Francisco (37.7749, -122.4194)
- Games: Fixed coordinates for predefined venues:
  - Main Field: (37.7749, -122.4194)
  - North Park: (37.8044, -122.2712)
  - South Stadium: (37.7089, -122.4621)
  - East Arena: (37.7833, -122.2167)
  - West Ground: (37.7577, -122.5076)

To regenerate sample data with location coordinates:
```bash
python scripts/generate_data.py
```

## Testing
New test suite in `tests/test_signup.py` includes:
- Distance calculation tests (Haversine formula)
- Player/game record creation with location
- Nearby games filtering logic

Run tests:
```bash
python tests/test_signup.py
```

## Screenshots

### Signup Page
![Signup Form](https://github.com/user-attachments/assets/8af03fbc-a320-4c7c-a9b5-2d893b70f836)

### Nearby Games Display
![Nearby Games](https://github.com/user-attachments/assets/5de36fa1-e409-41e6-be9e-83f900c2fcc6)

## Future Enhancements
- User authentication and session management
- Save user preferences and favorite locations
- Real-time game updates
- Push notifications for new games
- Map visualization of nearby games
- Filter games by date, skill level, or position needs
