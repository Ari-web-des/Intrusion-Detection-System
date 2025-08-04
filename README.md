# 🛡️ Intrusion Detection System (IDS) using Machine Learning

A machine learning-based Intrusion Detection System (IDS) that detects anomalies in network traffic. This interactive Streamlit application allows users to upload their own packet captures (CSV format) and get instant anomaly detection results.
---
## 🚀 Features
- ✅ Upload your own network packet CSV for anomaly detection.
- 📊 Visualize anomaly distribution with time series and bar charts.
- 📁 Real-time preprocessing of uploaded files.
- 🔍 Detects anomalies using trained ML model (`isolation forest`).
- 📥 Export predictions with anomaly flags.
- 🧠 Model trained on labeled packet data.
- 🧪 Future support for real-time packet sniffing with `pyshark`.
---
## 📂 Folder Structure
ids-ml/
│
├── app.py # Streamlit application
├── model/
│ └── ids_model.pkl # Trained ML model
├── data/
│ ├── parsed_packets.csv # Sample parsed packet data
│ ├── preprocessed_packets.csv # Preprocessed data used for prediction
│ ├── predicted_with_anomalies.csv # Output with anomaly column
│ └── Anomaly_plot.png # Anomaly visualization plot
├── source/
│ ├── preprocess_packets.py # Functions for preprocessing
│ └── pcap_parser.py # PCAP to CSV parser (for advanced users)
├── .vscode/
│ └── settings.json # VS Code config
└── README.md
## 🧪 How It Works
1. **Data Upload**  
   Upload your own network packet CSV file using the Streamlit sidebar.
2. **Preprocessing**  
   Your file is automatically cleaned, encoded, and scaled using `LabelEncoder` and `MinMaxScaler`.
3. **Prediction**  
   The ML model predicts anomalies based on encoded protocol and packet length.
4. **Visualization**  
   Anomaly statistics and time-series plots are generated and shown.
---
## 📌 Requirements
Install dependencies:
streamlit
scikit-learn
pandas
matplotlib
joblib
also u should a csv file for your own network
