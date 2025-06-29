import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses Google's Gemini Pro model to generate responses. "
    "To use this app, you need to provide a Gemini API key, which you can get [here](https://ai.google.dev/)."
)

# Ask user for their Gemini API key via `st.text_input`.
gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("Please add your Gemini API key to continue.", icon="🗝️")
else:
    # Configure the Gemini API client.
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')

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

        # Prepare the chat history for Gemini (Gemini expects a simple chat format).
        # Note: Gemini does not support streaming responses in the same way as OpenAI,
        # so we simplify the chat history and use a single prompt or recent context.
        # For a full conversation, you can send the last N messages as context.
        recent_messages = " ".join([m["content"] for m in st.session_state.messages[-5:]])
        # Or, for a simple prompt-response, just use the latest prompt:
        prompt_for_gemini = prompt

        # Generate a response using the Gemini API.
        response = model.generate_content(prompt_for_gemini)

        # Streamlit does not have a direct streaming equivalent for Gemini,
        # but you can display the response as it comes (if you want to simulate streaming).
        # For now, just display the response.
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
