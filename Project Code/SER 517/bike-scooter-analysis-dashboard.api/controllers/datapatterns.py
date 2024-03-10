from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load your data
df = pd.read_csv(r'C:\Users\vbodavul\Downloads\archive (2)\merged_and_cleaned_tripdata.csv')

@app.route('/api/data/summary', methods=['GET'])
def get_data_summary():
    # Example: Return summary statistics
    summary = {
        "average_distance_km": df['distance_km'].mean(),
        "most_common_start_location": df['start_station_name'].mode()[0]
    }
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)
