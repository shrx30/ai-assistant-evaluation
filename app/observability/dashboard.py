import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


import os

st.write(
    "File Exists:",
    os.path.exists(
        "app/observability/observability_logs.jsonl"
    )
)


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

except FileNotFoundError:

    st.error(
        "No observability logs found."
    )

    st.stop()


if len(logs) == 0:

    st.warning(
        "No log entries yet."
    )

    st.stop()


df = pd.DataFrame(logs)


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
        df["latency"].astype(float).mean(),
        2
    )
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
)


st.subheader(
    "Latency Trend"
)

fig, ax = plt.subplots()

ax.plot(
    df["latency"]
    .astype(float)
)

ax.set_xlabel(
    "Request"
)

ax.set_ylabel(
    "Latency"
)

st.pyplot(fig)


st.subheader(
    "Raw Logs"
)

st.dataframe(
    df,
    use_container_width=True
)
