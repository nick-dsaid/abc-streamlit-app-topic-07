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

st.title("Streamlit App")

form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area("Enter your prompt here", height=200)

if form.form_submit_button("Submit"):
    # response = llm.get_completion(user_prompt)
    response = customer_query_handler.process_user_query(user_prompt)
    st.write(response)

