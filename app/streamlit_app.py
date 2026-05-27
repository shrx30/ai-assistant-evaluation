import streamlit as st
import time
import uuid
import json

import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime

from logger import save_log

from models.oss_model import generate_response

from memory import (
    add_message,
    get_history
)


# ---------------------------------
# Page Config
# ---------------------------------

st.set_page_config(

    page_title="AI Assistant + Observability",

    page_icon="🤖",

    layout="wide"
)


# ---------------------------------
# Sidebar Navigation
# ---------------------------------

page = st.sidebar.radio(

    "Navigation",

    [
        "Chatbot",
        "Observability Dashboard"
    ]
)


# =================================
# CHATBOT PAGE
# =================================

if page == "Chatbot":

    st.title("AI Personal Assistant")

    st.write("NVIDIA Hosted Assistant")


    # ---------------------------------
    # Session State
    # ---------------------------------

    if "messages" not in st.session_state:

        st.session_state.messages = []


    if "request_count" not in st.session_state:

        st.session_state.request_count = 0


    # ---------------------------------
    # Display Chat History
    # ---------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])


    # ---------------------------------
    # User Input
    # ---------------------------------

    user_input = st.chat_input(
        "Type your message..."
    )


    # ---------------------------------
    # Main Chat Flow
    # ---------------------------------

    if user_input:

        trace_id = str(uuid.uuid4())

        st.session_state.request_count += 1


        # ---------------------------------
        # Show User Message
        # ---------------------------------

        st.session_state.messages.append({

            "role": "user",

            "content": user_input
        })

        with st.chat_message("user"):

            st.write(user_input)


        # ---------------------------------
        # Memory History
        # ---------------------------------

        add_message(
            "user",
            user_input
        )

        history = get_history()


        # ---------------------------------
        # Lightweight Guardrails
        # ---------------------------------

        blocked_words = [

            "hack",
            "malware",
            "bomb",
            "explosive"
        ]

        unsafe = any(

            word in user_input.lower()

            for word in blocked_words
        )


        # ---------------------------------
        # Response Generation
        # ---------------------------------

        start_time = time.time()

        if unsafe:

            response = (
                "Unsafe request blocked."
            )

        else:

            response = generate_response(
                history
            )

        end_time = time.time()

        latency = round(
            end_time - start_time,
            2
        )


        # ---------------------------------
        # Metrics
        # ---------------------------------

        input_tokens = len(
            str(history).split()
        )

        output_tokens = len(
            response.split()
        )

        generation_speed = round(

            len(response) / max(latency, 0.01),

            2
        )

        estimated_cost = 0


        # ---------------------------------
        # Sidebar Observability
        # ---------------------------------

        st.sidebar.subheader(
            "Live Observability"
        )

        st.sidebar.write(
            f"Trace ID: {trace_id[:8]}"
        )

        st.sidebar.write(
            f"Latency: {latency} sec"
        )

        st.sidebar.write(
            f"Input Tokens: {input_tokens}"
        )

        st.sidebar.write(
            f"Output Tokens: {output_tokens}"
        )

        st.sidebar.write(
            f"Generation Speed: {generation_speed}"
        )

        st.sidebar.write(
            f"Requests: {st.session_state.request_count}"
        )


        if unsafe:

            st.sidebar.error(
                "Unsafe Prompt Blocked"
            )

        else:

            st.sidebar.success(
                "Guardrails Active"
            )


        # ---------------------------------
        # Save Logs
        # ---------------------------------

        log_data = {

            "timestamp": datetime.now().isoformat(),

            "trace_id": trace_id,

            "latency": latency,

            "input_tokens": input_tokens,

            "output_tokens": output_tokens,

            "response_length": len(response),

            "generation_speed": generation_speed,

            "assistant_response": response,

            "unsafe_request": unsafe
        }

        save_log(log_data)


        # ---------------------------------
        # Save Assistant Message
        # ---------------------------------

        add_message(
            "assistant",
            response
        )

        st.session_state.messages.append({

            "role": "assistant",

            "content": response
        })


        # ---------------------------------
        # Streaming Render
        # ---------------------------------

        with st.chat_message("assistant"):

            placeholder = st.empty()

            full_text = ""

            for word in response.split():

                full_text += word + " "

                placeholder.markdown(full_text)

                time.sleep(0.02)


# =================================
# DASHBOARD PAGE
# =================================

elif page == "Observability Dashboard":

    st.title("Observability Dashboard")

    LOG_FILE = "app/observability_logs.jsonl"

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
    # Latency Trend
    # ---------------------------------

    st.subheader("Latency Trend")

    fig, ax = plt.subplots()

    ax.plot(df["latency"])

    ax.set_xlabel("Request")

    ax.set_ylabel("Latency")

    st.pyplot(fig)


    # ---------------------------------
    # Raw Logs
    # ---------------------------------

    st.subheader("Raw Logs")

    st.dataframe(df)