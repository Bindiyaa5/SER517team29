import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import calendar
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


def load_and_prepare_data(file_pattern):
    file_list = glob.glob(file_pattern)
    df = pd.concat((pd.read_csv(file) for file in file_list))
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    df.drop_duplicates(inplace=True)
    return df

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def calculate_distances(df):
    df['distance_km'] = df.apply(lambda x: haversine_distance(x['start_lat'], x['start_lng'], x['end_lat'], x['end_lng']), axis=1)
    return df

# New function to encapsulate data analysis and return summary metrics
def calculate_metrics(file_pattern="path/to/your/csv/files/*-divvy-tripdata.csv"):
    df = load_and_prepare_data(file_pattern)
    df = calculate_distances(df)
    
    average_distance_km = df['distance_km'].mean()
    most_common_start_location = df['start_station_name'].mode()[0]
    df['month'] = df['started_at'].dt.month
    most_preferred_month = df['month'].value_counts().idxmax()
    most_preferred_month_name = calendar.month_name[most_preferred_month]
    monthly_distance_sum = df.groupby('month')['distance_km'].sum()
    most_distance_month = monthly_distance_sum.idxmax()
    most_distance_month_name = calendar.month_name[most_distance_month]
    df['duration_minutes'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60
    average_duration = df['duration_minutes'].mean()
    
    # Returning a dictionary of calculated metrics
    return {
        "average_distance_km": average_distance_km,
        "most_common_start_location": most_common_start_location,
        "most_preferred_month_name": most_preferred_month_name,
        "most_distance_month_name": most_distance_month_name,
        "total_distance": monthly_distance_sum.max(),
        "average_duration": average_duration
    }

# If you wish to run and visualize directly from this script
def main():
    metrics = calculate_metrics(file_pattern="C:/Users/vbodavul/Downloads/archive (2)/202[2-4]*-divvy-tripdata.csv")
    print(metrics)

if __name__ == "__main__":
    main()
