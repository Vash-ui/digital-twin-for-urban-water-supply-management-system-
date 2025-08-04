# utils/preprocess.py
import pandas as pd

def preprocess_sensor_data(path='data/sensor_data.csv'):
    df = pd.read_csv(path, parse_dates=['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['flow_rate_norm'] = (df['flow_rate'] - df['flow_rate'].mean()) / df['flow_rate'].std()
    df['pressure_norm'] = (df['pressure'] - df['pressure'].mean()) / df['pressure'].std()
    return df[['flow_rate_norm', 'pressure_norm', 'hour']], df['leak']
