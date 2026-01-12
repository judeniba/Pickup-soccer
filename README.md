# Pickup Soccer ⚽

A web application for organizing and joining pickup soccer games in your area. Create games, see available matches, join or leave games, and coordinate with other players.

## Features

- 🎮 **Create Games**: Set up new pickup soccer games with location, date, time, and player limits
- 👥 **Join Games**: Browse available games and join with just your name
- 📊 **Real-time Updates**: See current player count and game status
- 🎯 **Simple Interface**: Clean, intuitive UI with responsive design
- 🔄 **Auto-refresh**: Games list automatically updates every 30 seconds

## Getting Started

### Prerequisites

- Node.js (version 12 or higher)
- npm (comes with Node.js)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/judeniba/Pickup-soccer.git
cd Pickup-soccer
```

2. Install dependencies:
```bash
npm install
```

3. Start the server:
```bash
npm start
```

4. Open your browser and navigate to:
```
http://localhost:3000
```

## Usage

### Creating a Game

1. Fill in the game details in the "Create a New Game" form:
   - Location (e.g., "Central Park Field 3")
   - Date
   - Time
   - Maximum number of players (default: 10)

2. Click "Create Game" to add it to the list

### Joining a Game

1. Browse the "Available Games" section
2. Enter your name in the text field for the game you want to join
3. Click "Join Game"
4. Your name will appear in the players list

### Leaving a Game

1. Click the "Leave Game" button on any game
2. Enter your name when prompted
3. You'll be removed from the players list

## API Endpoints

The application provides a RESTful API:

- `GET /api/games` - Get all games
- `POST /api/games` - Create a new game
- `POST /api/games/:id/join` - Join a game
- `DELETE /api/games/:id/leave` - Leave a game

## Project Structure

```
Pickup-soccer/
├── public/           # Frontend files
│   ├── index.html   # Main HTML page
│   ├── styles.css   # CSS styling
│   └── app.js       # Frontend JavaScript
├── server.js        # Express server and API
├── package.json     # Dependencies and scripts
└── README.md        # Documentation
```

## Technology Stack

- **Backend**: Node.js, Express.js
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Storage**: In-memory (for simplicity; can be extended to use a database)

## Future Enhancements

- User authentication and profiles
- Persistent database storage (MongoDB, PostgreSQL, etc.)
- Email/SMS notifications
- Game chat functionality
- Location-based search
- Weather integration
- Rating and review system

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.