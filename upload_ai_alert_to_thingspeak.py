import time
import pandas as pd
from sklearn.ensemble import IsolationForest
import requests

# --- YOUR SETTINGS ---
CHANNEL_ID = '3302311'
READ_API_KEY = 'QG2ZCO73LJA25EV7'
WRITE_API_KEY = '5RQMY12FIYJICV59'

def run_ai_monitor():
    print("AI Monitor Started... Checking for anomalies every 5 minutes.")
    
    while True:
        try:
            # 1. Download latest 100 data points from ThingSpeak
            url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?api_key={READ_API_KEY}&results=100"
            df = pd.read_csv(url)
            
            # 2. Prepare data for AI
            # This ensures 'df' and 'X' always have the same number of rows
            df.dropna(subset=['field1', 'field2', 'field3'], inplace=True)
            
            if not df.empty:
                # 3. Run Isolation Forest AI
                model = IsolationForest(contamination=0.05, random_state=42)
                X = df[['field1', 'field2', 'field3']]
                df['anomaly'] = model.fit_predict(X)
                
                # 4. Identify the latest reading
                latest_row = df.iloc[-1]
                latest_status = latest_row['anomaly']
                
                # 5. Determine Alert: 1 for Anomaly (-1), 0 for Normal (1)
                alert_value = 1 if latest_status == -1 else 0
                
                # 6. Upload Alert to Field 4 on ThingSpeak
                upload_url = f"https://api.thingspeak.com/update?api_key={WRITE_API_KEY}&field4={alert_value}"
                requests.get(upload_url)
                
                # Console Output with Data Details
                timestamp = time.strftime('%H:%M:%S')
                if alert_value == 1:
                    print(f"[{timestamp}] !!! ANOMALY DETECTED !!!")
                    print(f"Values -> Temp: {latest_row['field1']}, Hum: {latest_row['field2']}, Pres: {latest_row['field3']}")
                else:
                    print(f"[{timestamp}] Status: Normal (Temp: {latest_row['field1']})")
                    
            else:
                print("Waiting for more data from ESP32...")

        except Exception as e:
            print(f"Error occurred: {e}")

        print("Sleeping for 5 minutes...")
        time.sleep(300)

if __name__ == "__main__":
    run_ai_monitor()
