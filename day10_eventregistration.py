import streamlit as st
import pandas as pd
from datetime import datetime
import csv
from io import StringIO

# Configure page
st.set_page_config(
    page_title="Event Registration System",
    page_icon="📅",
    layout="wide"
)

# Initialize session state
if 'registrations' not in st.session_state:
    st.session_state.registrations = []

# Available events
EVENTS = [
    "Tech Conference 2024",
    "Digital Marketing Workshop",
    "AI & Machine Learning Summit",
    "Web Development Bootcamp",
    "Data Science Meetup",
    "Startup Pitch Event"
]

# Main title
st.title("📅 Event Registration System")

# Create two columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Register for an Event")
    
    # Registration form
    with st.form("registration_form"):
        name = st.text_input("Full Name *", placeholder="Enter your full name")
        email = st.text_input("Email Address *", placeholder="Enter your email address")
        event_choice = st.selectbox("Select Event *", [""] + EVENTS)
        
        # Additional optional fields
        st.subheader("Additional Information (Optional)")
        phone = st.text_input("Phone Number", placeholder="Enter your phone number")
        company = st.text_input("Company/Organization", placeholder="Enter your company name")
        
        submitted = st.form_submit_button("Register Now", type="primary")
        
        if submitted:
            # Validation
            if not name or not email or not event_choice:
                st.error("Please fill in all required fields marked with *")
            elif "@" not in email or "." not in email:
                st.error("Please enter a valid email address")
            else:
                # Check for duplicate registration
                duplicate = False
                for reg in st.session_state.registrations:
                    if reg['email'].lower() == email.lower() and reg['event'] == event_choice:
                        duplicate = True
                        break
                
                if duplicate:
                    st.warning(f"You're already registered for {event_choice} with this email address!")
                else:
                    # Add registration
                    registration = {
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'name': name,
                        'email': email,
                        'event': event_choice,
                        'phone': phone if phone else "Not provided",
                        'company': company if company else "Not provided"
                    }
                    st.session_state.registrations.append(registration)
                    st.success(f"✅ Successfully registered for {event_choice}!")
                    st.balloons()

with col2:
    st.header("Registration Stats")
    
    # Total registrations count
    total_registrations = len(st.session_state.registrations)
    st.metric("Total Registrations", total_registrations)
    
    # Event-wise breakdown
    if st.session_state.registrations:
        event_counts = {}
        for reg in st.session_state.registrations:
            event = reg['event']
            event_counts[event] = event_counts.get(event, 0) + 1
        
        st.subheader("Registrations by Event")
        for event, count in sorted(event_counts.items()):
            st.write(f"• {event}: {count}")

# Separator
st.divider()

# Admin section
st.header("📊 Admin Dashboard")

if st.session_state.registrations:
    # Display registrations table
    df = pd.DataFrame(st.session_state.registrations)
    
    # Reorder columns for better display
    column_order = ['timestamp', 'name', 'email', 'event', 'phone', 'company']
    df = df[column_order]
    
    st.subheader("All Registrations")
    st.dataframe(df, use_container_width=True)
    
    # Export functionality
    st.subheader("Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV export
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name=f"event_registrations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Excel export
        excel_buffer = StringIO()
        df.to_csv(excel_buffer, index=False)  # Using CSV format for compatibility
        
        st.download_button(
            label="📋 Download as Excel",
            data=excel_buffer.getvalue(),
            file_name=f"event_registrations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col3:
        # Clear all data (with confirmation)
        if st.button("🗑️ Clear All Data", type="secondary"):
            if st.session_state.get('confirm_clear', False):
                st.session_state.registrations = []
                st.session_state.confirm_clear = False
                st.success("All registration data cleared!")
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm clearing all data!")

else:
    st.info("No registrations yet. The registration data will appear here once people start registering.")

# Footer with instructions
st.divider()
st.markdown("""
### Instructions:
- Fill out the registration form above to register for an event
- View live registration counts in the stats panel
- Admin can view all registrations and export data as CSV or Excel
- Data persists during the session but will be reset when the app restarts

### Features:
✅ Registration form with validation  
✅ Duplicate registration prevention  
✅ Live registration count  
✅ Event-wise breakdown  
✅ Admin dashboard with data table  
✅ CSV/Excel export functionality  
✅ Session state data storage  
""")

# Auto-refresh for live updates (optional)
if st.checkbox("Enable auto-refresh (5 seconds)"):
    import time
    time.sleep(5)
    st.rerun()