import streamlit as st
import pandas as pd
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# Configure page
st.set_page_config(page_title="Restaurant Order & Billing App 🍔", layout="wide")

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'order_history' not in st.session_state:
    st.session_state.order_history = []

# Restaurant menu data
MENU = {
    "🍔 Burgers": {
        "Classic Burger": 12.99,
        "Cheeseburger": 14.99,
        "Bacon Deluxe": 16.99,
        "Veggie Burger": 13.99,
        "Double Whopper": 19.99
    },
    "🍕 Pizza": {
        "Margherita": 15.99,
        "Pepperoni": 17.99,
        "Supreme": 21.99,
        "Hawaiian": 18.99,
        "Veggie Delight": 19.99
    },
    "🍝 Pasta": {
        "Spaghetti Carbonara": 16.99,
        "Chicken Alfredo": 18.99,
        "Penne Arrabbiata": 15.99,
        "Lasagna": 19.99,
        "Seafood Linguine": 22.99
    },
    "🥗 Salads": {
        "Caesar Salad": 11.99,
        "Greek Salad": 12.99,
        "Cobb Salad": 14.99,
        "Quinoa Bowl": 13.99,
        "Garden Fresh": 10.99
    },
    "🥤 Beverages": {
        "Soft Drink": 2.99,
        "Fresh Juice": 4.99,
        "Coffee": 3.99,
        "Beer": 5.99,
        "Wine (Glass)": 7.99
    },
    "🍰 Desserts": {
        "Chocolate Cake": 7.99,
        "Tiramisu": 8.99,
        "Ice Cream": 5.99,
        "Cheesecake": 8.99,
        "Apple Pie": 6.99
    }
}

# Tax rate (adjustable)
TAX_RATE = 0.08  # 8%

def add_to_cart(item, price, quantity):
    """Add item to cart"""
    if quantity > 0:
        if item in st.session_state.cart:
            st.session_state.cart[item]['quantity'] += quantity
        else:
            st.session_state.cart[item] = {'price': price, 'quantity': quantity}

def remove_from_cart(item):
    """Remove item from cart"""
    if item in st.session_state.cart:
        del st.session_state.cart[item]

def calculate_totals():
    """Calculate subtotal, tax, and total"""
    subtotal = sum(item['price'] * item['quantity'] for item in st.session_state.cart.values())
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    return subtotal, tax, total

def generate_csv():
    """Generate CSV invoice"""
    if not st.session_state.cart:
        return None
    
    subtotal, tax, total = calculate_totals()
    
    # Create order data
    order_data = []
    for item, details in st.session_state.cart.items():
        order_data.append({
            'Item': item,
            'Price': f"${details['price']:.2f}",
            'Quantity': details['quantity'],
            'Subtotal': f"${details['price'] * details['quantity']:.2f}"
        })
    
    # Add summary rows
    order_data.append({'Item': '', 'Price': '', 'Quantity': '', 'Subtotal': ''})
    order_data.append({'Item': 'Subtotal', 'Price': '', 'Quantity': '', 'Subtotal': f"${subtotal:.2f}"})
    order_data.append({'Item': f'Tax ({TAX_RATE*100}%)', 'Price': '', 'Quantity': '', 'Subtotal': f"${tax:.2f}"})
    order_data.append({'Item': 'TOTAL', 'Price': '', 'Quantity': '', 'Subtotal': f"${total:.2f}"})
    
    df = pd.DataFrame(order_data)
    return df.to_csv(index=False)

def generate_pdf():
    """Generate PDF invoice"""
    if not st.session_state.cart:
        return None
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Header
    story.append(Paragraph("🍔 Restaurant Invoice", title_style))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Order details
    subtotal, tax, total = calculate_totals()
    
    # Create table data
    table_data = [['Item', 'Price', 'Qty', 'Subtotal']]
    
    for item, details in st.session_state.cart.items():
        table_data.append([
            item,
            f"${details['price']:.2f}",
            str(details['quantity']),
            f"${details['price'] * details['quantity']:.2f}"
        ])
    
    # Add summary rows
    table_data.append(['', '', '', ''])
    table_data.append(['Subtotal', '', '', f"${subtotal:.2f}"])
    table_data.append([f'Tax ({TAX_RATE*100}%)', '', '', f"${tax:.2f}"])
    table_data.append(['TOTAL', '', '', f"${total:.2f}"])
    
    # Create table
    table = Table(table_data, colWidths=[3*inch, 1*inch, 0.5*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    doc.build(story)
    
    buffer.seek(0)
    return buffer

# Main app
def main():
    st.title("🍔 Restaurant Order & Billing App")
    st.markdown("---")
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📋 Menu")
        
        # Display menu by category
        for category, items in MENU.items():
            st.subheader(category)
            
            # Create columns for each item in the category
            item_cols = st.columns(len(items))
            
            for idx, (item, price) in enumerate(items.items()):
                with item_cols[idx]:
                    st.write(f"**{item}**")
                    st.write(f"${price:.2f}")
                    
                    # Quantity selector
                    quantity = st.number_input(
                        f"Qty",
                        min_value=0,
                        max_value=10,
                        value=0,
                        key=f"{item}_qty",
                        help=f"Add {item} to cart"
                    )
                    
                    # Add to cart button
                    if st.button(f"Add to Cart", key=f"{item}_btn"):
                        if quantity > 0:
                            add_to_cart(item, price, quantity)
                            st.success(f"Added {quantity}x {item} to cart!")
                            st.rerun()
            
            st.markdown("---")
    
    with col2:
        st.header("🛒 Your Order")
        
        if st.session_state.cart:
            # Display cart items
            for item, details in st.session_state.cart.items():
                col_item, col_remove = st.columns([3, 1])
                with col_item:
                    st.write(f"**{item}**")
                    st.write(f"${details['price']:.2f} × {details['quantity']} = ${details['price'] * details['quantity']:.2f}")
                with col_remove:
                    if st.button("❌", key=f"remove_{item}", help=f"Remove {item}"):
                        remove_from_cart(item)
                        st.rerun()
            
            st.markdown("---")
            
            # Calculate totals
            subtotal, tax, total = calculate_totals()
            
            # Bill summary
            st.subheader("💰 Bill Summary")
            st.write(f"**Subtotal:** ${subtotal:.2f}")
            st.write(f"**Tax ({TAX_RATE*100}%):** ${tax:.2f}")
            st.write(f"**TOTAL:** ${total:.2f}")
            
            st.markdown("---")
            
            # Download options
            st.subheader("📥 Download Invoice")
            
            col_csv, col_pdf = st.columns(2)
            
            with col_csv:
                csv_data = generate_csv()
                if csv_data:
                    st.download_button(
                        label="📄 Download CSV",
                        data=csv_data,
                        file_name=f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            with col_pdf:
                pdf_data = generate_pdf()
                if pdf_data:
                    st.download_button(
                        label="📑 Download PDF",
                        data=pdf_data.getvalue(),
                        file_name=f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
            
            # Clear cart button
            st.markdown("---")
            if st.button("🗑️ Clear Cart", type="secondary"):
                st.session_state.cart = {}
                st.rerun()
                
        else:
            st.info("Your cart is empty. Add some items from the menu!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        🍔 Restaurant Order & Billing App | Made with Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()