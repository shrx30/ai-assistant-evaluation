import json
import os

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


LOG_FILE = (
    "app/observability/observability_logs.jsonl"
)


st.set_page_config(

    page_title="Observability Dashboard",

    page_icon="📊",

    layout="wide"
)


st.title(
    "AI Assistant Observability Dashboard"
)


# ---------------------------------
# Load Logs
# ---------------------------------

if not os.path.exists(
    LOG_FILE
):

    st.error(
        "No observability logs found."
    )

    st.stop()


logs = []

try:

    with open(

        LOG_FILE,

        "r",

        encoding="utf-8"

    ) as file:

        for line in file:

            if line.strip():

                logs.append(
                    json.loads(line)
                )

except Exception as e:

    st.error(
        f"Error loading logs: {str(e)}"
    )

    st.stop()


if len(logs) == 0:

    st.warning(
        "Log file exists but contains no entries."
    )

    st.stop()


df = pd.DataFrame(logs)


# ---------------------------------
# Debug Info
# ---------------------------------

st.subheader(
    "Debug Information"
)

st.write(
    "Available Columns:"
)

st.write(
    list(df.columns)
)

st.write(
    df.head()
)


# ---------------------------------
# Metrics
# ---------------------------------

st.subheader(
    "Runtime Metrics"
)

col1, col2, col3 = st.columns(3)

col1.metric(

    "Total Requests",

    len(df)
)

col2.metric(

    "Average Latency",

    round(

        df["latency"].mean(),

        2

    )

    if "latency" in df.columns

    else 0
)

col3.metric(

    "Average Response Length",

    round(

        df["response"]

        .astype(str)

        .str.len()

        .mean(),

        2

    )

    if "response" in df.columns

    else 0
)


# ---------------------------------
# Unsafe Requests
# ---------------------------------

if "unsafe" in df.columns:

    unsafe_count = len(

        df[

            df["unsafe"]

            == True
        ]
    )

else:

    unsafe_count = 0


st.metric(

    "Unsafe Requests",

    unsafe_count
)


# ---------------------------------
# Latency Chart
# ---------------------------------

if "latency" in df.columns:

    st.subheader(
        "Latency Trend"
    )

    fig, ax = plt.subplots()

    ax.plot(
        df["latency"]
    )

    ax.set_xlabel(
        "Request"
    )

    ax.set_ylabel(
        "Latency"
    )

    st.pyplot(fig)


# ---------------------------------
# Raw Logs
# ---------------------------------

st.subheader(
    "Raw Observability Logs"
)

st.dataframe(
    df,
    use_container_width=True
)
