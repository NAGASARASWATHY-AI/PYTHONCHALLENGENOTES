import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import timedelta
import json
import time

# ---- Page Configuration ----
st.set_page_config(
    page_title="🌊 AquaFlow - Hydration Analytics",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Custom CSS Styling ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .wave-container {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(79, 172, 254, 0.3);
    }
    
    .achievement-badge {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
        border: 2px solid #f093fb;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #a8edea 0%, #fed6e3 100%);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ---- Initialize Session State ----
if "hydration_log" not in st.session_state:
    st.session_state["hydration_log"] = {}
if "daily_target" not in st.session_state:
    st.session_state["daily_target"] = 2500  # in ml
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {
        "weight": 70,
        "activity_level": "moderate",
        "climate": "temperate"
    }

# ---- Helper Functions ----
def calculate_recommended_intake(weight, activity_level, climate):
    """Calculate recommended daily water intake based on user profile"""
    base_intake = weight * 35  # ml per kg
    
    activity_multiplier = {
        "low": 1.0,
        "moderate": 1.2,
        "high": 1.5,
        "athlete": 1.8
    }
    
    climate_multiplier = {
        "cold": 0.9,
        "temperate": 1.0,
        "warm": 1.1,
        "hot": 1.3
    }
    
    recommended = base_intake * activity_multiplier.get(activity_level, 1.0) * climate_multiplier.get(climate, 1.0)
    return int(recommended)

def get_hydration_status(current_intake, target):
    """Determine hydration status and color"""
    percentage = (current_intake / target) * 100
    
    if percentage >= 100:
        return "Excellent! 💧", "#00ff88", "🏆"
    elif percentage >= 80:
        return "Good Progress 📈", "#4facfe", "🎯"
    elif percentage >= 60:
        return "Keep Going! 💪", "#ffa726", "⚡"
    elif percentage >= 40:
        return "Need More Water 🥤", "#ff7043", "⚠️"
    else:
        return "Critical! Drink Now! 🚨", "#f44336", "🔴"

def create_wave_progress(percentage):
    """Create a wave-like progress indicator"""
    wave_height = min(percentage, 100)
    return f"""
    <div style="
        background: linear-gradient(to top, 
            rgba(79, 172, 254, 0.8) 0%, 
            rgba(79, 172, 254, 0.8) {wave_height}%, 
            rgba(255,255,255,0.1) {wave_height}%, 
            rgba(255,255,255,0.1) 100%);
        height: 200px;
        border-radius: 15px;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    ">
        {percentage:.1f}%
    </div>
    """

# ---- Main Application Header ----
st.markdown("""
<div class="main-header">
    <h1>🌊 AquaFlow - Hydration Analytics</h1>
    <p>Your intelligent water intake companion with personalized insights</p>
</div>
""", unsafe_allow_html=True)

# ---- Sidebar Configuration ----
with st.sidebar:
    st.header("🎛️ Personal Settings")
    
    # User Profile Section
    st.subheader("👤 Profile")
    weight = st.slider("Weight (kg)", 40, 150, st.session_state["user_profile"]["weight"], 1)
    activity_level = st.selectbox("Activity Level", 
                                 ["low", "moderate", "high", "athlete"],
                                 index=["low", "moderate", "high", "athlete"].index(st.session_state["user_profile"]["activity_level"]))
    climate = st.selectbox("Climate", 
                          ["cold", "temperate", "warm", "hot"],
                          index=["cold", "temperate", "warm", "hot"].index(st.session_state["user_profile"]["climate"]))
    
    # Update profile
    st.session_state["user_profile"].update({
        "weight": weight,
        "activity_level": activity_level,
        "climate": climate
    })
    
    # Calculate recommended intake
    recommended_ml = calculate_recommended_intake(weight, activity_level, climate)
    
    st.markdown(f"""
    <div class="metric-card">
        <h4>💡 Recommended Daily Intake</h4>
        <h2>{recommended_ml} ml</h2>
        <p>Based on your profile</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom target option
    st.subheader("🎯 Daily Target")
    use_recommended = st.checkbox("Use recommended intake", value=True)
    
    if use_recommended:
        st.session_state["daily_target"] = recommended_ml
    else:
        custom_target = st.number_input("Custom target (ml)", 1000, 5000, recommended_ml, 50)
        st.session_state["daily_target"] = custom_target
    
    # Quick add buttons
    st.subheader("⚡ Quick Add")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💧 250ml"):
            today = datetime.date.today().isoformat()
            st.session_state["hydration_log"][today] = st.session_state["hydration_log"].get(today, 0) + 250
    with col2:
        if st.button("🥤 500ml"):
            today = datetime.date.today().isoformat()
            st.session_state["hydration_log"][today] = st.session_state["hydration_log"].get(today, 0) + 500

# ---- Main Content Area ----
col1, col2, col3 = st.columns([2, 1, 2])

# Left Column - Today's Progress
with col1:
    st.subheader("📊 Today's Hydration")
    
    today = datetime.date.today().isoformat()
    current_intake = st.session_state["hydration_log"].get(today, 0)
    target = st.session_state["daily_target"]
    percentage = (current_intake / target) * 100 if target > 0 else 0
    
    # Progress wave
    st.markdown('<div class="wave-container">', unsafe_allow_html=True)
    st.markdown(create_wave_progress(percentage), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Status
    status, color, emoji = get_hydration_status(current_intake, target)
    st.markdown(f"""
    <div style="background: {color}; padding: 1rem; border-radius: 10px; text-align: center; color: white; margin: 1rem 0;">
        <h3>{emoji} {status}</h3>
        <p>{current_intake} ml / {target} ml</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Manual input
    st.subheader("➕ Add Intake")
    intake_amount = st.number_input("Amount (ml)", 0, 2000, 250, 25, key="manual_input")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Add Intake", type="primary"):
            st.session_state["hydration_log"][today] = current_intake + intake_amount
            st.success(f"Added {intake_amount}ml! 🎉")
            st.rerun()
    
    with col_btn2:
        if st.button("Reset Today", type="secondary"):
            if today in st.session_state["hydration_log"]:
                del st.session_state["hydration_log"][today]
            st.warning("Today's intake reset!")
            st.rerun()

# Middle Column - Quick Stats
with col2:
    st.subheader("📈 Quick Stats")
    
    # Get last 7 days data
    dates = [(datetime.date.today() - timedelta(days=i)).isoformat() for i in range(7)]
    intakes = [st.session_state["hydration_log"].get(date, 0) for date in dates]
    
    avg_intake = np.mean([x for x in intakes if x > 0]) if any(intakes) else 0
    max_intake = max(intakes) if intakes else 0
    streak = 0
    
    # Calculate streak
    for intake in reversed(intakes):
        if intake >= target * 0.8:  # 80% of target counts as success
            streak += 1
        else:
            break
    
    st.markdown(f"""
    <div class="achievement-badge">
        <h4>🔥 Current Streak</h4>
        <h2>{streak} days</h2>
    </div>
    
    <div class="achievement-badge">
        <h4>📊 7-Day Average</h4>
        <h2>{avg_intake:.0f} ml</h2>
    </div>
    
    <div class="achievement-badge">
        <h4>🏆 Personal Best</h4>
        <h2>{max_intake} ml</h2>
    </div>
    """, unsafe_allow_html=True)

# Right Column - Analytics
with col3:
    st.subheader("📈 Weekly Trends")
    
    if any(intakes):
        # Create trend chart
        df = pd.DataFrame({
            'Date': [datetime.datetime.fromisoformat(date).strftime('%a %m/%d') for date in reversed(dates)],
            'Intake': list(reversed(intakes)),
            'Target': [target] * 7
        })
        
        fig = go.Figure()
        
        # Add intake bars
        fig.add_trace(go.Bar(
            x=df['Date'],
            y=df['Intake'],
            name='Daily Intake',
            marker_color='lightblue',
            opacity=0.7
        ))
        
        # Add target line
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Target'],
            mode='lines',
            name='Target',
            line=dict(color='red', width=3, dash='dash')
        ))
        
        fig.update_layout(
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Start logging your water intake to see trends! 💧")

# ---- Bottom Section - Detailed History ----
st.markdown("---")
st.subheader("📅 Detailed History")

if st.session_state["hydration_log"]:
    # Create comprehensive history dataframe
    all_dates = sorted(st.session_state["hydration_log"].keys(), reverse=True)
    history_data = []
    
    for date in all_dates[:14]:  # Last 14 days
        intake = st.session_state["hydration_log"][date]
        date_obj = datetime.datetime.fromisoformat(date)
        percentage = (intake / target) * 100
        status, _, emoji = get_hydration_status(intake, target)
        
        history_data.append({
            'Date': date_obj.strftime('%A, %B %d'),
            'Intake (ml)': intake,
            'Target (ml)': target,
            'Achievement': f"{percentage:.1f}%",
            'Status': f"{emoji} {status}"
        })
    
    df_history = pd.DataFrame(history_data)
    st.dataframe(df_history, use_container_width=True, hide_index=True)
    
    # Export option
    if st.button("📊 Export Data as CSV"):
        csv = df_history.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"hydration_log_{datetime.date.today()}.csv",
            mime="text/csv"
        )
else:
    st.info("No hydration data yet. Start tracking your water intake! 🌊")

# ---- Motivational Footer ----
st.markdown("---")
motivational_quotes = [
    "💧 Water is life - drink up!",
    "🌊 Stay hydrated, stay healthy!",
    "💦 Every drop counts toward your goal!",
    "🥤 Hydration is the foundation of wellness!",
    "⚡ Fuel your body with pure H2O!"
]

current_hour = datetime.datetime.now().hour
quote_index = current_hour % len(motivational_quotes)

st.markdown(f"""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
           border-radius: 15px; color: white; margin-top: 2rem;">
    <h3>{motivational_quotes[quote_index]}</h3>
    <p>Keep up the great work on your hydration journey! 🎯</p>
</div>
""", unsafe_allow_html=True)