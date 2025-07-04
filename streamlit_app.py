import streamlit as st
from openai import OpenAI
import os

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot powered by your organization's LLM Foundry. "
    "To use this app, you need to provide your LLM Foundry token."
)

# Ask user for their LLM Foundry token via `st.text_input`.
# Alternatively, you can set this in `.streamlit/secrets.toml` as `LLMFOUNDRY_TOKEN`.
llmfoundry_token = st.text_input("LLM Foundry Token", type="password")
if not llmfoundry_token:
    st.info("Please add your LLM Foundry token to continue.", icon="🗝️")
else:
    # Create an OpenAI client with your LLM Foundry endpoint.
    project_name = "my-test-project"  # Or ask the user for a project name if needed
    client = OpenAI(
        api_key=f"{llmfoundry_token}:{project_name}",
        base_url="https://llmfoundry.straive.com/openai/v1/",
    )

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field.
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the LLM Foundry API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",  # Use your organization's model name
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
