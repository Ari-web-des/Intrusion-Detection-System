import joblib
import os
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from sklearn.ensemble import IsolationForest

def train_isolation_forest(input_csv,model_path,output_csv="data/predicted_packets.csv", contamination = 0.01):
    print("loading preprocessed data......")
    df = pd.read_csv(input_csv)
    
    if df.shape[0]==0:
        print("no data found")
        return
    print(f"training on {df.shape[0]} samples with {df.shape[1]} features...")
    
    model = IsolationForest(n_estimators = 100,contamination = contamination,random_state=42,verbose = 0)
    
    start_time = datetime.now()
    X = df[["protocol_encoded", "length_normalized"]]
    model.fit(X)
    end_time = datetime.now()
    print(f"Training Time:{(end_time - start_time).total_seconds():.2f} seconds")
    
    #predict
    df['anomaly'] = model.predict(X)
    
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved at: {model_path}")
    
    print("model trained and saved")
    print(df.head())
    
    anomaly_counts = df['anomaly'].value_counts()
    total = len(df)
    print("\n Anomaly Detection Summary:")
    print(f"Normal:  {anomaly_counts.get(1, 0)} packets")
    print(f"Anomalies: {anomaly_counts.get(-1, 0)} packets")
    print(f"Anomaly Rate: {(anomaly_counts.get(-1, 0) / total) * 100:.2f}%")
    
    try:
        plt.figure(figsize=(8,4))
        df['anomaly'].value_counts().plot(kind='bar', color=['green', 'red'])
        plt.xticks([0,1],['Normal(1)','Anomaly(-1)'], rotation = 0)
        plt.title("Isolation Forest:Anomaly vs Normal")
        plt.ylabel("Packet count")
        plt.tight_layout()
        plt.savefig("data/Anomaly_plot.png")
        print("plot saved as data/Anomaly_plot.png")
    except Exception as e:
        print("could not generate plot",e)
    output_path = "data/predicted_with_anomalies.csv"
    df.to_csv(output_path, index=False)
    print(f"Predictions saved at {output_path}")   
    
if __name__=='__main__':
    train_isolation_forest(
        input_csv="data/preprocessed_packets.csv",
        model_path="model/ids_model.pkl"
    )