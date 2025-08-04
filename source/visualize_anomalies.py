import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def visualize_anomalies(csv_path="data/parsed_packets.csv", anomaly_csv="data/predicted_with_anomalies.csv"):
    print("Loading data...")
    df_full = pd.read_csv(csv_path)
    df_pred = pd.read_csv(anomaly_csv)

    df = df_full.copy()
    df = df.iloc[:len(df_pred)] 
    df["anomaly"] = df_pred["anomaly"]

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Plot 1: Anomalies over time
    plt.figure(figsize=(12, 6))
    df.set_index("timestamp")["anomaly"].resample("1S").sum().plot()
    plt.title("Number of Anomalies Over Time")
    plt.ylabel("Anomalies")
    plt.xlabel("Timestamp")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("data/Anomaly_TimeSeries.png")
    print(" Time series plot saved as data/Anomaly_TimeSeries.png")

    # Plot 2: Top anomalous source IPs
    top_ips = df[df["anomaly"] == 1]["src_ip"].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_ips.values, y=top_ips.index, palette="Reds_r")
    plt.title("Top 10 Anomalous Source IPs")
    plt.xlabel("Anomaly Count")
    plt.ylabel("Source IP")
    plt.tight_layout()
    plt.savefig("data/Top_Anomalous_IPs.png")
    print("Bar plot saved as data/Top_Anomalous_IPs.png")

    # Plot 3: Heatmap of anomalies by protocol
    plt.figure(figsize=(10, 6))
    heat_data = pd.crosstab(df["protocol"], df["anomaly"])
    sns.heatmap(heat_data, annot=True, fmt="d", cmap="Reds")
    plt.title("Anomalies by Protocol")
    plt.xlabel("Anomaly (0=Normal, 1=Anomaly)")
    plt.ylabel("Protocol")
    plt.tight_layout()
    plt.savefig("data/Anomaly_Heatmap.png")
    print("Heatmap saved as data/Anomaly_Heatmap.png")

if __name__ == "__main__":
    visualize_anomalies()
