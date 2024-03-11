# app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from flask import Flask
from controllers import DataSummary

app = Flask(__name__)

app.route('/api/data-summary', methods=['GET'])(DataSummary.data_summary)

if __name__ == '__main__':
    app.run(debug=True)
