import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
import calendar
import warnings

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def summary_statistics(data):
    return data.describe()

def plot_histogram(data, column):
    plt.figure(figsize=(8, 6))
    sns.histplot(data[column], kde=True)
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    return plt

def correlation_matrix(data):
    return data.corr(numeric_only=True)

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance


def dist(df):
    df['distance_km'] = df.apply(lambda x: haversine_distance(x['Start Centroid Latitude'], x['Start Centroid Longitude'], x['End Centroid Latitude'], x['End Centroid Longitude']), axis=1)
    return df


def monthlyUsage(df):
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month.map(lambda x: calendar.month_name[x])
    monthly_trip_counts = df.groupby('Month').size()

    plt.figure(figsize=(10, 6))
    monthly_trip_counts.plot(kind='bar', color='skyblue')
    plt.title('Month-wise Usage Trends')
    plt.xlabel('Month')
    plt.ylabel('Number of Trips')
    plt.xticks(rotation=45)
    plt.show()

def popularStartAreas(df):
    df['distance_km'] = df.apply(lambda x: haversine_distance(x['Start Centroid Latitude'], x['Start Centroid Longitude'], x['End Centroid Latitude'], x['End Centroid Longitude']), axis=1)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month.map(lambda x: calendar.month_name[x])
    popular_start_areas = df['Start Community Area Name'].value_counts().head(10)

    plt.figure(figsize=(10, 6))
    popular_start_areas.plot(kind='bar', color='skyblue')
    plt.title('Popular Start Points (Community Area)')
    plt.xlabel('Community Area')
    plt.ylabel('Number of Trips')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def popularEndAreas(df):
    df['distance_km'] = df.apply(lambda x: haversine_distance(x['Start Centroid Latitude'], x['Start Centroid Longitude'], x['End Centroid Latitude'], x['End Centroid Longitude']), axis=1)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month.map(lambda x: calendar.month_name[x])
    popular_end_areas = df['End Community Area Name'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    popular_end_areas.plot(kind='bar', color='salmon')
    plt.title('Popular End Points (Community Area)')
    plt.xlabel('Community Area')
    plt.ylabel('Number of Trips')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def peakUsageHours(df):
    df['distance_km'] = df.apply(lambda x: haversine_distance(x['Start Centroid Latitude'], x['Start Centroid Longitude'], x['End Centroid Latitude'], x['End Centroid Longitude']), axis=1)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month.map(lambda x: calendar.month_name[x])
    df['Hour'] = df['Start Time'].dt.hour

    hourly_trip_counts = df.groupby('Hour').size()

    plt.figure(figsize=(10, 6))
    hourly_trip_counts.plot(kind='line', color='skyblue')
    plt.title('Peak Usage Times')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Trips')
    plt.xticks(range(24))
    plt.grid(True)
    plt.show()

