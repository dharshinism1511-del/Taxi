
from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Load Taxi Dataset
df = pd.read_csv("taxi_data.csv")

df["pickup_datetime"] = pd.to_datetime(
    df["pickup_datetime"]
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/analytics")
def analytics():

    df["hour"] = df["pickup_datetime"].dt.hour

    hourly = df.groupby("hour").size().reindex(
        range(24), fill_value=0
    )

    pickup = df["pickup_location"].value_counts().head(5)
    dropoff = df["dropoff_location"].value_counts().head(5)

    return jsonify({
        "total_trips": int(len(df)),
        "avg_fare": round(float(df["fare_amount"].mean()), 2),
        "total_revenue": round(float(df["fare_amount"].sum()), 2),
        "peak_hour": int(hourly.idxmax()),

        "hour_labels": [f"{h:02d}:00" for h in range(24)],
        "hour_values": hourly.tolist(),

        "pickup_labels": pickup.index.tolist(),
        "pickup_values": pickup.tolist(),

        "dropoff_labels": dropoff.index.tolist(),
        "dropoff_values": dropoff.tolist()
    })

if __name__ == "__main__":
    app.run(debug=True)
  
