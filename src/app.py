import streamlit as st

from streamlit_extras.add_vertical_space import add_vertical_space


st.set_page_config(
    page_title='OpenAI Data Extractor',
    page_icon='💎',
    layout='wide',
    initial_sidebar_state='expanded'
)

with st.sidebar:
    st.title('💎 OpenAI Data Extractor')
    add_vertical_space(3)

    openai_org = st.text_input(
        label='OpenAI Organization:',
        placeholder='Your organization ID...'
    )
    openai_api_key = st.text_input(
        label='OpenAI API Key:',
        placeholder='sk-...A2v2'
    )
