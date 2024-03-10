# datasummary.py
from flask import jsonify
import data_analysis as da

def data_summary():
    metrics = da.calculate_metrics("C:/Users/vbodavul/Downloads/archive (2)/202[23]*-divvy-tripdata.csv")
    return jsonify(metrics)
