import streamlit as st
import requests
import json

st.set_page_config(page_title="Emotional Support Chatbot", page_icon="💙")
st.title("💙 Emotional Support Chatbot")
st.write("This chatbot uses DeepSeek-R1 to provide kind and emotionally supportive responses.")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    role, content = msg
    with st.chat_message(role):
        st.markdown(content)

# On new user input
if prompt := st.chat_input("How are you feeling today?"):
    st.session_state["messages"].append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Safe JSON parsing with fallback
        try:
            with requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "deepseek-r1:1.5b",
                    "prompt": f"Be empathetic and supportive. Only provide the final supportive answer without any internal thoughts or explanations. User says: {prompt}",
                      "stream": True,
                },
                stream=True,
            ) as r:
                for line in r.iter_lines():
                    if line:
                        line_str = line.decode("utf-8")
                        if not line_str.strip():
                            continue
                        try:
                            data = json.loads(line_str)
                            token = data.get("response", "")
                            full_response += token
                            message_placeholder.markdown(full_response + "▌")
                        except json.JSONDecodeError:
                            # Ignore bad JSON chunks that might appear during streaming
                            pass
            message_placeholder.markdown(full_response)
        except requests.exceptions.RequestException as e:
            message_placeholder.markdown(f"Error communicating with Ollama API: {e}")
            full_response = f"Error: {e}"

    st.session_state["messages"].append(("assistant", full_response))