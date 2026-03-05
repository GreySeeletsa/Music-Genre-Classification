from flask import Flask, render_template, request, jsonify
import joblib
import librosa
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
# Load your trained model (saved earlier as .pkl)
model = joblib.load("music_genre_model.pkl")
genres = ['blues','classical','country','disco','hiphop','jazz','metal','pop','reggae','rock']

def extract_features(file_path):
    y, sr = librosa.load(file_path, duration=30)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    return np.mean(mfcc.T, axis=0)

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = "temp.wav"
    file.save(file_path)

    features = extract_features(file_path).reshape(1, -1)
    prediction = model.predict(features)[0]

    return jsonify({"genre": prediction})

if __name__ == "__main__":
    app.run(debug=True)
