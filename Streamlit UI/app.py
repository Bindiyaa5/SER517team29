import streamlit as st

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'main'

def navigate(page):
    st.session_state.page = page

# Navigation function
def show_page():
    if st.session_state.page == 'main':
        main_page()
    elif st.session_state.page == 'classic_bikes':
        classic_bikes_page()
    # Add more pages as elif blocks

# Main page with buttons
def main_page():
    st.title('Scooter Usage Dashboard')
    
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button('Classic Bikes'):
            navigate('classic_bikes')
    
    # Setup buttons for Electric Bikes and Comparison Trends similarly

def classic_bikes_page():
    st.title('Classic Bikes Analysis')

    # Placeholder for visualizations
    st.header('1. Usage Trends Over Time')
    # Insert code to display the visualization
    
    st.header('2. Average Time Duration and Distance')
    # Insert code to display the visualization
    
    st.header('3. Popular Areas of Start and End Points')
    # Insert code to display the visualization
    
    st.header('4. Operational Insights')
    # Insert code to display the visualization

# Show the current page
show_page()
