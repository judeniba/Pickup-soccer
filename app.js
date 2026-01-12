// Pickup Soccer App - Main JavaScript

// Game data storage
let games = [];

// Load games from localStorage on page load
document.addEventListener('DOMContentLoaded', () => {
    loadGames();
    displayGames();
});

// Handle form submission
document.getElementById('gameForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const location = document.getElementById('location').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const maxPlayers = parseInt(document.getElementById('players').value);
    
    const game = {
        id: Date.now(),
        location,
        date,
        time,
        maxPlayers,
        currentPlayers: 0
    };
    
    games.push(game);
    saveGames();
    displayGames();
    
    // Reset form
    e.target.reset();
    
    // Show success message
    alert('Game created successfully!');
});

// Save games to localStorage
function saveGames() {
    localStorage.setItem('pickupSoccerGames', JSON.stringify(games));
}

// Load games from localStorage
function loadGames() {
    const stored = localStorage.getItem('pickupSoccerGames');
    if (stored) {
        games = JSON.parse(stored);
    }
}

// Display games in the UI
function displayGames() {
    const gamesList = document.getElementById('gamesList');
    
    if (games.length === 0) {
        gamesList.innerHTML = '<p class="no-games">No games scheduled yet. Create one to get started!</p>';
        return;
    }
    
    // Sort games by date
    games.sort((a, b) => new Date(a.date + ' ' + a.time) - new Date(b.date + ' ' + b.time));
    
    gamesList.innerHTML = games.map(game => `
        <div class="game-card">
            <h3>📍 ${game.location}</h3>
            <p class="game-info"><strong>Date:</strong> ${formatDate(game.date)}</p>
            <p class="game-info"><strong>Time:</strong> ${formatTime(game.time)}</p>
            <p class="game-info"><strong>Players:</strong> ${game.currentPlayers} / ${game.maxPlayers}</p>
            <button class="btn btn-success" onclick="joinGame(${game.id})">Join Game</button>
        </div>
    `).join('');
}

// Join a game
function joinGame(gameId) {
    const game = games.find(g => g.id === gameId);
    
    if (game) {
        if (game.currentPlayers < game.maxPlayers) {
            game.currentPlayers++;
            saveGames();
            displayGames();
            alert('You have joined the game!');
        } else {
            alert('Sorry, this game is full!');
        }
    }
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        weekday: 'short', 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

// Format time for display
function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
}
