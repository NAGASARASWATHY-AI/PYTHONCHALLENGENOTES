# Simple Calculator App using Streamlit
# Import the streamlit library
import streamlit as st

# Set the page configuration (optional but good practice)
st.set_page_config(
    page_title="Simple Calculator",  # Title shown in browser tab
    page_icon="🧮",                  # Icon shown in browser tab
    layout="centered"                # Layout of the app
)

# Main title of the app
st.title("🧮 Simple Calculator")
st.write("Welcome to our simple calculator app!")

# Create a horizontal line separator for better visual organization
st.divider()

# INPUT SECTION
# Create two columns for better layout of input fields
col1, col2 = st.columns(2)

# First number input (placed in first column)
with col1:
    # number_input creates a numeric input field
    # value=0.0 sets the default value
    # step=0.1 allows decimal inputs
    num1 = st.number_input(
        label="Enter first number:",
        value=0.0,
        step=0.1,
        help="Enter any number (integers or decimals)"
    )

# Second number input (placed in second column)
with col2:
    num2 = st.number_input(
        label="Enter second number:",
        value=0.0,
        step=0.1,
        help="Enter any number (integers or decimals)"
    )

# OPERATION SELECTION
st.subheader("Choose Operation:")

# Create four columns for operation buttons
col1, col2, col3, col4 = st.columns(4)

# Initialize result variable
result = None
operation_performed = None

# Addition button
with col1:
    if st.button("➕ Add", use_container_width=True):
        result = num1 + num2
        operation_performed = "Addition"

# Subtraction button
with col2:
    if st.button("➖ Subtract", use_container_width=True):
        result = num1 - num2
        operation_performed = "Subtraction"

# Multiplication button
with col3:
    if st.button("✖️ Multiply", use_container_width=True):
        result = num1 * num2
        operation_performed = "Multiplication"

# Division button
with col4:
    if st.button("➗ Divide", use_container_width=True):
        # Check for division by zero
        if num2 != 0:
            result = num1 / num2
            operation_performed = "Division"
        else:
            # Show error message if trying to divide by zero
            st.error("❌ Error: Cannot divide by zero!")
            result = None

# RESULT DISPLAY SECTION
st.divider()

# Display result if an operation was performed
if result is not None and operation_performed:
    st.subheader("📊 Result:")
    
    # Create a success message box with the result
    st.success(f"**{operation_performed}**: {num1} and {num2} = **{result:.2f}**")
    
    # Additional information in an info box
    st.info(f"Operation performed: {operation_performed}")
    
    # Show raw result for precision
    with st.expander("Show detailed result"):
        st.write(f"Exact result: {result}")
        st.write(f"Rounded to 2 decimal places: {result:.2f}")
        st.write(f"Rounded to 4 decimal places: {result:.4f}")

# ADDITIONAL FEATURES SECTION
st.divider()
st.subheader("💡 Additional Features:")

# History section (simple display)
if st.checkbox("Show calculation summary"):
    if result is not None and operation_performed:
        st.write("**Last Calculation:**")
        st.code(f"{num1} {'+' if operation_performed == 'Addition' else '-' if operation_performed == 'Subtraction' else '*' if operation_performed == 'Multiplication' else '/'} {num2} = {result}")
    else:
        st.write("No calculation performed yet.")

# Clear button
if st.button("🗑️ Clear All", type="secondary"):
    # Rerun the app to reset all values
    st.rerun()

# FOOTER SECTION
st.divider()
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Simple Calculator App")

# Sidebar with instructions (optional)
with st.sidebar:
    st.header("📖 How to Use:")
    st.write("""
    1. Enter your first number
    2. Enter your second number  
    3. Click on any operation button
    4. View your result below!
    
    **Features:**
    - Supports decimal numbers
    - Division by zero protection
    - Detailed result display
    - Clean, responsive design
    """)
    
    st.header("🔧 About:")
    st.write("""
    This is a simple calculator built with Streamlit, 
    perfect for basic arithmetic operations.
    """)