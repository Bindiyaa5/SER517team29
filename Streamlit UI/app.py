import streamlit as st

# Custom CSS for buttons
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
    font-weight: bold;
}
.streamlit-button{
    height: 3em;
    width: 10em;
    border-radius:10px;
    border: 2px solid #4CAF50;
    color: white;
    background-color: #4CAF50;
}
</style>
""", unsafe_allow_html=True)

def main_page():
    st.title('Scooter Usage Dashboard')

    col1, col2, col3 = st.columns(3)  # Updated to st.columns from st.beta_columns

    with col1:
        if st.button('Classic Bikes', key='classic'):
            st.write('Classic Bikes selected.')
            # Navigate to Classic Bikes page or functionality
    
    with col2:
        if st.button('Electric Bikes', key='electric'):
            st.write('Electric Bikes selected.')
            # Navigate to Electric Bikes page or functionality
    
    with col3:
        if st.button('Comparison Trends', key='comparison'):
            st.write('Comparison Trends selected.')
            # Navigate to Comparison Trends page or functionality

if __name__ == '__main__':
    main_page()
