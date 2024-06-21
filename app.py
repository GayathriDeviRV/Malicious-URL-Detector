from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, disconnect
import joblib
import pandas as pd
from extract_features import extract_features
import signal
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Load the model and scaler
model = joblib.load('url_classifier_model.pkl')
scaler = joblib.load('scaler.pkl')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    features_df = extract_features(url)
    features_scaled = scaler.transform(features_df)
    prediction = model.predict(features_scaled)
    result = 'Malicious' if prediction[0] == 1 else 'Benign'
    return jsonify(result=result)


def signal_handler(sig, frame):
    print('Shutting down the server...')
    os._exit(0)


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    signal_handler(None, None)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    socketio.run(app, debug=True)
