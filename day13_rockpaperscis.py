import streamlit as st
import random

# Initialize session state for scores
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'computer_score' not in st.session_state:
    st.session_state.computer_score = 0
if 'games_played' not in st.session_state:
    st.session_state.games_played = 0

def get_computer_choice():
    """Generate random computer choice"""
    return random.choice(['Rock', 'Paper', 'Scissors'])

def determine_winner(user_choice, computer_choice):
    """Determine the winner of the game"""
    if user_choice == computer_choice:
        return 'tie'
    
    winning_combinations = {
        'Rock': 'Scissors',
        'Paper': 'Rock', 
        'Scissors': 'Paper'
    }
    
    if winning_combinations[user_choice] == computer_choice:
        return 'user'
    else:
        return 'computer'

def get_emoji(choice):
    """Return emoji for each choice"""
    emojis = {
        'Rock': '🪨',
        'Paper': '📄',
        'Scissors': '✂️'
    }
    return emojis.get(choice, '')

# Main app
st.title("🎮 Rock, Paper, Scissors")
st.write("Choose your weapon and battle the computer!")

# Display current scores
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Your Score", st.session_state.user_score)
with col2:
    st.metric("Computer Score", st.session_state.computer_score)
with col3:
    st.metric("Games Played", st.session_state.games_played)

st.divider()

# Game interface
st.subheader("Make your choice:")

# Create buttons for user choices
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🪨 Rock", use_container_width=True):
        user_choice = "Rock"
        computer_choice = get_computer_choice()
        result = determine_winner(user_choice, computer_choice)
        
        # Update game state
        st.session_state.games_played += 1
        if result == 'user':
            st.session_state.user_score += 1
        elif result == 'computer':
            st.session_state.computer_score += 1
        
        # Store choices for display
        st.session_state.last_user_choice = user_choice
        st.session_state.last_computer_choice = computer_choice
        st.session_state.last_result = result

with col2:
    if st.button("📄 Paper", use_container_width=True):
        user_choice = "Paper"
        computer_choice = get_computer_choice()
        result = determine_winner(user_choice, computer_choice)
        
        # Update game state
        st.session_state.games_played += 1
        if result == 'user':
            st.session_state.user_score += 1
        elif result == 'computer':
            st.session_state.computer_score += 1
        
        # Store choices for display
        st.session_state.last_user_choice = user_choice
        st.session_state.last_computer_choice = computer_choice
        st.session_state.last_result = result

with col3:
    if st.button("✂️ Scissors", use_container_width=True):
        user_choice = "Scissors"
        computer_choice = get_computer_choice()
        result = determine_winner(user_choice, computer_choice)
        
        # Update game state
        st.session_state.games_played += 1
        if result == 'user':
            st.session_state.user_score += 1
        elif result == 'computer':
            st.session_state.computer_score += 1
        
        # Store choices for display
        st.session_state.last_user_choice = user_choice
        st.session_state.last_computer_choice = computer_choice
        st.session_state.last_result = result

# Display last game result
if 'last_result' in st.session_state:
    st.divider()
    st.subheader("Last Game:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**You chose:**")
        st.write(f"{get_emoji(st.session_state.last_user_choice)} {st.session_state.last_user_choice}")
    
    with col2:
        st.write("**Computer chose:**")
        st.write(f"{get_emoji(st.session_state.last_computer_choice)} {st.session_state.last_computer_choice}")
    
    # Display result
    if st.session_state.last_result == 'user':
        st.success("🎉 You Won!")
    elif st.session_state.last_result == 'computer':
        st.error("💻 Computer Won!")
    else:
        st.info("🤝 It's a Tie!")

# Reset button
st.divider()
if st.button("🔄 Reset Scores", type="secondary"):
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.games_played = 0
    # Clear last game results
    if 'last_result' in st.session_state:
        del st.session_state.last_result
        del st.session_state.last_user_choice
        del st.session_state.last_computer_choice
    st.rerun()

# Game statistics
if st.session_state.games_played > 0:
    st.divider()
    st.subheader("📊 Game Statistics")
    
    user_win_rate = (st.session_state.user_score / st.session_state.games_played) * 100
    computer_win_rate = (st.session_state.computer_score / st.session_state.games_played) * 100
    tie_rate = 100 - user_win_rate - computer_win_rate
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Your Win Rate", f"{user_win_rate:.1f}%")
    with col2:
        st.metric("Computer Win Rate", f"{computer_win_rate:.1f}%")
    with col3:
        st.metric("Tie Rate", f"{tie_rate:.1f}%")