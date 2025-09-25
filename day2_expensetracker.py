import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Fair Expense Splitter",
    page_icon="💰",
    layout="centered"
)

# App title and description
st.title("💰 Fair Expense Splitter")
st.write("Easily split expenses among friends after a dinner or trip!")

# Initialize session state for storing people and their contributions
if 'people' not in st.session_state:
    st.session_state.people = []

# Input section for basic information
st.header("📊 Basic Information")
total_amount = st.number_input("Total Amount Spent:", min_value=0.0, value=0.0, step=1.0, format="%.2f")
num_people = st.number_input("Number of People:", min_value=1, value=2, step=1)

# Radio button for split type
split_type = st.radio(
    "How would you like to split the expenses?",
    ["Equal Split", "Contribution Based Split"],
    horizontal=True
)

if split_type == "Contribution Based Split":
    st.header("👥 Individual Contributions")
    st.write("Enter each person's name and how much they contributed.")
    
    # Create a compact form for inputs
    for i in range(num_people):
        # Use columns to create a compact horizontal layout
        cols = st.columns([2, 1])
        with cols[0]:
            name = st.text_input(f"Person {i+1} Name:", value=f"Friend {i+1}", key=f"name_{i}")
        with cols[1]:
            contribution = st.number_input(
                f"Amount:", 
                min_value=0.0, 
                value=0.0, 
                step=1.0, 
                format="%.2f",
                key=f"contribution_{i}"
            )
        
        # Store person data
        if i < len(st.session_state.people):
            st.session_state.people[i] = {"name": name, "contribution": contribution}
        else:
            st.session_state.people.append({"name": name, "contribution": contribution})
    
    # Ensure we have exactly num_people entries
    st.session_state.people = st.session_state.people[:num_people]
    
    # Calculate button
    if st.button("Calculate Fair Share", type="primary"):
        # Calculate fair share per person
        fair_share = total_amount / num_people
        
        # Calculate each person's balance
        balances = []
        total_contributed = sum(person["contribution"] for person in st.session_state.people)
        
        for person in st.session_state.people:
            balance = person["contribution"] - fair_share
            balances.append({
                "name": person["name"],
                "contributed": person["contribution"],
                "fair_share": fair_share,
                "balance": balance
            })
        
        # Check if total contributions match total amount
        if abs(total_contributed - total_amount) > 0.01:
            st.error(f"⚠️ The total contributed (${total_contributed:.2f}) doesn't match the total amount (${total_amount:.2f}). Please adjust the contributions.")
        else:
            # Display results
            st.header("📋 Results")
            
            # Show summary
            st.subheader("Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Amount", f"${total_amount:.2f}")
            with col2:
                st.metric("Number of People", num_people)
            with col3:
                st.metric("Fair Share Each", f"${fair_share:.2f}")
            
            # Show detailed results
            st.subheader("Individual Balances")
            for balance in balances:
                if balance["balance"] > 0:
                    st.success(f"**{balance['name']}** should receive **${balance['balance']:.2f}** (contributed ${balance['contributed']:.2f})")
                elif balance["balance"] < 0:
                    st.error(f"**{balance['name']}** should pay **${abs(balance['balance']):.2f}** (contributed ${balance['contributed']:.2f})")
                else:
                    st.info(f"**{balance['name']}** is all settled! (contributed exactly ${balance['contributed']:.2f})")
            
            # Show transactions needed to settle up
            st.subheader("💡 Suggested Transactions")
            creditors = [b for b in balances if b["balance"] > 0]
            debtors = [b for b in balances if b["balance"] < 0]
            
            creditors.sort(key=lambda x: x["balance"], reverse=True)
            debtors.sort(key=lambda x: x["balance"])
            
            for debtor in debtors:
                debt_amount = abs(debtor["balance"])
                for creditor in creditors:
                    if creditor["balance"] > 0 and debt_amount > 0:
                        payment_amount = min(creditor["balance"], debt_amount)
                        
                        if payment_amount > 0:
                            st.write(f"**{debtor['name']}** should pay **${payment_amount:.2f}** to **{creditor['name']}**")
                            
                            # Update balances
                            creditor["balance"] -= payment_amount
                            debt_amount -= payment_amount

else:
    # Equal split mode
    if st.button("Calculate Fair Share", type="primary"):
        if total_amount <= 0:
            st.error("Please enter a valid total amount greater than zero.")
        else:
            per_person = total_amount / num_people
            
            st.header("📋 Results")
            
            # Show summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Amount", f"${total_amount:.2f}")
            with col2:
                st.metric("Number of People", num_people)
            with col3:
                st.metric("Each Person Owes", f"${per_person:.2f}")
            
            st.info(f"Each person should pay **${per_person:.2f}** to settle the total of **${total_amount:.2f}**")

# Add some tips
st.divider()
st.subheader("💡 Tips for Fair Splitting")
st.write("""
- For meals, consider using itemized splitting if some people ordered more expensive items
- For trips, account for different room types or travel arrangements
- Remember to include tax and tip in your total amount
- Use contribution based splitting when people contributed different amounts
""")