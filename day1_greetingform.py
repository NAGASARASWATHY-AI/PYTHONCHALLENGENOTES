# Import the streamlit library
import streamlit as st

# Set up the page configuration
st.set_page_config(
    page_title="Greeting App",
    page_icon="👋",
    layout="centered"
)

# Add a title to the app
st.title("👋 Personal Greeting Generator")

# Add a brief description
st.write("Welcome! Please fill out the form below to receive a personalized greeting.")

# Create a form to group the input elements
with st.form("greeting_form"):
    # Text input for the user's name
    name = st.text_input("Enter your name:", placeholder="Type your name here...")
    
    # Slider input for the user's age
    age = st.slider("Select your age:", min_value=0, max_value=100, value=25)
    
    # Submit button for the form
    submitted = st.form_submit_button("Generate Greeting")

# Check if the form has been submitted
if submitted:
    # Validate that a name was entered
    if name.strip():  # Check if name is not empty after removing whitespace
        # Create a personalized greeting message
        greeting = f"Hello, {name}! 👋"
        age_message = f"Wow, {age} years young! "
        
        # Add a special message based on age
        if age < 18:
            age_message += "You're full of potential! 🌟"
        elif age < 30:
            age_message += "The world is your oyster! 🌍"
        elif age < 50:
            age_message += "You're in your prime! 💪"
        else:
            age_message += "Wisdom comes with age! 📚"
        
        # Display the greeting and age message
        st.success(greeting)
        st.info(age_message)
        
        # Add some celebratory emojis based on age
        if age < 12:
            st.write("🎂🎈🦄 Have an amazing day!")
        else:
            st.write("🎉✨😊 Have a wonderful day!")
    else:
        # Show an error if no name was entered
        st.error("Please enter your name to generate a greeting.")