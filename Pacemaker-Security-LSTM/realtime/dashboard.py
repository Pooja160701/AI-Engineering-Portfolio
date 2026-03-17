import streamlit as st
import pandas as pd
import random
import time

# Page configuration
st.set_page_config(
    page_title="AI Pacemaker Monitor",
    layout="wide"
)

st.title("❤️ AI Pacemaker Monitoring System")
st.subheader("Real-Time Cardiac Anomaly Detection")

# Placeholders
metric_placeholder = st.empty()
chart_placeholder = st.empty()
table_placeholder = st.empty()
alert_placeholder = st.empty()

data = []
attack_count = 0

while True:

    # Simulated heart rate signal
    heart_rate = random.randint(60, 110)

    # Detect anomaly
    anomaly = 1 if heart_rate > 95 else 0

    if anomaly:
        attack_count += 1

    new_row = {
        "HeartRate": heart_rate,
        "Status": "⚠ Anomaly" if anomaly else "Normal"
    }

    data.append(new_row)

    df = pd.DataFrame(data[-30:])

    # ---------------------
    # METRICS SECTION
    # ---------------------

    with metric_placeholder.container():

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Current Heart Rate",
            f"{heart_rate} bpm"
        )

        col2.metric(
            "System Status",
            "⚠ Alert" if anomaly else "Normal"
        )

        col3.metric(
            "Total Signals",
            len(data)
        )

        col4.metric(
            "Total Anomalies",
            attack_count
        )

    # ---------------------
    # HEART RATE GRAPH
    # ---------------------

    chart_placeholder.line_chart(df["HeartRate"])

    # ---------------------
    # LIVE DATA TABLE
    # ---------------------

    table_placeholder.dataframe(df)

    # ---------------------
    # ALERT MESSAGE
    # ---------------------

    if anomaly:
        alert_placeholder.error("⚠ Pacemaker anomaly detected!")
    else:
        alert_placeholder.success("Normal heartbeat")

    time.sleep(2)