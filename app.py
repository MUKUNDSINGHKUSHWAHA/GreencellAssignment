import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

st.title("Voltage Data Analysis")

# Upload CSV File
uploaded_file = st.file_uploader("Upload your Sample Data File in .csv Format", type=["csv"])

if uploaded_file:
    # reading uploaded file and converting it into a pandas dataframe
    df = pd.read_csv(uploaded_file)

    # Timestamp to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values(by='Timestamp')

    # Renaming values column in the file to voltage
    df.rename(columns={'Values': 'Voltage'}, inplace=True)

    # data trendline on the Voltage data, 5 day moving average on the plot
    st.subheader("Voltage Trend")
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df['Timestamp'], df['Voltage'], label='Original Voltage', color='blue', alpha=0.6)

    # Moving Average
    df['Moving_Avg'] = df['Voltage'].rolling(window=5, min_periods=1).mean()
    ax.plot(df['Timestamp'], df['Moving_Avg'], label='5-Day Moving Avg', color='red', linewidth=2)

    # Peaks and Lows
    peaks, _ = find_peaks(df['Voltage'])
    lows, _ = find_peaks(-df['Voltage'])

    ax.scatter(df['Timestamp'][peaks], df['Voltage'][peaks], color='green', label='Peaks', marker='o')
    ax.scatter(df['Timestamp'][lows], df['Voltage'][lows], color='orange', label='Lows', marker='*')

    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Voltage")
    plt.title("Voltage Data with 5-Day Moving Average and Peaks/Lows")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    st.pyplot(fig)

    # c.) tabulated peaks and lows
    st.subheader("Local Peaks")
    st.dataframe(df.iloc[peaks][['Timestamp', 'Voltage']])

    st.subheader("Local Lows")
    st.dataframe(df.iloc[lows][['Timestamp', 'Voltage']])

    # d.)Instances where voltage went below 20
    st.subheader("Voltage Below 20 Instances")
    low_voltage_instances = df[df['Voltage'] < 20]
    st.dataframe(low_voltage_instances[['Timestamp', 'Voltage']])

    # 2. Tabulated timestamp of instance when the downward slope accelerates in each downward cycle 
    df['Voltage_Change'] = df['Voltage'].diff()
    df['Voltage_Accel'] = df['Voltage_Change'].diff()
    downward_accel_instances = df[df['Voltage_Accel'] < 0][['Timestamp', 'Voltage', 'Voltage_Accel']]

    st.subheader("Timestamps where downward slope accelerates")
    st.dataframe(downward_accel_instances)
