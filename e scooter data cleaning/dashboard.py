# dashboard.py

import streamlit as st
import pandas as pd
from new import load_data, summary_statistics

def load_data_cache(file_path):
    return load_data(file_path)

# Sidebar
st.sidebar.title('Dashboard Options')

# Selectbox for selecting analysis
analysis_option = st.sidebar.selectbox('Select Analysis', ('Summary', 'Histogram', 'Correlation'))

# Main content
st.title('Data Analysis Dashboard')

# Load data
file_path = 'cleaned_e_scooter_trip_data.csv'
data = load_data_cache(file_path)

if analysis_option == 'Summary':
    st.write('## Summary Statistics')
    st.write(summary_statistics(data))