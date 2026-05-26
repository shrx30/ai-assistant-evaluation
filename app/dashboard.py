import json

import pandas as pd

import streamlit as st

import matplotlib.pyplot as plt


LOG_FILE = "app/observability_logs.jsonl"


st.set_page_config(

    page_title="Observability Dashboard",

    page_icon="📊",

    layout="wide"
)


st.title("AI Assistant Observability Dashboard")


# ---------------------------------
# Load Logs
# ---------------------------------

logs = []

try:

    with open(

        LOG_FILE,

        "r",

        encoding="utf-8"

    ) as file:

        for line in file:

            logs.append(
                json.loads(line)
            )

except FileNotFoundError:

    st.error(
        "No observability logs found."
    )

    st.stop()


df = pd.DataFrame(logs)


# ---------------------------------
# Metrics
# ---------------------------------

st.subheader("Runtime Metrics")


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
)

col3.metric(
    "Average Output Tokens",

    round(
        df["output_tokens"].mean(),
        2
    )
)


# ---------------------------------
# Unsafe Requests
# ---------------------------------

unsafe_count = len(

    df[df["safe_request"] == False]
)

st.metric(
    "Unsafe Requests Blocked",
    unsafe_count
)


# ---------------------------------
# Latency Chart
# ---------------------------------

st.subheader("Latency Trend")


fig, ax = plt.subplots()

ax.plot(df["latency"])

ax.set_xlabel("Request")

ax.set_ylabel("Latency")


st.pyplot(fig)


# ---------------------------------
# Token Usage Chart
# ---------------------------------

st.subheader("Output Token Trend")


fig2, ax2 = plt.subplots()

ax2.plot(df["output_tokens"])

ax2.set_xlabel("Request")

ax2.set_ylabel("Output Tokens")


st.pyplot(fig2)


# ---------------------------------
# Raw Logs
# ---------------------------------

st.subheader("Raw Observability Logs")

st.dataframe(df)