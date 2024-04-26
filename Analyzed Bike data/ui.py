import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import numpy as np

# Load the data
df = pd.read_csv(r'C:\Users\vbodavul\Downloads\Output (1).csv')

# Function to calculate daily metrics and reindex with the complete date range
def calculate_daily_metrics(df):
    # Assume df contains the relevant data
    # Convert 'started_at' to datetime if not already done
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    # Define the date range from January 2022 to December 2023
    date_range = pd.date_range(start='2022-01-01', end='2023-12-31', freq='D')
    # Calculate daily metrics and reindex with the complete date range
    metrics = df.groupby(df['started_at'].dt.date).agg(
        daily_trips=('ride_id', 'size'),
        avg_elevation_change=('Elevation_Change', 'mean'),
        avg_trip_distance=('Distance', 'mean'),
        avg_trip_duration=('trip_duration', 'mean')
    ).reindex(date_range, fill_value=0)  # Reindexing and filling missing days with zeros
    metrics.index.name = 'started_at'
    # Cap elevation changes at 3
    metrics['avg_elevation_change'] = metrics['avg_elevation_change'].clip(upper=3)
    return metrics.reset_index()

# Function to calculate hourly bike counts
def calculate_hourly_counts(df):
    # Assume df contains the relevant data
    # Extract hour from 'ended_at' column
    df['hour'] = df['ended_at'].dt.hour
    # Calculate hourly counts
    hourly_counts = df.groupby('hour').size()
    return hourly_counts

def main():
    # Calculate metrics for the entire dataset
    all_metrics = calculate_daily_metrics(df)
    hourly_counts = calculate_hourly_counts(df)

    # Sidebar
    st.sidebar.title("Bike Sharing Data Analysis")
    selection = st.sidebar.radio("Choose a view", ["Electric", "Classic", "Comparison"])

    # Main content
    if selection == "Electric" or selection == "Classic":
        st.header(f"{selection} Rideable Type Metrics")
        rideable_metrics = calculate_daily_metrics(df[df['rideable_type'] == selection.lower()])
        metric_selection = st.selectbox("Select a metric to visualize", ["Daily Trips", "Elevation Change", "Trip Distance", "Trip Duration"])
        
        if metric_selection == "Daily Trips":
            st.subheader("Daily Trips")
            fig = plt.figure(figsize=(12, 6))
            plt.plot(rideable_metrics['started_at'], rideable_metrics['daily_trips'], label=selection, marker='o')
            plt.xlabel('Date')
            plt.ylabel('Number of Trips')
            plt.title(f'Daily Trips for {selection} Rideable Type')
            plt.legend()
            st.pyplot(fig)

        elif metric_selection == "Elevation Change":
            st.subheader("Average Daily Elevation Change")
            fig = plt.figure(figsize=(12, 6))
            plt.plot(rideable_metrics['started_at'], rideable_metrics['avg_elevation_change'], label=selection, marker='o')
            plt.xlabel('Date')
            plt.ylabel('Elevation Change (meters)')
            plt.title(f'Average Daily Elevation Change for {selection} Rideable Type')
            plt.legend()
            st.pyplot(fig)

        elif metric_selection == "Trip Distance":
            st.subheader("Average Daily Trip Distance")
            fig = plt.figure(figsize=(12, 6))
            plt.plot(rideable_metrics['started_at'], rideable_metrics['avg_trip_distance'], label=selection, marker='o')
            plt.xlabel('Date')
            plt.ylabel('Distance (km)')
            plt.title(f'Average Daily Trip Distance for {selection} Rideable Type')
            plt.legend()
            st.pyplot(fig)

        elif metric_selection == "Trip Duration":
            st.subheader("Average Daily Trip Duration")
            fig = plt.figure(figsize=(12, 6))
            plt.plot(rideable_metrics['started_at'], rideable_metrics['avg_trip_duration'], label=selection, marker='o')
            plt.xlabel('Date')
            plt.ylabel('Duration (minutes)')
            plt.title(f'Average Daily Trip Duration for {selection} Rideable Type')
            plt.legend()
            st.pyplot(fig)

    elif selection == "Comparison":
        st.header("Comparison between Electric and Classic Rideable Types")
        comparison_selection = st.selectbox("Select a metric to compare", ["Daily Trips", "Elevation Change", "Trip Distance", "Trip Duration"])

        df_electric = calculate_daily_metrics(df[df['rideable_type'] == 'electric'])
        df_classic = calculate_daily_metrics(df[df['rideable_type'] == 'classic'])

        if comparison_selection == "Daily Trips":
            st.subheader("Comparison of Daily Trips")
            fig = plt.figure(figsize=(12, 6))
            plt.plot(all_metrics['started_at'], all_metrics['daily_trips'], label='All Data', marker='o')
            plt.plot(df_electric['started_at'], df_electric['daily_trips'], label='Electric', marker='o')
            plt.plot(df_classic['started_at'], df_classic['daily_trips'], label='Classic', marker='o')
            plt.xlabel('Date')
            plt.ylabel('Number of Trips')
            plt.title('Comparison of Daily Trips between Electric and Classic Rideable Types')
            plt.legend()
            st.pyplot(fig)

        elif comparison_selection == "Elevation Change":
            st.subheader("Comparison of Average Elevation Change")
            fig = plt.figure(figsize=(12, 6))
            plt.plot(all_metrics['started_at'], all_metrics['avg_elevation_change'], label='All Data', marker='o')
            plt.plot(df_electric['started_at'], df_electric['avg_elevation_change'], label='Electric', marker='o')
            plt.plot(df_classic['started_at'], df_classic['avg_elevation_change'], label='Classic', marker='o')
            plt.xlabel('Date')
            plt.ylabel('Elevation Change (meters)')
            plt.title('Comparison of Average Elevation Change between Electric and Classic Rideable Types')
            plt.legend()
            st.pyplot(fig)

        elif comparison_selection == "Trip Distance":
            st.subheader("Comparison of Average Trip Distance")
            fig = plt.figure(figsize=(12, 6))
            plt.plot(all_metrics['started_at'], all_metrics['avg_trip_distance'], label='All Data', marker='o')
            plt.plot(df_electric['started_at'], df_electric['avg_trip_distance'], label='Electric', marker='o')
            plt.plot(df_classic['started_at'], df_classic['avg_trip_distance'], label='Classic', marker='o')
            plt.xlabel('Date')
            plt.ylabel('Distance (km)')
            plt.title('Comparison of Average Trip Distance between Electric and Classic Rideable Types')
            plt.legend()
            st.pyplot(fig)

        elif comparison_selection == "Trip Duration":
            st.subheader("Comparison of Average Trip Duration")
            fig = plt.figure(figsize=(12, 6))
            plt.plot(all_metrics['started_at'], all_metrics['avg_trip_duration'], label='All Data', marker='o')
            plt.plot(df_electric['started_at'], df_electric['avg_trip_duration'], label='Electric', marker='o')
            plt.plot(df_classic['started_at'], df_classic['avg_trip_duration'], label='Classic', marker='o')
            plt.xlabel('Date')
            plt.ylabel('Duration (minutes)')
            plt.title('Comparison of Average Trip Duration between Electric and Classic Rideable Types')
            plt.legend()
            st.pyplot(fig)
        
        elif comparison_selection == "Hourly Bike Counts":
            # Hourly bike counts based on 'ended_at'
            st.subheader("Hourly Bike Counts")
            plt.figure(figsize=(12, 6))
            plt.plot(all_metrics['started_at'], all_metrics['avg_trip_duration'], label='All Data', marker='o')
            plt.plot(df_electric['started_at'], df_electric['avg_trip_duration'], label='Electric', marker='o')
            plt.plot(df_classic['started_at'], df_classic['avg_trip_duration'], label='Classic', marker='o')
            plt.xlabel('Date')
            plt.ylabel('Duration (minutes)')
            plt.title('Comparison of Average Trip Duration between Electric and Classic Rideable Types')
            plt.legend()
            st.pyplot(fig)
            sns.countplot(data=df, x='hour')
            plt.title('Hourly Bike Counts')
            plt.xlabel('Hour of the Day')
            plt.ylabel('Count')
            plt.xticks(range(24))
            plt.tight_layout()
            st.pyplot()

if __name__ == "__main__":
    main()