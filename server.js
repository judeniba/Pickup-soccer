const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Constants
const DEFAULT_MAX_PLAYERS = 10;

// In-memory storage for games (in production, use a database)
let games = [];
let gameIdCounter = 1;

// API Routes
app.get('/api/games', (req, res) => {
  res.json(games);
});

app.post('/api/games', (req, res) => {
  const { location, date, time, maxPlayers } = req.body;
  
  if (!location || !date || !time) {
    return res.status(400).json({ error: 'Location, date, and time are required' });
  }

  const parsedMaxPlayers = maxPlayers !== undefined ? parseInt(maxPlayers) : DEFAULT_MAX_PLAYERS;
  
  if (isNaN(parsedMaxPlayers)) {
    return res.status(400).json({ error: 'Max players must be a valid number' });
  }
  
  if (parsedMaxPlayers < 2 || parsedMaxPlayers > 30) {
    return res.status(400).json({ error: 'Max players must be between 2 and 30' });
  }

  const newGame = {
    id: gameIdCounter++,
    location,
    date,
    time,
    maxPlayers: parsedMaxPlayers,
    players: [],
    createdAt: new Date().toISOString()
  };

  games.push(newGame);
  res.status(201).json(newGame);
});

app.post('/api/games/:id/join', (req, res) => {
  const gameId = parseInt(req.params.id);
  const { playerName } = req.body;

  if (isNaN(gameId)) {
    return res.status(400).json({ error: 'Invalid game ID' });
  }

  if (!playerName) {
    return res.status(400).json({ error: 'Player name is required' });
  }

  const game = games.find(g => g.id === gameId);
  
  if (!game) {
    return res.status(404).json({ error: 'Game not found' });
  }

  if (game.players.length >= game.maxPlayers) {
    return res.status(400).json({ error: 'Game is full' });
  }

  if (game.players.includes(playerName)) {
    return res.status(400).json({ error: 'Player already joined' });
  }

  game.players.push(playerName);
  res.json(game);
});

app.delete('/api/games/:id/leave', (req, res) => {
  const gameId = parseInt(req.params.id);
  const { playerName } = req.body;

  if (isNaN(gameId)) {
    return res.status(400).json({ error: 'Invalid game ID' });
  }

  if (!playerName) {
    return res.status(400).json({ error: 'Player name is required' });
  }

  const game = games.find(g => g.id === gameId);
  
  if (!game) {
    return res.status(404).json({ error: 'Game not found' });
  }

  const playerIndex = game.players.indexOf(playerName);
  
  if (playerIndex === -1) {
    return res.status(400).json({ error: 'Player not in this game' });
  }

  game.players.splice(playerIndex, 1);
  res.json(game);
});

// Start server
app.listen(PORT, () => {
  console.log(`Pickup Soccer server running on http://localhost:${PORT}`);
});
