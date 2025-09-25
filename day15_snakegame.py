import streamlit as st
import random
import time
import numpy as np

# Initialize session state
def init_game():
    """Initialize or reset the game state"""
    st.session_state.board_size = 20
    st.session_state.snake = [(10, 10), (10, 9), (10, 8)]  # Head at index 0
    st.session_state.direction = (0, 1)  # Moving right initially
    st.session_state.food = generate_food()
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_running = False

def generate_food():
    """Generate food at a random position not occupied by snake"""
    while True:
        food_pos = (
            random.randint(0, st.session_state.board_size - 1),
            random.randint(0, st.session_state.board_size - 1)
        )
        if food_pos not in st.session_state.snake:
            return food_pos

def move_snake():
    """Move the snake in the current direction"""
    if st.session_state.game_over or not st.session_state.game_running:
        return
    
    head = st.session_state.snake[0]
    new_head = (
        head[0] + st.session_state.direction[0],
        head[1] + st.session_state.direction[1]
    )
    
    # Check wall collision
    if (new_head[0] < 0 or new_head[0] >= st.session_state.board_size or
        new_head[1] < 0 or new_head[1] >= st.session_state.board_size):
        st.session_state.game_over = True
        st.session_state.game_running = False
        return
    
    # Check self collision
    if new_head in st.session_state.snake:
        st.session_state.game_over = True
        st.session_state.game_running = False
        return
    
    # Move snake
    st.session_state.snake.insert(0, new_head)
    
    # Check food collision
    if new_head == st.session_state.food:
        st.session_state.score += 10
        st.session_state.food = generate_food()
    else:
        # Remove tail if no food eaten
        st.session_state.snake.pop()

def change_direction(new_direction):
    """Change snake direction if valid"""
    current_dir = st.session_state.direction
    # Prevent reversing into itself
    if (new_direction[0] * -1, new_direction[1] * -1) != current_dir:
        st.session_state.direction = new_direction

def render_board():
    """Render the game board using HTML and CSS"""
    board = np.zeros((st.session_state.board_size, st.session_state.board_size), dtype=int)
    
    # Place snake (head = 2, body = 1)
    for i, segment in enumerate(st.session_state.snake):
        if i == 0:  # Head
            board[segment[0]][segment[1]] = 2
        else:  # Body
            board[segment[0]][segment[1]] = 1
    
    # Place food (3)
    board[st.session_state.food[0]][st.session_state.food[1]] = 3
    
    # Generate HTML
    html = """
    <style>
    .game-board {
        display: grid;
        grid-template-columns: repeat(20, 20px);
        grid-gap: 1px;
        background-color: #333;
        padding: 10px;
        border-radius: 5px;
        margin: 20px auto;
        width: fit-content;
    }
    .cell {
        width: 20px;
        height: 20px;
        background-color: #111;
    }
    .snake-head {
        background-color: #4CAF50 !important;
        border-radius: 3px;
    }
    .snake-body {
        background-color: #8BC34A !important;
        border-radius: 2px;
    }
    .food {
        background-color: #FF5722 !important;
        border-radius: 50%;
    }
    </style>
    <div class="game-board">
    """
    
    for row in board:
        for cell in row:
            if cell == 2:  # Snake head
                html += '<div class="cell snake-head"></div>'
            elif cell == 1:  # Snake body
                html += '<div class="cell snake-body"></div>'
            elif cell == 3:  # Food
                html += '<div class="cell food"></div>'
            else:  # Empty
                html += '<div class="cell"></div>'
    
    html += "</div>"
    return html

# Main app
st.title("🐍 Snake Game")
st.write("Use the buttons below to control the snake. Eat the red food to grow and increase your score!")

# Initialize game if not exists
if 'snake' not in st.session_state:
    init_game()

# Game controls
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

with col1:
    if st.button("⬆️ Up", key="up"):
        change_direction((-1, 0))

with col2:
    if st.button("⬇️ Down", key="down"):
        change_direction((1, 0))

with col3:
    if st.button("⬅️ Left", key="left"):
        change_direction((0, -1))

with col4:
    if st.button("➡️ Right", key="right"):
        change_direction((0, 1))

with col5:
    if st.button("🎮 Start/Pause", key="start_pause"):
        st.session_state.game_running = not st.session_state.game_running

# Game status and score
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Score", st.session_state.score)
with col2:
    status = "Game Over" if st.session_state.game_over else ("Running" if st.session_state.game_running else "Paused")
    st.metric("Status", status)
with col3:
    st.metric("Length", len(st.session_state.snake))

# Restart button
if st.button("🔄 Restart Game", key="restart"):
    init_game()
    st.rerun()

# Game board
board_container = st.empty()

# Game loop
if st.session_state.game_running and not st.session_state.game_over:
    move_snake()
    time.sleep(0.2)  # Game speed
    st.rerun()

# Display board
board_container.markdown(render_board(), unsafe_allow_html=True)

# Game over message
if st.session_state.game_over:
    st.error(f"🎮 Game Over! Your final score was {st.session_state.score}")
    st.balloons()

# Instructions
with st.expander("📖 How to Play"):
    st.markdown("""
    **Objective:** Control the snake to eat food and grow as long as possible!
    
    **Controls:**
    - Use the directional buttons (⬆️⬇️⬅️➡️) to change the snake's direction
    - Click "🎮 Start/Pause" to start the game or pause/resume
    - Click "🔄 Restart Game" to start over
    
    **Rules:**
    - The snake moves automatically in the chosen direction
    - Eat the red food (🔴) to grow and increase your score
    - Avoid hitting the walls or the snake's own body
    - Each food eaten increases your score by 10 points
    
    **Tips:**
    - Plan your moves ahead to avoid trapping yourself
    - The snake moves faster as the game progresses
    - Try to achieve the highest score possible!
    """)

# Add some styling
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 20px;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)