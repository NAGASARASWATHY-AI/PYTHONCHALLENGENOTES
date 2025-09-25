import streamlit as st

# Static exchange rates (relative to USD as base)
EXCHANGE_RATES = {
    'USD': 1.0,      # Base currency
    'EUR': 0.85,     # 1 USD = 0.85 EUR
    'GBP': 0.73,     # 1 USD = 0.73 GBP
    'INR': 83.25,    # 1 USD = 83.25 INR
    'JPY': 110.0,    # 1 USD = 110 JPY
    'CAD': 1.25,     # 1 USD = 1.25 CAD
    'AUD': 1.35,     # 1 USD = 1.35 AUD
    'CHF': 0.92,     # 1 USD = 0.92 CHF
    'CNY': 6.45,     # 1 USD = 6.45 CNY
    'SGD': 1.35,     # 1 USD = 1.35 SGD
}

# Currency symbols for better display
CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'INR': '₹',
    'JPY': '¥',
    'CAD': 'C$',
    'AUD': 'A$',
    'CHF': 'CHF',
    'CNY': '¥',
    'SGD': 'S$',
}

def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another"""
    if from_currency == to_currency:
        return amount
    
    # Convert to USD first, then to target currency
    usd_amount = amount / EXCHANGE_RATES[from_currency]
    converted_amount = usd_amount * EXCHANGE_RATES[to_currency]
    
    return converted_amount

def main():
    st.set_page_config(
        page_title="Currency Converter",
        page_icon="💱",
        layout="centered"
    )
    
    st.title("💱 Currency Converter")
    st.markdown("Convert between different currencies using static exchange rates")
    
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("From")
        from_currency = st.selectbox(
            "Select source currency:",
            options=list(EXCHANGE_RATES.keys()),
            index=list(EXCHANGE_RATES.keys()).index('USD')
        )
        
        amount = st.number_input(
            f"Enter amount in {from_currency}:",
            min_value=0.0,
            value=100.0,
            step=0.01,
            format="%.2f"
        )
    
    with col2:
        st.subheader("To")
        to_currency = st.selectbox(
            "Select target currency:",
            options=list(EXCHANGE_RATES.keys()),
            index=list(EXCHANGE_RATES.keys()).index('INR')
        )
    
    # Convert button
    if st.button("🔄 Convert", type="primary"):
        if amount > 0:
            converted_amount = convert_currency(amount, from_currency, to_currency)
            
            # Display result in a nice format
            st.success(f"""
            **Conversion Result:**
            
            {CURRENCY_SYMBOLS.get(from_currency, '')}{amount:,.2f} {from_currency} 
            = 
            {CURRENCY_SYMBOLS.get(to_currency, '')}{converted_amount:,.2f} {to_currency}
            """)
            
            # Show exchange rate used
            if from_currency != to_currency:
                rate = EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency]
                st.info(f"Exchange Rate: 1 {from_currency} = {rate:.4f} {to_currency}")
        else:
            st.warning("Please enter an amount greater than 0")
    
    # Display exchange rates table
    st.markdown("---")
    st.subheader("📊 Current Exchange Rates (Base: USD)")
    
    # Create a nice table of exchange rates
    rate_data = []
    for currency, rate in EXCHANGE_RATES.items():
        if currency != 'USD':
            rate_data.append({
                'Currency': f"{CURRENCY_SYMBOLS.get(currency, '')} {currency}",
                'Rate (1 USD =)': f"{rate:.4f} {currency}"
            })
    
    st.table(rate_data)
    
    # Add disclaimer
    st.markdown("---")
    st.caption("⚠️ **Disclaimer:** These are static exchange rates for demonstration purposes only. For real transactions, please use current market rates from a reliable financial source.")

if __name__ == "__main__":
    main()