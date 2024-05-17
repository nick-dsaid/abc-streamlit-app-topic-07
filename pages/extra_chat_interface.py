import streamlit as st
from helper_functions import llm
from logics import customer_query_handler

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App",
    page_icon="images/launchpad-icon.png"
)
# endregion <--------- Streamlit App Configuration --------->


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("Streamlit App")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What is up?")
if prompt:
    # display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant message
    with st.spinner("Thinking..."):
        # Process user query
        response = customer_query_handler.process_user_query(prompt)

        # Add system message to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.markdown(response)

    # Save chat history
    st.session_state.messages = st.session_state.messages[-10:]

