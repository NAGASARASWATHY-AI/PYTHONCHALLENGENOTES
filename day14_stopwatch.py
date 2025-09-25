import streamlit as st
import time
from datetime import datetime, timedelta

def format_time(seconds):
    """Format seconds into MM:SS.ms format"""
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:06.3f}"

def main():
    st.title("⏱️ Stopwatch Timer")
    st.markdown("---")
    
    # Initialize session state variables
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = 0.0
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
    if 'lap_times' not in st.session_state:
        st.session_state.lap_times = []
    
    # Calculate current elapsed time
    if st.session_state.is_running and st.session_state.start_time:
        current_elapsed = st.session_state.elapsed_time + (time.time() - st.session_state.start_time)
    else:
        current_elapsed = st.session_state.elapsed_time
    
    # Display the timer
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; font-size: 3rem; font-weight: bold; 
                    background: linear-gradient(90deg, #FF6B6B, #4ECDC4); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    padding: 20px; border-radius: 10px; margin: 20px 0;'>
            {format_time(current_elapsed)}
        </div>
        """, unsafe_allow_html=True)
    
    # Control buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("▶️ Start", disabled=st.session_state.is_running, use_container_width=True):
            st.session_state.is_running = True
            st.session_state.start_time = time.time()
            st.rerun()
    
    with col2:
        if st.button("⏸️ Stop", disabled=not st.session_state.is_running, use_container_width=True):
            if st.session_state.start_time:
                st.session_state.elapsed_time += time.time() - st.session_state.start_time
            st.session_state.is_running = False
            st.session_state.start_time = None
            st.rerun()
    
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.start_time = None
            st.session_state.elapsed_time = 0.0
            st.session_state.is_running = False
            st.session_state.lap_times = []
            st.rerun()
    
    with col4:
        if st.button("🏁 Lap", disabled=not st.session_state.is_running, use_container_width=True):
            lap_time = current_elapsed
            st.session_state.lap_times.append(lap_time)
            st.rerun()
    
    # Auto-refresh when running
    if st.session_state.is_running:
        time.sleep(0.1)
        st.rerun()
    
    # Display lap times
    if st.session_state.lap_times:
        st.markdown("---")
        st.subheader("🏁 Lap Times")
        
        for i, lap_time in enumerate(reversed(st.session_state.lap_times), 1):
            lap_num = len(st.session_state.lap_times) - i + 1
            st.markdown(f"**Lap {lap_num}:** {format_time(lap_time)}")
    
    # Status indicator
    st.markdown("---")
    status_color = "🟢" if st.session_state.is_running else "🔴"
    status_text = "Running" if st.session_state.is_running else "Stopped"
    st.markdown(f"**Status:** {status_color} {status_text}")
    
    # Instructions
    with st.expander("📖 Instructions"):
        st.markdown("""
        - **Start**: Begin timing
        - **Stop**: Pause the timer (can be resumed)
        - **Reset**: Clear all times and return to 00:00.000
        - **Lap**: Record current time while continuing to run
        
        The timer displays time in MM:SS.mmm format (minutes:seconds.milliseconds).
        """)

if __name__ == "__main__":
    main()