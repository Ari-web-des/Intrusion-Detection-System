import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

def preprocess_packets(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    df = df[(df['src_ip'] != 'N/A') & (df['dst_ip'] != 'N/A')]

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])  # Drop rows where timestamp couldn't be parsed

    # Debugging Info
    print(df.describe())
    print(df.info())
    print(df.isnull().sum())

    # Encode protocol
    le = LabelEncoder()
    df['protocol_encoded'] = le.fit_transform(df['protocol'])

    # Normalize length
    scaler = MinMaxScaler()
    df['length_normalized'] = scaler.fit_transform(df[['length']])

    # Final output
    df_final = df[['timestamp', 'src_ip', 'dst_ip', 'protocol_encoded', 'length_normalized']]
    df_final.to_csv(output_csv, index=False)

    print(f"\nPreprocessed data saved to: {output_csv}")
    print(df_final.head())
def preprocess_dataframe(df):
    df = df[(df['src_ip'] != 'N/A') & (df['dst_ip'] != 'N/A')]
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    le = LabelEncoder()
    df['protocol_encoded'] = le.fit_transform(df['protocol'])
    scaler = MinMaxScaler()
    df['length_normalized'] = scaler.fit_transform(df[['length']])
    return df[["timestamp", "src_ip", "dst_ip", "protocol_encoded", "length_normalized"]]

if __name__ == '__main__':
    preprocess_packets("data/parsed_packets.csv", "data/preprocessed_packets.csv")
    print("🎉 Done!")
