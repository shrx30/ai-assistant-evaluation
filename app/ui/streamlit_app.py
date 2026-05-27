import streamlit as st
import json

import pandas as pd
import matplotlib.pyplot as plt


import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from services.chat_services import (
    process_chat
)

from memory.memory_manager import (
    clear_memory
)


# =================================
# PAGE CONFIG
# =================================

st.set_page_config(

    page_title="AI Assistant",

    page_icon="🤖",

    layout="wide"
)


# =================================
# SIDEBAR NAVIGATION
# =================================

page = st.sidebar.radio(

    "Navigation",

    [
        "Chatbot",
        "Observability Dashboard"
    ]
)


# =================================
# MEMORY CONTROLS
# =================================

if st.sidebar.button(
    "Clear Memory"
):

    clear_memory()

    st.session_state.messages = []

    st.sidebar.success(
        "Memory Cleared"
    )


# =================================
# SESSION STATE
# =================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =================================
# CHATBOT PAGE
# =================================

if page == "Chatbot":

    st.title("AI Personal Assistant")

    st.write("NVIDIA Hosted Assistant")


    # -----------------------------
    # DISPLAY HISTORY
    # -----------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])


    # -----------------------------
    # USER INPUT
    # -----------------------------

    user_input = st.chat_input(
        "Type your message..."
    )


    # -----------------------------
    # MAIN CHAT FLOW
    # -----------------------------

    if user_input:

        st.session_state.messages.append({

            "role": "user",

            "content": user_input
        })


        with st.chat_message("user"):

            st.write(user_input)


        # -------------------------
        # PROCESS CHAT
        # -------------------------

        result = process_chat(
            user_input
        )

        response_stream = result[
            "response"
        ]

        latency = result[
            "latency"
        ]

        trace_id = result[
            "trace_id"
        ]

        unsafe = result[
            "unsafe"
        ]


        # -------------------------
        # OBSERVABILITY SIDEBAR
        # -------------------------

        st.sidebar.subheader(
            "Live Observability"
        )

        st.sidebar.write(
            f"Trace ID: {trace_id[:8]}"
        )

        st.sidebar.write(
            f"Latency: {latency} sec"
        )


        if unsafe:

            st.sidebar.error(
                "Unsafe Prompt Blocked"
            )

        else:

            st.sidebar.success(
                "Guardrails Active"
            )


        # -------------------------
        # STREAM RESPONSE
        # -------------------------

        with st.chat_message("assistant"):

            placeholder = st.empty()

            full_text = ""

            for chunk in response_stream:

                full_text += chunk

                placeholder.markdown(
                    full_text
                )


        # -------------------------
        # SAVE ASSISTANT MESSAGE
        # -------------------------

        st.session_state.messages.append({

            "role": "assistant",

            "content": full_text
        })


# =================================
# OBSERVABILITY DASHBOARD
# =================================

elif page == "Observability Dashboard":

    st.title(
        "Observability Dashboard"
    )

    LOG_FILE = (
        "app/observability_logs.jsonl"
    )

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


    # -----------------------------
    # METRICS
    # -----------------------------

    st.subheader("Runtime Metrics")

    col1, col2 = st.columns(2)

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


    # -----------------------------
    # LATENCY CHART
    # -----------------------------

    st.subheader("Latency Trend")

    fig, ax = plt.subplots()

    ax.plot(df["latency"])

    ax.set_xlabel("Request")

    ax.set_ylabel("Latency")

    st.pyplot(fig)


    # -----------------------------
    # RAW LOGS
    # -----------------------------

    st.subheader("Raw Logs")

    st.dataframe(df)