# app.py
from flask import Flask
from controllers.datapatterns import data_summary

app = Flask(__name__)

app.route('/api/data-summary', methods=['GET'])(data_summary)

if __name__ == '__main__':
    app.run(debug=True)
