import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def simulate_data(duration_minutes=1440):
    # Create 'data' directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    timestamps = [datetime.now() - timedelta(minutes=i) for i in range(duration_minutes)]
    data = {
        'timestamp': timestamps[::-1],
        'flow_rate': np.random.normal(80, 10, duration_minutes),
        'pressure': np.random.normal(60, 5, duration_minutes),
        'leak': np.random.choice([0, 1], duration_minutes, p=[0.95, 0.05])
    }
    df = pd.DataFrame(data)
    df.to_csv('data/sensor_data.csv', index=False)
    print("✅ Sensor data generated.")

if __name__ == "__main__":
    simulate_data()
 