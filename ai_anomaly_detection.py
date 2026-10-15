# ===== AI Anomaly Detection for IoT Weather Station =====
# Install (once): pip install pandas numpy matplotlib scikit-learn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
# Load ThingSpeak CSV
df = pd.read_csv("C:/Sahil7551/feeds.csv")
# Rename columns to simple names (ThingSpeak uses field1/field2/field3)
df = df.rename(columns={"field1": "temp", "field2": "hum", "field3": "pres"})
# Keep required columns and remove missing values
df = df[["created_at", "temp", "hum", "pres"]].dropna()
# Features for AI
X = df[["temp", "hum", "pres"]]
# Train unsupervised anomaly model
model = IsolationForest(contamination=0.01, random_state=42)
df["anomaly"] = model.fit_predict(X)  # -1 = anomaly, 1 = normal
anoms = df[df["anomaly"] == -1]
print("Total rows:", len(df))
print("Anomalies found:", len(anoms))
print(anoms.tail(10))
# Plot example: temperature with anomalies marked
plt.figure()
plt.plot(df["temp"].values, label="Temperature")
plt.scatter(anoms.index, anoms["temp"], marker="x", label="Anomaly")
plt.title("Temperature with AI Anomaly Detection")
plt.xlabel("Sample Index")
plt.ylabel("Temperature (C)")
plt.legend()
plt.show()
