import streamlit as st
import requests

st.set_page_config(page_title="Emotional Support Chatbot", page_icon="💙")
st.title("💙 Emotional Support Chatbot")
st.write("This chatbot uses DeepSeek-R1 to provide kind and emotionally supportive responses.")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    role, content = msg
    with st.chat_message(role):
        st.markdown(content)

if prompt := st.chat_input("How are you feeling today?"):
    st.session_state["messages"].append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        with requests.post(
            "http://localhost:1134/api/generate",
            json={
                "model": "deepseek-r1",
                "prompt": f"Be empathetic and supportive. User says: {prompt}",
                "stream": True
            },
            stream=True
        ) as r:
            for line in r.iter_lines():
                if line:
                    data = line.decode("utf-8")
                    if data.strip() == "":  # skip empty lines
                        continue
                    try:
                        content = eval(data)  # JSON-like chunks
                        token = content.get("response", "")
                        full_response += token
                        message_placeholder.markdown(full_response + "▌")
                    except:
                        pass

        message_placeholder.markdown(full_response)

    st.session_state["messages"].append(("assistant", full_response))
