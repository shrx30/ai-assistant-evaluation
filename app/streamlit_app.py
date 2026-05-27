import streamlit as st
import time
import uuid
import json

import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime

from app.logger import save_log

from app.models.oss_model import generate_response

from app.memory import (
    add_message,
    get_history
)

from app.advanced_guardrails import (
    guardrail_check
)

from app.planner import (
    plan_tool
)

from app.tools.tool_router import (
    execute_tool
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

    st.write("OSS Assistant Demo")


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
        # Run Guardrails
        # ---------------------------------

        guardrail_result = guardrail_check(
            user_input
        )

        safe = guardrail_result["safe"]

        message = guardrail_result["reason"]

        sanitized_prompt = guardrail_result[
            "sanitized_prompt"
        ]

        # ---------------------------------
        # Add User Message To UI
        # ---------------------------------

        st.session_state.messages.append({

            "role": "user",

            "content": user_input
        })

        # ---------------------------------
        # Add Sanitized Prompt To Memory
        # ---------------------------------

        if sanitized_prompt:

            add_message(
                "user",
                sanitized_prompt
            )

        # ---------------------------------
        # Default Tool Result
        # ---------------------------------

        tool_result = None

        # ---------------------------------
        # Unsafe Prompt
        # ---------------------------------

        if not safe:

            response = message

            latency = 0

            history = get_history()

        # ---------------------------------
        # Safe Prompt
        # ---------------------------------

        else:

            history = get_history()

            start_time = time.time()

            # ---------------------------------
            # Planning Layer
            # ---------------------------------

            plan = plan_tool(
                user_input
            )

            # ---------------------------------
            # Tool Execution Layer
            # ---------------------------------

            if plan:

                tool_result = execute_tool(

                    plan["tool_name"],

                    plan["tool_input"],

                    trace_id
                )

                # ---------------------------------
                # Structured Tool Execution
                # ---------------------------------

                if tool_result:

                    # ---------------------------------
                    # Successful Tool Execution
                    # ---------------------------------

                    if tool_result["status"] == "ok":

                        tool_data = tool_result.get(
                            "data",
                            {}
                        )

                        response = str(tool_data)

                    # ---------------------------------
                    # Tool Failure
                    # ---------------------------------

                    else:

                        error_message = tool_result.get(

                            "error_message",

                            "Unknown tool error."
                        )

                        response = (

                            f"Tool Error: {error_message}"
                        )

                else:

                    response = (
                        "Tool execution failed."
                    )

            # ---------------------------------
            # LLM Fallback
            # ---------------------------------

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
        # Observability Metrics
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

        # ---------------------------------
        # Cost Tracing
        # ---------------------------------

        INPUT_COST_PER_1K = 0.0005

        OUTPUT_COST_PER_1K = 0.001


        estimated_cost = round(

            (

                (input_tokens / 1000)

                * INPUT_COST_PER_1K

            )

            +

            (

                (output_tokens / 1000)

                * OUTPUT_COST_PER_1K

            ),

            6
        )

        # ---------------------------------
        # Sidebar Observability
        # ---------------------------------

        st.sidebar.subheader(
            "Live Observability"
        )

        st.sidebar.write(
            "Model: Qwen2.5-0.5B-Instruct"
        )

        st.sidebar.write(
            f"Trace ID: {trace_id[:8]}"
        )

        st.sidebar.write(
            f"Conversation Length: {len(history)}"
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
            f"Response Length: {len(response)} chars"
        )

        st.sidebar.write(
            f"Generation Speed: {generation_speed} chars/sec"
        )

        st.sidebar.write(
            f"Estimated Cost: ${estimated_cost}"
        )

        st.sidebar.write(
            f"Requests: {st.session_state.request_count}"
        )

        st.sidebar.write(
            f"Timestamp: {datetime.now().strftime('%H:%M:%S')}"
        )

        # ---------------------------------
        # Tool Observability Sidebar
        # ---------------------------------

        if tool_result:

            st.sidebar.write(
                f"Tool Used: {tool_result['tool_name']}"
            )

            st.sidebar.write(
                f"Tool Status: {tool_result['status']}"
            )

            st.sidebar.write(
                f"Tool Version: {tool_result['tool_version']}"
            )

            st.sidebar.write(
                f"Tool Latency: {tool_result['latency_ms']} ms"
            )

        # ---------------------------------
        # Safety Status
        # ---------------------------------

        if safe:

            st.sidebar.success(
                "NeMo + Presidio Guardrails Active"
            )

        else:

            st.sidebar.error(
                "Unsafe Prompt Blocked"
            )

        # ---------------------------------
        # Save Observability Logs
        # ---------------------------------

        log_data = {

            "timestamp": datetime.now().isoformat(),

            "trace_id": trace_id,

            "latency": latency,

            "input_tokens": input_tokens,

            "output_tokens": output_tokens,

            "conversation_length": len(history),

            "response_length": len(response),

            "generation_speed": generation_speed,

            "estimated_cost": estimated_cost,

            "safe_request": safe,

            "request_count": st.session_state.request_count,

            "user_input": user_input,

            "sanitized_prompt": sanitized_prompt,

            "assistant_response": response,

            "planner_output": plan,

            # ---------------------------------
            # Tool Telemetry
            # ---------------------------------

            "tool_status":

                tool_result["status"]

                if tool_result else None,

            "tool_name":

                tool_result["tool_name"]

                if tool_result else None,

            "tool_version":

                tool_result["tool_version"]

                if tool_result else None,

            "tool_latency_ms":

                tool_result["latency_ms"]

                if tool_result else None
        }

        save_log(log_data)

        # ---------------------------------
        # Save Assistant Response
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
        # Streaming Response Rendering
        # ---------------------------------

        with st.chat_message("assistant"):

            placeholder = st.empty()

            full_text = ""

            for word in response.split():

                full_text += word + " "

                placeholder.markdown(full_text)

                time.sleep(0.03)


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


    col1, col2, col3, col4 = st.columns(4)


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

    col4.metric(

        "Total Estimated Cost",

        f"${round(df['estimated_cost'].sum(), 4)}"
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

    st.metric(

        "Average Cost Per Request",

        f"${round(df['estimated_cost'].mean(), 6)}"
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
    # Output Tokens Trend
    # ---------------------------------

    st.subheader("Output Tokens Trend")


    fig2, ax2 = plt.subplots()

    ax2.plot(df["output_tokens"])

    ax2.set_xlabel("Request")

    ax2.set_ylabel("Output Tokens")


    st.pyplot(fig2)


    # ---------------------------------
    # Download Logs
    # ---------------------------------

    st.download_button(

        "Download Observability Logs",

        data=df.to_csv(index=False),

        file_name="observability_logs.csv",

        mime="text/csv"
    )


    # ---------------------------------
    # Raw Logs
    # ---------------------------------

    st.subheader("Raw Observability Logs")

    st.dataframe(df)