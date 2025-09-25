import streamlit as st
import random
import time

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
if 'current_player' not in st.session_state:
    st.session_state.current_player = 'X'
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = 'Two Player'
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'winning_line' not in st.session_state:
    st.session_state.winning_line = []

def check_winner(board):
    """Check for a winner and return the winner and winning line coordinates"""
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0], [(i, 0), (i, 1), (i, 2)]
    
    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != '':
            return board[0][j], [(0, j), (1, j), (2, j)]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2], [(0, 2), (1, 1), (2, 0)]
    
    return None, []

def is_board_full(board):
    """Check if the board is full"""
    return all(board[i][j] != '' for i in range(3) for j in range(3))

def get_computer_move(board):
    """Get a random move for the computer"""
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    return random.choice(empty_cells) if empty_cells else None

def make_move(row, col):
    """Make a move on the board"""
    if st.session_state.board[row][col] == '' and not st.session_state.game_over:
        st.session_state.board[row][col] = st.session_state.current_player
        
        # Check for winner
        winner, winning_line = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
            st.session_state.winning_line = winning_line
            st.session_state.game_over = True
        elif is_board_full(st.session_state.board):
            st.session_state.game_over = True
            st.session_state.winner = "Tie"
        else:
            # Switch player
            if st.session_state.game_mode == 'Two Player':
                st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
            elif st.session_state.game_mode == 'vs Computer' and st.session_state.current_player == 'X':
                st.session_state.current_player = 'O'
                # Computer makes a move
                computer_move = get_computer_move(st.session_state.board)
                if computer_move and not st.session_state.game_over:
                    time.sleep(0.5)  # Small delay for better UX
                    comp_row, comp_col = computer_move
                    st.session_state.board[comp_row][comp_col] = 'O'
                    
                    # Check for winner after computer move
                    winner, winning_line = check_winner(st.session_state.board)
                    if winner:
                        st.session_state.winner = winner
                        st.session_state.winning_line = winning_line
                        st.session_state.game_over = True
                    elif is_board_full(st.session_state.board):
                        st.session_state.game_over = True
                        st.session_state.winner = "Tie"
                    else:
                        st.session_state.current_player = 'X'

def reset_game():
    """Reset the game to initial state"""
    st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.winning_line = []

def get_button_style(row, col):
    """Get the CSS style for a button based on its state"""
    is_winning_cell = (row, col) in st.session_state.winning_line
    
    if is_winning_cell:
        return """
        background-color: #90EE90 !important;
        border: 3px solid #228B22 !important;
        color: #000080 !important;
        font-weight: bold !important;
        """
    else:
        return """
        background-color: #f0f2f6 !important;
        border: 2px solid #262730 !important;
        color: #262730 !important;
        """

# Streamlit UI
st.title("🎮 Tic-Tac-Toe ❌⭕")
st.markdown("---")

# Game mode selection
col1, col2 = st.columns([1, 1])
with col1:
    game_mode = st.selectbox("🎯 Game Mode:", ["Two Player", "vs Computer"])
    if game_mode != st.session_state.game_mode:
        st.session_state.game_mode = game_mode
        reset_game()

with col2:
    if st.button("🔄 Reset Game", use_container_width=True):
        reset_game()
        st.rerun()

# Current player display
if not st.session_state.game_over:
    if st.session_state.game_mode == 'Two Player':
        st.info(f"🎯 Current Player: **{st.session_state.current_player}**")
    else:
        if st.session_state.current_player == 'X':
            st.info("🎯 Your turn: **X**")
        else:
            st.info("🤖 Computer is thinking...")

# Game result display
if st.session_state.game_over:
    if st.session_state.winner == "Tie":
        st.warning("🤝 **It's a tie!**")
    else:
        if st.session_state.game_mode == 'vs Computer':
            if st.session_state.winner == 'X':
                st.success("🎉 **You won!**")
            else:
                st.error("🤖 **Computer won!**")
        else:
            st.success(f"🎉 **Player {st.session_state.winner} wins!**")

# Game board
st.markdown("### 🎲 Game Board")

# Custom CSS for buttons
st.markdown("""
<style>
.stButton > button {
    width: 100%;
    height: 80px;
    font-size: 24px;
    font-weight: bold;
    border-radius: 10px;
    margin: 2px;
}
</style>
""", unsafe_allow_html=True)

# Create the 3x3 grid
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        with cols[j]:
            button_text = st.session_state.board[i][j] if st.session_state.board[i][j] else " "
            button_style = get_button_style(i, j)
            
            # Create button with custom styling
            if st.button(
                button_text,
                key=f"btn_{i}_{j}",
                use_container_width=True,
                help=f"Position ({i+1}, {j+1})"
            ):
                make_move(i, j)
                st.rerun()

# Game statistics (optional enhancement)
st.markdown("---")
st.markdown("### 📊 Game Info")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎮 Game Mode", st.session_state.game_mode)

with col2:
    moves_made = sum(1 for i in range(3) for j in range(3) if st.session_state.board[i][j] != '')
    st.metric("📈 Moves Made", moves_made)

with col3:
    if st.session_state.game_over:
        if st.session_state.winner == "Tie":
            status = "Tie Game"
        else:
            status = f"{st.session_state.winner} Wins"
    else:
        status = "In Progress"
    st.metric("🎯 Game Status", status)

# Instructions
with st.expander("📋 How to Play"):
    st.markdown("""
    **Tic-Tac-Toe Rules:**
    - Players take turns placing X's and O's on a 3×3 grid
    - The first player to get 3 of their marks in a row (horizontally, vertically, or diagonally) wins
    - If all 9 squares are filled and no player has won, it's a tie
    
    **Game Modes:**
    - **Two Player**: Play against a friend on the same device
    - **vs Computer**: Play against the computer (makes random moves)
    
    **Features:**
    - Winning combinations are highlighted in green
    - Reset the game anytime with the "Reset Game" button
    - Track game progress with live statistics
    """)