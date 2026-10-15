import time
import pandas as pd
import requests
import logging
from sklearn.ensemble import IsolationForest

# --- YOUR SETTINGS ---
CHANNEL_ID = '3302311'
READ_API_KEY = 'QG2ZCO73LJA25EV7'
WRITE_API_KEY = '5RQMY12FIYJICV59'

# Set up logging to log to a file and console
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('ai_monitor.log')
    ]
)

def run_ai_monitor():
    logging.info("AI Monitor Started... Checking for anomalies every 5 minutes.")
    
    # Initialize the Isolation Forest model
    model = IsolationForest(contamination=0.05, random_state=42)

    while True:
        try:
            # 1. Download latest 100 data points from ThingSpeak
            url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?api_key={READ_API_KEY}&results=100"
            df = pd.read_csv(url)
            
            # 2. Prepare data for AI
            df.dropna(subset=['field1', 'field2', 'field3'], inplace=True)
            
            if not df.empty:
                # 3. Run Isolation Forest AI - Fit model only on first run
                X = df[['field1', 'field2', 'field3']]
                
                # Fit the model only on the first run
                if not hasattr(model, 'estimators_'):
                    model.fit(X)
                
                df['anomaly'] = model.predict(X)
                
                # 4. Identify the latest reading
                latest_row = df.iloc[-1]
                latest_status = latest_row['anomaly']
                
                # 5. Determine Alert: 1 for Anomaly (-1), 0 for Normal (1)
                alert_value = 1 if latest_status == -1 else 0
                
                # 6. Upload Alert to Field 4 on ThingSpeak
                upload_url = f"https://api.thingspeak.com/update?api_key={WRITE_API_KEY}&field4={alert_value}"
                
                # Attempt to upload the alert and retry on failure
                retries = 3
                success = False
                for attempt in range(retries):
                    try:
                        response = requests.get(upload_url)
                        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
                        
                        if response.status_code == 200:
                            logging.info(f"Alert successfully uploaded to ThingSpeak. Attempt {attempt + 1}/{retries}.")
                            success = True
                            break
                        else:
                            logging.warning(f"Unexpected status code: {response.status_code}. Response: {response.text}")
                    except requests.exceptions.RequestException as e:
                        logging.error(f"Error on attempt {attempt + 1}/{retries}: {e}")
                        if attempt < retries - 1:
                            logging.info("Retrying...")
                        else:
                            logging.error("Max retries reached. Giving up.")
                
                if not success:
                    logging.warning(f"Failed to upload alert after {retries} attempts.")
                
                # Console Output with Data Details
                timestamp = time.strftime('%H:%M:%S')
                if alert_value == 1:
                    logging.warning(f"[{timestamp}] !!! ANOMALY DETECTED !!!")
                    logging.warning(f"Values -> Temp: {latest_row['field1']}, Hum: {latest_row['field2']}, Pres: {latest_row['field3']}")
                else:
                    logging.info(f"[{timestamp}] Status: Normal (Temp: {latest_row['field1']})")
                    
            else:
                logging.info("Waiting for more data from ESP32...")

        except Exception as e:
            logging.error(f"Error occurred: {e}")

        logging.info("Sleeping for 5 minutes...")
        time.sleep(300)

if __name__ == "__main__":
    run_ai_monitor()
    
