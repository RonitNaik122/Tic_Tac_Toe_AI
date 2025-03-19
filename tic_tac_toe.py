import streamlit as st
import numpy as np
import random
import time

# Page Configuration
st.set_page_config(page_title="Tic-Tac-Toe Deluxe", layout="wide", initial_sidebar_state="collapsed")

# Custom Styles for Enhanced UI
st.markdown(
    """
    <style>
        /* Global Styles */
        body {
            background-color: #121212;
            font-family: 'Poppins', sans-serif;
            color: #FFFFFF;
        }

        /* Header Styles */
        .main-header {
            background: linear-gradient(90deg, #8E2DE2, #4A00E0);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.3);
        }

        .title {
            color: #FFFFFF;
            font-size: 42px;
            font-weight: 800;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            margin: 0;
        }

        .subtitle {
            color: #E0E0E0;
            font-size: 18px;
            margin-top: 5px;
        }

        /* Game Board Styles */
        .game-board {
            background-color: #1E1E2F;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
        }

        .cell-button {
            width: 120px !important;
            height: 120px !important;
            font-size: 48px !important;
            font-weight: bold !important;
            margin: 8px !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        /* Cell button variants */
        .empty-cell {
            background-color: #2D2D44 !important;
            color: #FFFFFF !important;
        }

        .x-cell {
            background: linear-gradient(135deg, #FF5252, #B33939) !important;
            color: #FFFFFF !important;
        }

        .o-cell {
            background: linear-gradient(135deg, #3498DB, #2980B9) !important;
            color: #FFFFFF !important;
        }

        .empty-cell:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3) !important;
        }

        /* Settings Panel Styles */
        .settings-panel {
            background: linear-gradient(135deg, #2C3E50, #1A1A2E);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.3);
        }

        .settings-header {
            color: #E0E0E0;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 15px;
            border-bottom: 2px solid #4A00E0;
            padding-bottom: 10px;
        }

        /* Status and Notification Styles */
        .player-turn {
            background-color: rgba(74, 20, 140, 0.7);
            padding: 10px 15px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            margin: 15px 0;
            text-align: center;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% {opacity: 0.7;}
            50% {opacity: 1;}
            100% {opacity: 0.7;}
        }

        .winner {
            background: linear-gradient(90deg, #FFD700, #FFA500);
            color: #000000;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            margin: 15px 0;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
            animation: winner-pulse 1.5s infinite;
        }

        @keyframes winner-pulse {
            0% {transform: scale(1);}
            50% {transform: scale(1.05);}
            100% {transform: scale(1);}
        }

        .tie {
            background: linear-gradient(90deg, #95A5A6, #7F8C8D);
            color: #FFFFFF;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            margin: 15px 0;
            padding: 15px;
            border-radius: 10px;
        }

        /* Button Styles */
        .action-button {
            background: linear-gradient(90deg, #4A00E0, #8E2DE2) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 10px 20px !important;
            border-radius: 8px !important;
            border: none !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
            transition: all 0.3s ease !important;
        }

        .action-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3) !important;
        }

        /* Game Stats */
        .stats-container {
            background-color: rgba(46, 49, 65, 0.7);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
        }

        .stat-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .stat-label {
            color: #B8B8B8;
        }

        .stat-value {
            color: #FFFFFF;
            font-weight: 600;
        }

        /* Custom Radio & Select Styles */
        div.stRadio > div {
            background-color: #2D2D44;
            border-radius: 10px;
            padding: 10px;
        }

        div.stRadio > div > div > label {
            background-color: transparent !important;
            color: #E0E0E0 !important;
        }

        div.stSelectbox > div > div {
            background-color: #2D2D44;
            border-radius: 8px;
        }

        /* Animations */
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }

        .fadeIn {
            animation: fadeIn 0.5s ease;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .cell-button {
                width: 80px !important;
                height: 80px !important;
                font-size: 32px !important;
            }

            .title {
                font-size: 32px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Game State
if "board" not in st.session_state:
    st.session_state.board = np.full((3, 3), "", dtype=str)
if "player_turn" not in st.session_state:
    st.session_state.player_turn = True  # True = Player X, False = AI/Player O
if "game_mode" not in st.session_state:
    st.session_state.game_mode = "1P"
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Medium"
if "player_x_wins" not in st.session_state:
    st.session_state.player_x_wins = 0
if "player_o_wins" not in st.session_state:
    st.session_state.player_o_wins = 0
if "ties" not in st.session_state:
    st.session_state.ties = 0
if "move_count" not in st.session_state:
    st.session_state.move_count = 0
if "game_history" not in st.session_state:
    st.session_state.game_history = []
if "last_move" not in st.session_state:
    st.session_state.last_move = None
if "game_active" not in st.session_state:
    st.session_state.game_active = True
if "game_start_time" not in st.session_state:
    st.session_state.game_start_time = time.time()
if "game_duration" not in st.session_state:
    st.session_state.game_duration = 0

# Check for a Winner
def check_winner():
    b = st.session_state.board
    for row in b:
        if row[0] == row[1] == row[2] != "":
            return row[0]
    for col in range(3):
        if b[0][col] == b[1][col] == b[2][col] != "":
            return b[0][col]
    if b[0][0] == b[1][1] == b[2][2] != "" or b[0][2] == b[1][1] == b[2][0] != "":
        return b[1][1]
    if "" not in b:
        return "Tie"
    return None

# Minimax Algorithm for AI
def minimax(b, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
    winner = check_winner()
    if winner == "X": return depth - 10
    if winner == "O": return 10 - depth
    if winner == "Tie": return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if b[i][j] == "":
                    b[i][j] = "O"
                    score = minimax(b, depth + 1, False, alpha, beta)
                    b[i][j] = ""
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if b[i][j] == "":
                    b[i][j] = "X"
                    score = minimax(b, depth + 1, True, alpha, beta)
                    b[i][j] = ""
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score

# AI Move Logic
def best_ai_move():
    best_score = -float('inf')
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if st.session_state.board[i][j] == "":
                st.session_state.board[i][j] = "O"
                score = minimax(st.session_state.board, 0, False)
                st.session_state.board[i][j] = ""
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move

def ai_move():
    if not st.session_state.game_active:
        return

    # Add thinking delay for more natural feel
    time.sleep(0.5)

    if st.session_state.difficulty == "Easy":
        # 20% chance to make a good move, 80% random
        if random.random() < 0.2:
            i, j = best_ai_move()
        else:
            empty_cells = [(i, j) for i in range(3) for j in range(3) if st.session_state.board[i][j] == ""]
            if empty_cells:
                i, j = random.choice(empty_cells)
            else:
                return
    elif st.session_state.difficulty == "Medium":
        # 60% chance to make the best move
        if random.random() < 0.6:
            i, j = best_ai_move()
        else:
            empty_cells = [(i, j) for i in range(3) for j in range(3) if st.session_state.board[i][j] == ""]
            if empty_cells:
                i, j = random.choice(empty_cells)
            else:
                return
    else:  # Hard - always makes the best move
        i, j = best_ai_move()

    st.session_state.board[i][j] = "O"
    st.session_state.last_move = (i, j)
    st.session_state.move_count += 1
    st.session_state.player_turn = True

    # Check for game end
    winner = check_winner()
    if winner:
        handle_game_end(winner)

# Player Move
def player_move(i, j):
    if not st.session_state.game_active or st.session_state.board[i][j] != "":
        return

    current_player = "X" if st.session_state.player_turn else "O"
    st.session_state.board[i][j] = current_player
    st.session_state.last_move = (i, j)
    st.session_state.move_count += 1
    st.session_state.player_turn = not st.session_state.player_turn

    # Check for winner after player move
    winner = check_winner()
    if winner:
        handle_game_end(winner)
        return

    # If 1-player mode and it's AI's turn
    if st.session_state.game_mode == "1P" and not st.session_state.player_turn:
        ai_move()

def handle_game_end(winner):
    st.session_state.game_active = False
    st.session_state.game_duration = round(time.time() - st.session_state.game_start_time, 1)

    # Update statistics
    if winner == "X":
        st.session_state.player_x_wins += 1
    elif winner == "O":
        st.session_state.player_o_wins += 1
    elif winner == "Tie":
        st.session_state.ties += 1

    # Add to game history
    game_result = {
        "winner": winner,
        "moves": st.session_state.move_count,
        "duration": st.session_state.game_duration,
        "mode": st.session_state.game_mode,
        "difficulty": st.session_state.difficulty if st.session_state.game_mode == "1P" else "N/A"
    }
    st.session_state.game_history.append(game_result)

# Reset the Game
def reset_game():
    st.session_state.board = np.full((3, 3), "", dtype=str)
    st.session_state.player_turn = True
    st.session_state.move_count = 0
    st.session_state.last_move = None
    st.session_state.game_active = True
    st.session_state.game_start_time = time.time()
    st.session_state.game_duration = 0

# Get cell styling based on content
def get_cell_style(value):
    if value == "X":
        return "x-cell"
    elif value == "O":
        return "o-cell"
    else:
        return "empty-cell"

# UI Layout
st.markdown('<div class="main-header fadeIn"><h1 class="title">Tic-Tac-Toe Deluxe</h1><p class="subtitle">The classic game reimagined</p></div>', unsafe_allow_html=True)

# Create three columns for layout
col1, col2, col3 = st.columns([1, 2, 1])

# Left Column (Game Settings & Stats)
with col1:
    st.markdown('<div class="settings-panel fadeIn">', unsafe_allow_html=True)
    st.markdown('<h2 class="settings-header">Game Settings</h2>', unsafe_allow_html=True)

    game_mode = st.radio("Game Mode", ["1-Player", "2-Player"], index=0 if st.session_state.game_mode == "1P" else 1)
    st.session_state.game_mode = "1P" if game_mode == "1-Player" else "2P"

    if st.session_state.game_mode == "1P":
        st.markdown('<p style="margin-top:15px;">AI Difficulty:</p>', unsafe_allow_html=True)
        st.session_state.difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"], value=st.session_state.difficulty)

    st.markdown('<button class="action-button stButton">Reset Game</button>', unsafe_allow_html=True)
    if st.button("Reset Game", key="reset_btn"):
        reset_game()

    # Game Statistics
    st.markdown('<h2 class="settings-header" style="margin-top:30px;">Game Stats</h2>', unsafe_allow_html=True)
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="stat-item">
            <span class="stat-label">Player X Wins:</span>
            <span class="stat-value">{st.session_state.player_x_wins}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Player O Wins:</span>
            <span class="stat-value">{st.session_state.player_o_wins}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Ties:</span>
            <span class="stat-value">{st.session_state.ties}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Current Game:</span>
            <span class="stat-value">{st.session_state.move_count} moves</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Middle Column (Game Board)
with col2:
    st.markdown('<div class="game-board fadeIn">', unsafe_allow_html=True)

    # Player Turn Indicator
    if st.session_state.game_active:
        current_player = "X" if st.session_state.player_turn else "O"
        player_label = "Your" if st.session_state.game_mode == "1P" and current_player == "X" else "AI's" if st.session_state.game_mode == "1P" and current_player == "O" else f"Player {current_player}'s"
        st.markdown(f'<div class="player-turn">{player_label} Turn</div>', unsafe_allow_html=True)

    # Game Board
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            cell_value = st.session_state.board[i][j]
            cell_style = get_cell_style(cell_value)

            # Highlight last move with pulse animation
            highlight_style = ""
            if st.session_state.last_move == (i, j):
                highlight_style = "animation: winner-pulse 1.5s infinite;"

            # Create styled button for each cell
            cell_content = cell_value if cell_value else " "
            cols[j].markdown(
                f"""<button
                    class="cell-button {cell_style}"
                    style="{highlight_style}"
                    onclick="
                        window.parent.postMessage({{
                            type: 'streamlit:buttonClicked',
                            key: 'cell_{i}_{j}'
                        }}, '*')
                    "
                >{cell_content}</button>""",
                unsafe_allow_html=True
            )

            # Hidden button to capture clicks
            if cols[j].button("", key=f"cell_{i}_{j}", help="Make your move", disabled=not st.session_state.game_active or cell_value != ""):
                player_move(i, j)
                st.rerun()

    # Show Winner Message or Tie
    winner = check_winner()
    if winner:
        if winner == "Tie":
            st.markdown('<div class="tie fadeIn">It\'s a Tie! 🤝</div>', unsafe_allow_html=True)
        else:
            winner_label = "You won!" if st.session_state.game_mode == "1P" and winner == "X" else "AI won!" if st.session_state.game_mode == "1P" and winner == "O" else f"Player {winner} Wins!"
            st.markdown(f'<div class="winner fadeIn">{winner_label} 🏆</div>', unsafe_allow_html=True)

        if st.button("Play Again", key="play_again", help="Start a new game"):
            reset_game()
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Right Column (Game Info & Help)
with col3:
    st.markdown('<div class="settings-panel fadeIn">', unsafe_allow_html=True)
    st.markdown('<h2 class="settings-header">How to Play</h2>', unsafe_allow_html=True)

    st.markdown("""
    - Players take turns marking empty squares
    - Get three of your marks in a row (horizontally, vertically, or diagonally) to win
    - The game ends in a tie if all squares are filled without a winner
    """)

    st.markdown('<h2 class="settings-header" style="margin-top:20px;">AI Difficulty</h2>', unsafe_allow_html=True)

    if st.session_state.game_mode == "1P":
        st.markdown("""
        - **Easy**: Makes mostly random moves
        - **Medium**: Makes some strategic moves
        - **Hard**: Makes optimal moves using minimax algorithm
        """)
    else:
        st.markdown("Two-player mode active. Take turns with a friend!")

    # Last 3 Game Results
    if len(st.session_state.game_history) > 0:
        st.markdown('<h2 class="settings-header" style="margin-top:20px;">Recent Games</h2>', unsafe_allow_html=True)
        st.markdown('<div class="stats-container">', unsafe_allow_html=True)

        for i, game in enumerate(reversed(st.session_state.game_history[-3:])):
            result_text = "Tie" if game["winner"] == "Tie" else f"{game['winner']} Won"
            st.markdown(f"""
                <div class="stat-item">
                    <span class="stat-label">Game {len(st.session_state.game_history) - i}:</span>
                    <span class="stat-value">{result_text} ({game['moves']} moves)</span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)