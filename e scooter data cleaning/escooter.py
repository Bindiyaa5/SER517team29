# # %%
# pip install pandas

# # %%
# pip install numpy

# # %%
# pip install --upgrade pip


# # %%
# pip install matplotlib

# # %%
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# # %%
# df = pd.read_csv("E-Scooter_Trips_20240215.csv")

# # %%
# print(df.head())

# # %%
# print(df.isnull().sum())

# # %%
# df.dropna(inplace=True)

# # %%
# df['Start Time'] = pd.to_datetime(df['Start Time'])

# # %%
# print(df['Start Time'].head())

# # %%
# df['End Time'] = pd.to_datetime(df['End Time'])

# # %%
# print(df['End Time'].head())

# # %%
# df

# # %%
# df['Trip Distance (miles)'] = df['Trip Distance'] / 1609   # Converting 'Trip Distance' from meters to miles

# # %%
# df.drop('Trip Distance', axis=1, inplace=True)

# # %%
# df.head()

# # %%
# df['Trip Duration (minutes)'] = df['Trip Duration'] / 60  #Converting 'Trip Duration' from seconds to minutes

# # %%
# df.drop('Trip Duration', axis=1, inplace=True)

# # %%
# df.head()

# # %%
# print(df.describe())

# # %%

# df.drop_duplicates(inplace=True)

# # %%
# print(df.duplicated().sum())


# # %%
# df.reset_index(drop=True, inplace=True)


# # %%
# pip install scipy

# # %%
# from scipy import stats

# # %%
# z_scores_duration = stats.zscore(df['Trip Duration (minutes)'])
# z_scores_distance = stats.zscore(df['Trip Distance (miles)'])

# # %%
# z_score_threshold = 3 #considering observations beyond 3 standard deviations as outliers

# # %%
# df = df[(abs(z_scores_duration) <= z_score_threshold) & (abs(z_scores_distance) <= z_score_threshold)]

# # %%
# df

# # %%
# df = df[df['End Time'] > df['Start Time']]  #validating data integrity

# # %%
# df.to_csv("cleaned_e_scooter_trip_data.csv", index=False)

# # %% [markdown]
# # Total Average Distance Travelled

# # %%
# def haversine_distance(lat1, lon1, lat2, lon2):
#     R = 6371.0  # Earth radius in kilometers
#     lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#     a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
#     c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
#     distance = R * c
#     return distance

# # %%
# df['distance_km'] = df.apply(lambda x: haversine_distance(x['Start Centroid Latitude'], x['Start Centroid Longitude'], x['End Centroid Latitude'], x['End Centroid Longitude']), axis=1)


# # %%
# # Calculate the average distance
# average_distance_km = df['distance_km'].mean()

# # %%
# # Find the most common start location
# most_common_start_location = df['Start Community Area Name'].mode()[0]

# # %%
# # You can print these out or use them as needed
# print(f"Average distance traveled: {average_distance_km} km")
# print(f"Most common start location: {most_common_start_location}")

# # %% [markdown]
# # Month with maximum distance travelled

# # %%
# import calendar
# import warnings

# # %%
# df['Start Time'] = pd.to_datetime(df['Start Time'])


# with warnings.catch_warnings():
#     warnings.simplefilter("ignore")  
#     df['Month'] = df['Start Time'].dt.month.map(lambda x: calendar.month_name[x])

# # Group by month and sum trip distances
# monthly_distance = df.groupby('Month')['Trip Distance (miles)'].sum()

# max_distance_month = monthly_distance.idxmax()

# print("Month with maximum distance traveled:", max_distance_month)

# # %% [markdown]
# # Maximum distance travelled in a month

# # %%
# max_distance_per_month = df.groupby('Month')['Trip Distance (miles)'].max()

# max_distance_month = max_distance_per_month.idxmax()

# print("Maximum distance traveled in a month:", max_distance_per_month[max_distance_month], "miles in month", max_distance_month)

# # %% [markdown]
# # Monthwise usage trends

# # %%
# monthly_trip_counts = df.groupby('Month').size()

# plt.figure(figsize=(10, 6))
# monthly_trip_counts.plot(kind='bar', color='skyblue')
# plt.title('Month-wise Usage Trends')
# plt.xlabel('Month')
# plt.ylabel('Number of Trips')
# plt.xticks(rotation=45)
# plt.show()

# # %% [markdown]
# # Average trip duration and distance

# # %%
# average_trip_duration = df['Trip Duration (minutes)'].mean()

# average_trip_distance = df['Trip Distance (miles)'].mean()

# print("Average Trip Duration:", average_trip_duration, "minutes")
# print("Average Trip Distance:", average_trip_distance, "miles")

# # %% [markdown]
# # Popular Areas for start and end points

# # %%
# popular_start_areas = df['Start Community Area Name'].value_counts().head(10)

# popular_end_areas = df['End Community Area Name'].value_counts().head(10)

# plt.figure(figsize=(10, 6))
# popular_start_areas.plot(kind='bar', color='skyblue')
# plt.title('Popular Start Points (Community Area)')
# plt.xlabel('Community Area')
# plt.ylabel('Number of Trips')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# # Plot popular end points
# plt.figure(figsize=(10, 6))
# popular_end_areas.plot(kind='bar', color='salmon')
# plt.title('Popular End Points (Community Area)')
# plt.xlabel('Community Area')
# plt.ylabel('Number of Trips')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# # %%
# popular_start_areas = df['Start Community Area Name'].value_counts().head(10)

# def popular_start_points(popular_start_areas):
#     plt.figure(figsize=(10, 6))
#     popular_start_areas.plot(kind='bar', color='skyblue')
#     plt.title('Popular Start Points (Community Area)')
#     plt.xlabel('Community Area')
#     plt.ylabel('Number of Trips')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()

# popular_start_points(popular_start_areas)

# # %% [markdown]
# # Peak usage times

# # %%
# df['Hour'] = df['Start Time'].dt.hour

# hourly_trip_counts = df.groupby('Hour').size()

# plt.figure(figsize=(10, 6))
# hourly_trip_counts.plot(kind='line', color='skyblue')
# plt.title('Peak Usage Times')
# plt.xlabel('Hour of the Day')
# plt.ylabel('Number of Trips')
# plt.xticks(range(24))
# plt.grid(True)
# plt.show()

# # %%
# pip install ipynb-py-convert

# # %%
# pip install nbconvert --user

# # %%
# jupyter nbconvert --to python escooter.ipynb


