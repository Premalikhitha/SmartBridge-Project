from flask import Flask, render_template, request
import sqlite3
import joblib
import os

app = Flask(__name__)

# Load ML Model
model = joblib.load("crop_model.pkl")

DATABASE = "database.db"

# Create database
def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nitrogen REAL,
        phosphorus REAL,
        potassium REAL,
        temperature REAL,
        humidity REAL,
        ph REAL,
        rainfall REAL,
        crop TEXT
    )
    """)

    conn.commit()
    conn.close()

create_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    N = float(request.form["N"])
    P = float(request.form["P"])
    K = float(request.form["K"])
    temperature = float(request.form["temperature"])
    humidity = float(request.form["humidity"])
    ph = float(request.form["ph"])
    rainfall = float(request.form["rainfall"])

    prediction = model.predict([[N, P, K, temperature,
                                 humidity, ph, rainfall]])

    crop = prediction[0]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions
    (nitrogen, phosphorus, potassium,
    temperature, humidity, ph, rainfall, crop)

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (N, P, K, temperature,
     humidity, ph, rainfall, crop))

    conn.commit()
    conn.close()

    return render_template(
        "index.html",
        prediction_text=f"Recommended Crop: {crop}"
    )


if __name__ == "__main__":
    app.run(debug=True)