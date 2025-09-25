import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Initialize the database
def init_database():
    conn = sqlite3.connect('workout_logger.db')
    c = conn.cursor()
    
    # Create workouts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            exercise TEXT NOT NULL,
            sets INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            weight REAL NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Add workout to database
def add_workout(date, exercise, sets, reps, weight, notes=""):
    conn = sqlite3.connect('workout_logger.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO workouts (date, exercise, sets, reps, weight, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (date, exercise, sets, reps, weight, notes))
    
    conn.commit()
    conn.close()

# Get all workouts from database
def get_all_workouts():
    conn = sqlite3.connect('workout_logger.db')
    df = pd.read_sql_query("SELECT * FROM workouts ORDER BY date DESC, id DESC", conn)
    conn.close()
    return df

# Get workouts for a specific exercise
def get_exercise_history(exercise):
    conn = sqlite3.connect('workout_logger.db')
    df = pd.read_sql_query(
        "SELECT * FROM workouts WHERE exercise = ? ORDER BY date ASC", 
        conn, params=(exercise,)
    )
    conn.close()
    return df

# Delete workout
def delete_workout(workout_id):
    conn = sqlite3.connect('workout_logger.db')
    c = conn.cursor()
    c.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
    conn.commit()
    conn.close()

# Get unique exercises
def get_exercises():
    conn = sqlite3.connect('workout_logger.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT exercise FROM workouts ORDER BY exercise")
    exercises = [row[0] for row in c.fetchall()]
    conn.close()
    return exercises

# Calculate weekly progress
def get_weekly_progress():
    conn = sqlite3.connect('workout_logger.db')
    df = pd.read_sql_query('''
        SELECT 
            date,
            exercise,
            SUM(sets * reps * weight) as total_volume,
            MAX(weight) as max_weight,
            SUM(sets * reps) as total_reps
        FROM workouts 
        GROUP BY date, exercise 
        ORDER BY date ASC
    ''', conn)
    conn.close()
    
    if df.empty:
        return df
    
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.isocalendar().week
    df['year'] = df['date'].dt.year
    df['week_year'] = df['year'].astype(str) + '-W' + df['week'].astype(str).str.zfill(2)
    
    return df

# Streamlit App
def main():
    st.set_page_config(page_title="Gym Workout Logger", page_icon="💪", layout="wide")
    
    # Initialize database
    init_database()
    
    st.title("💪 Gym Workout Logger")
    st.markdown("---")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Log Workout", "Workout History", "Progress Analytics"])
    
    if page == "Log Workout":
        log_workout_page()
    elif page == "Workout History":
        workout_history_page()
    elif page == "Progress Analytics":
        progress_analytics_page()

def log_workout_page():
    st.header("📝 Log New Workout")
    
    # Common exercises for quick selection
    common_exercises = [
        "Bench Press", "Squat", "Deadlift", "Overhead Press", "Barbell Row",
        "Pull-ups", "Dips", "Bicep Curls", "Tricep Extensions", "Leg Press",
        "Lat Pulldown", "Shoulder Press", "Lunges", "Push-ups", "Planks"
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Date input
        workout_date = st.date_input("Workout Date", value=datetime.now().date())
        
        # Exercise selection
        exercise_option = st.radio("Choose exercise input method:", ["Select from common", "Enter custom"])
        
        if exercise_option == "Select from common":
            exercise = st.selectbox("Select Exercise", common_exercises)
        else:
            exercise = st.text_input("Enter Exercise Name")
        
        # Sets, Reps, Weight
        sets = st.number_input("Sets", min_value=1, max_value=20, value=3)
        reps = st.number_input("Reps", min_value=1, max_value=100, value=10)
        weight = st.number_input("Weight (kg)", min_value=0.0, step=2.5, value=20.0)
        
    with col2:
        # Notes
        notes = st.text_area("Notes (optional)", height=200, 
                           placeholder="Add any notes about your workout, form, difficulty, etc.")
        
        # Display workout summary
        st.subheader("Workout Summary")
        if exercise:
            st.write(f"**Exercise:** {exercise}")
            st.write(f"**Sets:** {sets}")
            st.write(f"**Reps:** {reps}")
            st.write(f"**Weight:** {weight} kg")
            st.write(f"**Total Volume:** {sets * reps * weight} kg")
    
    # Log workout button
    if st.button("Log Workout", type="primary"):
        if exercise:
            add_workout(str(workout_date), exercise, sets, reps, weight, notes)
            st.success(f"✅ Workout logged successfully!")
            st.balloons()
        else:
            st.error("Please enter an exercise name.")

def workout_history_page():
    st.header("📊 Workout History")
    
    # Get all workouts
    df = get_all_workouts()
    
    if df.empty:
        st.info("No workouts logged yet. Go to 'Log Workout' to add your first workout!")
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        exercises = get_exercises()
        selected_exercise = st.selectbox("Filter by Exercise", ["All"] + exercises)
    
    with col2:
        # Date range filter
        min_date = pd.to_datetime(df['date']).min().date()
        max_date = pd.to_datetime(df['date']).max().date()
        start_date = st.date_input("From Date", value=min_date)
    
    with col3:
        end_date = st.date_input("To Date", value=max_date)
    
    # Apply filters
    filtered_df = df.copy()
    filtered_df['date'] = pd.to_datetime(filtered_df['date'])
    
    if selected_exercise != "All":
        filtered_df = filtered_df[filtered_df['exercise'] == selected_exercise]
    
    filtered_df = filtered_df[
        (filtered_df['date'].dt.date >= start_date) & 
        (filtered_df['date'].dt.date <= end_date)
    ]
    
    # Display summary statistics
    if not filtered_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Workouts", len(filtered_df))
        with col2:
            st.metric("Total Volume", f"{(filtered_df['sets'] * filtered_df['reps'] * filtered_df['weight']).sum():.1f} kg")
        with col3:
            st.metric("Max Weight", f"{filtered_df['weight'].max():.1f} kg")
        with col4:
            st.metric("Total Reps", f"{(filtered_df['sets'] * filtered_df['reps']).sum()}")
    
    # Display workout table
    st.subheader("Workout Log")
    
    if not filtered_df.empty:
        # Prepare display dataframe
        display_df = filtered_df.copy()
        display_df['Volume'] = display_df['sets'] * display_df['reps'] * display_df['weight']
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        
        # Select columns to display
        display_columns = ['date', 'exercise', 'sets', 'reps', 'weight', 'Volume', 'notes']
        display_df = display_df[display_columns + ['id']]
        
        # Display dataframe with delete option
        for idx, row in display_df.iterrows():
            with st.expander(f"{row['date']} - {row['exercise']} ({row['sets']}x{row['reps']} @ {row['weight']}kg)"):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**Volume:** {row['Volume']} kg")
                    if row['notes']:
                        st.write(f"**Notes:** {row['notes']}")
                with col2:
                    if st.button(f"Delete", key=f"delete_{row['id']}", type="secondary"):
                        delete_workout(row['id'])
                        st.rerun()
    else:
        st.info("No workouts found for the selected filters.")

def progress_analytics_page():
    st.header("📈 Progress Analytics")
    
    df = get_weekly_progress()
    
    if df.empty:
        st.info("No workout data available for analysis. Log some workouts first!")
        return
    
    # Exercise selector for detailed analysis
    exercises = df['exercise'].unique()
    selected_exercise = st.selectbox("Select Exercise for Detailed Analysis", exercises)
    
    # Filter data for selected exercise
    exercise_data = df[df['exercise'] == selected_exercise].copy()
    
    # Create visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Weight progression over time
        fig_weight = px.line(
            exercise_data, 
            x='date', 
            y='max_weight',
            title=f'{selected_exercise} - Max Weight Progression',
            labels={'max_weight': 'Max Weight (kg)', 'date': 'Date'}
        )
        fig_weight.update_traces(line=dict(width=3))
        st.plotly_chart(fig_weight, use_container_width=True)
    
    with col2:
        # Volume progression over time
        fig_volume = px.line(
            exercise_data, 
            x='date', 
            y='total_volume',
            title=f'{selected_exercise} - Volume Progression',
            labels={'total_volume': 'Total Volume (kg)', 'date': 'Date'}
        )
        fig_volume.update_traces(line=dict(width=3))
        st.plotly_chart(fig_volume, use_container_width=True)
    
    # Weekly summary for all exercises
    st.subheader("Weekly Summary - All Exercises")
    
    weekly_data = df.groupby(['week_year', 'exercise']).agg({
        'total_volume': 'sum',
        'max_weight': 'max',
        'total_reps': 'sum'
    }).reset_index()
    
    # Weekly volume by exercise
    fig_weekly = px.bar(
        weekly_data, 
        x='week_year', 
        y='total_volume',
        color='exercise',
        title='Weekly Training Volume by Exercise',
        labels={'total_volume': 'Total Volume (kg)', 'week_year': 'Week'}
    )
    fig_weekly.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_weekly, use_container_width=True)
    
    # Summary statistics table
    st.subheader("Exercise Summary Statistics")
    summary_stats = df.groupby('exercise').agg({
        'total_volume': ['mean', 'max', 'sum'],
        'max_weight': ['mean', 'max'],
        'total_reps': ['mean', 'sum']
    }).round(2)
    
    summary_stats.columns = ['Avg Volume', 'Max Volume', 'Total Volume', 'Avg Max Weight', 'Peak Weight', 'Avg Reps', 'Total Reps']
    st.dataframe(summary_stats, use_container_width=True)

if __name__ == "__main__":
    main()