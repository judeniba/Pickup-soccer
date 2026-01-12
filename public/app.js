// API endpoints
const API_URL = '/api/games';

// Load games on page load
document.addEventListener('DOMContentLoaded', () => {
    loadGames();
    setupCreateGameForm();
    
    // Auto-refresh games every 30 seconds
    setInterval(loadGames, 30000);
});

// Setup create game form
function setupCreateGameForm() {
    const form = document.getElementById('createGameForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const location = document.getElementById('location').value;
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;
        const maxPlayersValue = parseInt(document.getElementById('maxPlayers').value, 10);
        const maxPlayers = isNaN(maxPlayersValue) ? 10 : maxPlayersValue;

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ location, date, time, maxPlayers })
            });

            if (response.ok) {
                form.reset();
                showMessage('Game created successfully!', 'success');
                loadGames();
            } else {
                const error = await response.json();
                showMessage(error.error || 'Failed to create game', 'error');
            }
        } catch (error) {
            showMessage('Network error. Please try again.', 'error');
        }
    });
}

// Load all games
async function loadGames() {
    const container = document.getElementById('gamesContainer');
    
    try {
        const response = await fetch(API_URL);
        const games = await response.json();

        if (games.length === 0) {
            container.innerHTML = '<p class="no-games">No games available. Create one to get started!</p>';
            return;
        }

        container.innerHTML = games.map(game => createGameCard(game)).join('');
        
        // Attach event listeners to join/leave buttons
        games.forEach(game => {
            setupGameActions(game.id);
        });
    } catch (error) {
        container.innerHTML = '<p class="error">Failed to load games. Please refresh the page.</p>';
    }
}

// Create HTML for a game card
function createGameCard(game) {
    const isFull = game.players.length >= game.maxPlayers;
    const statusClass = isFull ? 'full' : 'open';
    const statusText = isFull ? 'FULL' : 'OPEN';
    
    return `
        <div class="game-card">
            <div class="game-header">
                <div class="game-location">${escapeHtml(game.location)}</div>
                <div class="game-status ${statusClass}">${statusText}</div>
            </div>
            <div class="game-details">
                <div class="game-detail"><strong>📅 Date:</strong> ${formatDate(game.date)}</div>
                <div class="game-detail"><strong>🕐 Time:</strong> ${game.time}</div>
                <div class="game-detail"><strong>👥 Players:</strong> ${game.players.length}/${game.maxPlayers}</div>
            </div>
            ${game.players.length > 0 ? `
                <div class="players-list">
                    <h4>Players:</h4>
                    <ul>
                        ${game.players.map(player => `<li>${escapeHtml(player)}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            <div class="game-actions">
                <form class="join-form" id="joinForm-${game.id}">
                    <input 
                        type="text" 
                        placeholder="Enter your name" 
                        required 
                        id="playerName-${game.id}"
                    >
                    <button type="submit" class="join-button" ${isFull ? 'disabled' : ''}>
                        Join Game
                    </button>
                </form>
                <button class="leave-button" data-game-id="${game.id}">
                    Leave Game
                </button>
            </div>
            <div id="message-${game.id}"></div>
        </div>
    `;
}

// Setup join/leave actions for a game
function setupGameActions(gameId) {
    const joinForm = document.getElementById(`joinForm-${gameId}`);
    const leaveButton = document.querySelector(`button.leave-button[data-game-id="${gameId}"]`);
    
    if (joinForm) {
        joinForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const playerNameInput = document.getElementById(`playerName-${gameId}`);
            const playerName = playerNameInput.value.trim();
            
            if (!playerName) return;
            
            try {
                const response = await fetch(`${API_URL}/${gameId}/join`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ playerName })
                });

                if (response.ok) {
                    playerNameInput.value = '';
                    showGameMessage(gameId, 'Successfully joined the game!', 'success');
                    loadGames();
                } else {
                    const error = await response.json();
                    showGameMessage(gameId, error.error || 'Failed to join game', 'error');
                }
            } catch (error) {
                showGameMessage(gameId, 'Network error. Please try again.', 'error');
            }
        });
    }
    
    if (leaveButton) {
        leaveButton.addEventListener('click', () => {
            const playerNameInput = document.getElementById(`playerName-${gameId}`);
            leaveGame(gameId, playerNameInput.value);
        });
    }
}

// Leave a game
async function leaveGame(gameId, playerName) {
    if (!playerName) {
        showGameMessage(gameId, 'Please enter your name in the join field to leave', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/${gameId}/leave`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ playerName: playerName.trim() })
        });

        if (response.ok) {
            showGameMessage(gameId, 'Successfully left the game!', 'success');
            loadGames();
        } else {
            const error = await response.json();
            showGameMessage(gameId, error.error || 'Failed to leave game', 'error');
        }
    } catch (error) {
        showGameMessage(gameId, 'Network error. Please try again.', 'error');
    }
}

// Show message for a specific game
function showGameMessage(gameId, message, type) {
    const messageDiv = document.getElementById(`message-${gameId}`);
    if (messageDiv) {
        messageDiv.innerHTML = `<div class="${type}">${escapeHtml(message)}</div>`;
        setTimeout(() => {
            messageDiv.innerHTML = '';
        }, 5000);
    }
}

// Show general message
function showMessage(message, type) {
    const createGameSection = document.querySelector('.create-game');
    const existingMessage = createGameSection.querySelector('.message');
    
    if (existingMessage) {
        existingMessage.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    createGameSection.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        weekday: 'short', 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}
