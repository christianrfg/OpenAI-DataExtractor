import streamlit as st
import openai
import pandas as pd
import streamlit_antd_components as sac

from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.colored_header import colored_header

from data import read_example


st.set_page_config(
    page_title='OpenAI Data Extractor',
    page_icon='💎',
    layout='wide',
    initial_sidebar_state='expanded'
)

with st.sidebar:
    st.title('💎 OpenAI Data Extractor')
    add_vertical_space(3)

    openai_organization_id = st.text_input(
        label='OpenAI Organization ID:',
        placeholder='org-...GS4u'
    )
    openai_api_key = st.text_input(
        label='OpenAI API Key:',
        placeholder='sk-...A2v2'
    )

    openai.organization  = openai_organization_id
    openai.api_key = openai_api_key

# Section to test the tool
colored_header(
    label='Try Yourself!',
    description='Experiment the tool with your own data!'
)

# Display warnings if keys aren't provided
if not openai_organization_id or not openai_api_key:
    sac.alert(
        message='Insert your OpenAI configurations in the sidemenu to be able to test the tool.', 
        type='warning', 
        icon=True
    )
elif (not openai_organization_id.startswith('org-')) or (not openai_api_key.startswith('sk-')):
    sac.alert(
        message="Wrong value for OpenAI credentials. Make sure that OpenAI Organization ID starts with 'org-' and OpenAI API Key starts with 'sk-'", 
        type='error', 
        icon=True
    )

# Example's section
add_vertical_space(10)
colored_header(
    label='Examples',
    description='Tree use case examples of using OpenAI/GPT to structure data from unstructured data.'
)

# Example selection
example_id = sac.segmented(
    items=[
        sac.SegmentedItem(label='Example 1 - Books'),
        sac.SegmentedItem(label='Example 2 - Resumes'),
        sac.SegmentedItem(label='Example 3 - News')
    ],
    align='center',
    grow=True,
    return_index=True
)

# Read example from csv file
df = read_example(example_id=example_id)

# Display input documents from example
col1, col2 = st.columns([.7, .3])
with col1:
    documents_mkd = "**Documents**\n"
    for i, doc in enumerate(df['Document']):
        documents_mkd += f"\n{i+1}. {doc}"
    st.markdown(body=documents_mkd)

# Display input features and data types
with col2:
    df_features = pd.DataFrame(
        data=[
            ['Title', '📃 String'],
            ['Author', '📃 String'],
            ['Main Character', '📃 String'],
            ['Plot Summary', '📃 String']
        ],
        columns=['Feature Name', 'Data Type']
    )

    st.markdown('**Features**')
    st.dataframe(
        df_features,
        hide_index=True,
        column_config={
            'Feature Name': st.column_config.TextColumn(width=120),
            'Data Type': st.column_config.SelectboxColumn(width=120)
        },
        use_container_width=True
    )

add_vertical_space(2)
st.markdown('**Results**')
st.dataframe(
    data=df,
    hide_index=True,
    column_config={
        'Document': None
    },
    use_container_width=True
)
