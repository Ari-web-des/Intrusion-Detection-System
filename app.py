import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import plotly.graph_objects as go
import seaborn as sns
import plotly.express as px
import sys
sys.path.append('source')
from preprocess_packets import preprocess_dataframe


st.set_page_config(page_title="IDS Dashboard", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    h1, h2, h3 {
        color: #1f77b4;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .css-1rs6os.edgvbvh3 {
        color: #444 !important;
    }
    </style>
""", unsafe_allow_html=True)


# Title
st.title("🔐 Intrusion Detection System - Anomaly Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/predicted_with_anomalies.csv")

uploaded_file = st.sidebar.file_uploader("Upload your packet CSV", type=["csv"])
if uploaded_file:
    user_df = pd.read_csv(uploaded_file)
    try:
        preprocessed = preprocess_dataframe(user_df)
        model = joblib.load("model/ids_model.pkl")
        preprocessed["anomaly"] = model.predict(preprocessed[["protocol_encoded", "length_normalized"]])
        df = preprocessed 
        st.sidebar.success("File processed and analyzed!")
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

df = load_data()

# Sidebar
st.sidebar.title("Navigation")
view_option = st.sidebar.radio("Choose a view", ["📊 Summary", "📈 Time Series", "🌍 IP Heatmap"])

# 📊 Summary View
if view_option == "📊 Summary":
    st.subheader("Anomaly Detection Summary")
    st.markdown("""
    ### 📊 Anomaly Detection Summary <span title="This shows the number of normal vs suspicious packets detected using machine learning."></span>
    """, unsafe_allow_html=True)

    with st.expander("ℹ️ What is an Anomaly?"):
        st.markdown("""
        An **anomaly** is a data point that deviates significantly from the norm in your network traffic.
        
        In the context of this Intrusion Detection System:
        - Anomalies could be caused by **suspicious behavior**, such as port scans, DDoS attempts, or abnormal packet size/frequency.
        - Detected using **unsupervised machine learning (Isolation Forest)**.
        - Helps you identify potential **intrusions or threats**.
        """)
    # Compute counts
    normal = len(df[df["anomaly"] == 1])
    anomalies = len(df[df["anomaly"] == -1])
    total = len(df)
    anomaly_rate = round((anomalies / total) * 100, 2)

    # Display counts
    st.markdown(f"""
    <div style="font-size:18px;">
    ⚠️ <b>{anomalies}</b> anomalies found out of <b>{total}</b> packets.
    <br><br>
    ✅ <b>Normal Packets:</b> {normal}<br>
    ⚠️ <b>Anomalies Detected:</b> {anomalies}<br>
    📦 <b>Total Packets:</b> {total}<br>
    📉 <b>Anomaly Rate:</b> {anomaly_rate}%
    </div>
    """, unsafe_allow_html=True)

    # Interactive bar chart
    fig = px.bar(
        x=["Normal", "Anomaly"],
        y=[normal, anomalies],
        color=["Normal", "Anomaly"],
        color_discrete_map={"Normal": "green", "Anomaly": "red"},
        title="Anomaly vs Normal Packet Count",
        labels={"x": "Packet Type", "y": "Count"}
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# 📈 Time Series View
elif view_option == "📈 Time Series":
    st.subheader("📈 Anomalies Over Time")

    # Convert timestamp column
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Filter anomalies
    anomalies = df[df["anomaly"] == -1].copy()
    anomalies["minute"] = anomalies["timestamp"].dt.floor("T")  # Group by minute
    anomaly_counts = anomalies.groupby("minute").size().reset_index(name="count")

    if anomaly_counts.empty:
        st.warning("No anomaly data available for time series plot.")
    else:
        fig = px.line(
            anomaly_counts,
            x="minute",
            y="count",
            title="📉 Anomalies Detected Per Minute",
            labels={"minute": "Time", "count": "Anomaly Count"},
            markers=True,
        )
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Count",
            template="plotly_dark",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

# 🌍 Heatmap View
elif view_option == "🌍 IP Heatmap":
    st.subheader("Top Anomalous IPs")
    top_ips = df[df["anomaly"] == -1]["src_ip"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_ips.values, y=top_ips.index, palette="Reds_r", ax=ax)
    ax.set_title("Top 10 Anomalous Source IPs")
    st.pyplot(fig, use_container_width=True)

    st.markdown("🔍 These are the most frequent source IPs flagged as anomalies.")

# Footer
st.markdown("---")
st.markdown("© 2025 Aritra Das | IDS Project | Powered by Streamlit 🚀")
