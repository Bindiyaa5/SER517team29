# datasummary.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from flask import jsonify
from controllers import Data_Analysis as da


def data_summary():
    metrics = da.calculate_metrics("C:/Users/vbodavul/Downloads/archive (2)/202[23]*-divvy-tripdata.csv")
    return jsonify(metrics)
