import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import calendar

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

def analyze_data(df):
    average_distance_km = df['distance_km'].mean()
    most_common_start_location = df['start_station_name'].mode()[0]
    df['month'] = df['started_at'].dt.month
    most_preferred_month = df['month'].value_counts().idxmax()
    most_preferred_month_name = calendar.month_name[most_preferred_month]
    monthly_distance_sum = df.groupby('month')['distance_km'].sum()
    most_distance_month = monthly_distance_sum.idxmax()
    most_distance_month_name = calendar.month_name[most_distance_month]
    print(f"Average distance traveled: {average_distance_km} km")
    print(f"Most common start location: {most_common_start_location}")
    print(f"The most preferred month for bicycle riding is: {most_preferred_month_name}")
    print(f"The month with the most distance traveled is: {most_distance_month_name} with a total distance of {monthly_distance_sum.max()} kilometers.")
    df['duration_minutes'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60
    average_duration = df['duration_minutes'].mean()
    print(f'Average Trip Duration: {average_duration} minutes')

def visualize_data(df):
    df['month'] = df['started_at'].dt.to_period('M')
    usage_trends = df.groupby('month').size()
    usage_trends.plot(kind='bar')
    plt.title('Usage Trends Over Time')
    plt.xlabel('Month')
    plt.ylabel('Number of Trips')
    plt.xticks(rotation=45)
    plt.show()

    top_starts = df['start_station_name'].value_counts().head(10)
    top_ends = df['end_station_name'].value_counts().head(10)
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    top_starts.plot(kind='barh', ax=axes[0], title='Top Start Locations')
    top_ends.plot(kind='barh', ax=axes[1], title='Top End Locations')
    plt.tight_layout()
    plt.show()

    df['hour'] = df['started_at'].dt.hour
    peak_usage = df.groupby('hour').size()
    peak_usage.plot(kind='bar')
    plt.title('Peak Usage Times')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Trips')
    plt.show()

def main():
    file_pattern = "C:/Users/vbodavul/Downloads/archive (2)/202[23]*-divvy-tripdata.csv"
    df = load_and_prepare_data(file_pattern)
    df = calculate_distances(df)
    analyze_data(df)
    visualize_data(df)
    df.to_csv('C:/Users/vbodavul/Downloads/archive (2)/merged_and_cleaned_tripdata.csv', index=False)

if __name__ == "__main__":
    main()
