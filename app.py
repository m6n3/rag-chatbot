"""Chatbot Web APP."""

import chatbot_llm
import gcp_stub
import logging
import os
import streamlit as st
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Globals
api_key_valid = False

with st.sidebar:
    st.title("🤖 Cloud Healthcare API Chatbot")
    if not os.environ.get("GOOGLE_API_KEY"):
        api_key = st.text_input("Enter PALM API token:", type="password")
    else:
        api_key = os.environ.get("GOOGLE_API_KEY")

    # Hack for validating api_key.
    if api_key and len(api_key) > 10:
        api_key_valid = True
        os.environ["GOOGLE_API_KEY"] = api_key
        st.success("Proceed to entering your prompt message!", icon="👉")
    elif api_key:
        st.error("API key is invalid", icon="🚨")


if "messages" not in st.session_state:
    st.session_state.messages = []


if api_key_valid:
    llm_chain = None
    with st.spinner("Downloading Cloud Healthcare public docs ..."):
        llm_chain = chatbot_llm.get_llm()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How Can I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("▌")
            full_response = ""
            try:
                full_response = llm_chain.run(
                    prompt,
                    gcp_stub.get_consent_store_context(),
                )
                message_placeholder.markdown(full_response)
            except Exception as e:
                message_placeholder.markdown(f"Something went wrong, try again \n {e}")

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
