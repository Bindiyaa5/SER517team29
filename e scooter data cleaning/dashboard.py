# dashboard.py

import streamlit as st
import pandas as pd
from escooterAnalysis import load_data, summary_statistics, plot_histogram, correlation_matrix

def load_data_cache(file_path):
    return load_data(file_path)

# Sidebar
st.sidebar.title('Dashboard Options')

# Selectbox for selecting analysis
analysis_option = st.sidebar.selectbox('Select Analysis', ('Summary', 'Histogram', 'Correlation'))

# Main content
st.title('E-scooter trips data analysis dashboard')

# Load data
file_path = 'cleaned_e_scooter_trip_data.csv'
data = load_data_cache(file_path)

if analysis_option == 'Summary':
    st.write('## Summary Statistics')
    st.write(summary_statistics(data))

elif analysis_option == 'Histogram':
    st.write('## Histogram')
    selected_column = st.selectbox('Select Column for Histogram', data.columns)
    plot = plot_histogram(data, selected_column)
    st.pyplot(plot)

elif analysis_option == 'Correlation':
    st.write('## Correlation Matrix')
    corr_matrix = correlation_matrix(data)
    st.write(corr_matrix)



