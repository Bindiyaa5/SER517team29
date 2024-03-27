import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk  # Assuming advanced mapping might be used

# Replace 'cols' with the actual columns you're using from your CSV
cols = ['ride_id', 'rideable_type', 'started_at', 'ended_at', 'start_station_name', 'start_station_id',
        'end_station_name', 'end_station_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng',
        'member_casual', 'trip_duration_minutes']

@st.cache_data
def load_bikes_data(filename):
    # Loading data with specified columns for efficiency
    return pd.read_csv(filename, usecols=cols)

def haversine_vectorized(df):
    # Ensure your data includes these columns, or adjust as necessary
    lon1, lat1, lon2, lat2 = map(np.radians, [df['start_lng'], df['start_lat'], df['end_lng'], df['end_lat']])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6371 * c
    return km

def prepare_data(df):
    if 'started_at' in df.columns:
        df['started_at'] = pd.to_datetime(df['started_at'])
        df['ended_at'] = pd.to_datetime(df['ended_at'])
        df['duration_minutes'] = df['trip_duration_minutes'].astype(float)
        df['hour_started'] = df['started_at'].dt.hour
        df['distance_km'] = haversine_vectorized(df)
        return df
    else:
        st.error("Missing 'started_at' column in the dataset.")
        return None

def monthly_peak_usage_hours(df):
    if 'started_at' not in df.columns:
        st.error("The 'started_at' column is missing.")
        return

    df['month'] = df['started_at'].dt.month_name()
    monthly_hourly_counts = df.groupby(['month', 'hour_started']).size().unstack(fill_value=0)
    months_list = monthly_hourly_counts.index.tolist()
    selected_months = st.multiselect('Select months to display', options=months_list, default=months_list)

    if selected_months:
        filtered_counts = monthly_hourly_counts.loc[selected_months]
        st.line_chart(filtered_counts)
    else:
        st.write("Please select at least one month to display usage hours.")

def visualize_data(df, bike_type):
    df_prepared = prepare_data(df)
    if df_prepared is not None:
        st.header(f"{bike_type} Bikes Data Analysis")
        monthly_peak_usage_hours(df_prepared)
        # You can add more visualization functions here as needed

def main():
    st.sidebar.title("Bike Sharing Data Analysis")
    selection = st.sidebar.radio("Choose a view", ["Normal Bikes", "Electric Bikes", "Comparison"])

    if selection == "Normal Bikes":
        df_normal = load_bikes_data('normal_bikes.csv')
        visualize_data(df_normal, "Normal")
    elif selection == "Electric Bikes":
        df_electric = load_bikes_data('electric_bikes.csv')
        visualize_data(df_electric, "Electric")
    elif selection == "Comparison":
        st.write("Comparison view is under construction.")  # Placeholder for comparison logic

if __name__ == "__main__":
    main()
