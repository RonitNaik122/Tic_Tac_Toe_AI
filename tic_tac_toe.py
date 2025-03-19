import streamlit as st
import numpy as np
import time

# Colors
PLAYER = "O"  # User
AI = "X"  # AI

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = np.full((3, 3), "", dtype=str)
if "is_player_turn" not in st.session_state:
    st.session_state.is_player_turn = True
if "winner" not in st.session_state:
    st.session_state.winner = None

def check_winner(b):
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

def minimax(b, depth, is_maximizing):
    winner = check_winner(b)
    if winner == AI: return 10 - depth
    if winner == PLAYER: return depth - 10
    if winner == "Tie": return 0

    if is_maximizing:
        best = -1000
        for i in range(3):
            for j in range(3):
                if b[i][j] == "":
                    b[i][j] = AI
                    score = minimax(b, depth + 1, False)
                    b[i][j] = ""
                    best = max(best, score)
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if b[i][j] == "":
                    b[i][j] = PLAYER
                    score = minimax(b, depth + 1, True)
                    b[i][j] = ""
                    best = min(best, score)
        return best

def ai_play():
    best_score = -1000
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if st.session_state.board[i][j] == "":
                st.session_state.board[i][j] = AI
                score = minimax(st.session_state.board, 0, False)
                st.session_state.board[i][j] = ""
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    i, j = best_move
    st.session_state.board[i][j] = AI

    st.session_state.winner = check_winner(st.session_state.board)

def player_move(i, j):
    if st.session_state.board[i][j] == "" and st.session_state.winner is None:
        st.session_state.board[i][j] = PLAYER
        st.session_state.winner = check_winner(st.session_state.board)
        if st.session_state.winner is None:
            time.sleep(0.5)
            ai_play()

def reset_board():
    st.session_state.board = np.full((3, 3), "", dtype=str)
    st.session_state.is_player_turn = True
    st.session_state.winner = None

st.title("Tic-Tac-Toe AI 🎮")
st.markdown("Play against an AI using the **Minimax Algorithm**.")

# Display the board
cols = st.columns(3)
for i in range(3):
    for j in range(3):
        with cols[j]:
            if st.session_state.board[i][j] == "":
                if st.button(" ", key=f"{i}{j}"):
                    player_move(i, j)
            else:
                st.button(st.session_state.board[i][j], key=f"{i}{j}", disabled=True)

# Display result
if st.session_state.winner:
    if st.session_state.winner == "Tie":
        st.success("It's a Tie! 🤝")
    else:
        st.success(f"{st.session_state.winner} wins! 🎉")

if st.button("Restart Game"):
    reset_board()
