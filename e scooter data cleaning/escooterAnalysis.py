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

# def startTime(df):
#     df['Start Time'] = pd.to_datetime(df['Start Time'])

# def month(df):
#     df['Month'] = df['Start Time'].dt.month.map(lambda x: calendar.month_name[x])


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

