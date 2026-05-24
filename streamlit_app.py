import streamlit as st

from app.models.oss_model import generate_response


st.title("AI Personal Assistant")

st.write("OSS Assistant Demo")


if "messages" not in st.session_state:
    st.session_state.messages = []


user_input = st.chat_input("Type your message...")


if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    response = generate_response(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])