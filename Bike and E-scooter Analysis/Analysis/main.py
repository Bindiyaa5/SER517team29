# main_script.py
import pandas as pd
from distance import calculate_distance
from weather import add_weather_data

def main():
    # Load your data into a pandas DataFrame
    df = pd.read_csv('updated_bike_sharing_data_with_distance.csv ')  # Make sure the file extension is correct (.csv instead of .xls)

    # # Calculate the distance for each ride and create a new column 'distance_km' in the DataFrame
    # df['distance_km'] = df.apply(
    #     lambda row: calculate_distance(
    #         (row['start_lat'], row['start_lng']),
    #         (row['end_lat'], row['end_lng'])
    #     ), axis=1
    # )

    # df.to_csv('updated_bike_sharing_data_with_distance.csv', index=False)
    # Your OpenWeatherMap API key
    api_key = '11a611eeac4be6b2d65d57c621bbf128'

    df = add_weather_data(df, api_key)

    # Save the updated DataFrame back to a new CSV file
    df.to_csv('updated_bike_sharing_data_with_weather.csv', index=False)

if __name__ == "__main__":
    main()
