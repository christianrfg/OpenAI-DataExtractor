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

    sac.divider(
        label='OpenAI Configurations', 
        icon='gear-fill', 
        align='start', 
        dashed=True, 
        bold=True
    )

    openai_organization_id = st.text_input(
        label='OpenAI Organization ID:',
        placeholder='org-...GS4u'
    )
    openai_api_key = st.text_input(
        label='OpenAI API Key:',
        placeholder='sk-...A2v2'
    )

    add_vertical_space()
    sac.divider(
        label='Model Configurations', 
        icon='robot', 
        align='start', 
        dashed=True, 
        bold=True
    )

    # Display alerts if keys aren't provided
    openai_disabled = not openai_organization_id or not openai_api_key
    if openai_disabled:
        sac.alert(
            message='Insert your OpenAI configurations to be able to test the tool.', 
            type='warning', 
            icon=True
        )
    elif (not openai_organization_id.startswith('org-')) or (not openai_api_key.startswith('sk-')):
        sac.alert(
            message="Wrong value for OpenAI credentials. Make sure that OpenAI Organization ID starts with 'org-' and OpenAI API Key starts with 'sk-'", 
            type='error', 
            icon=True
        )
    else:
        openai.organization  = openai_organization_id
        openai.api_key = openai_api_key

    openai_model = st.selectbox(
        'Model:',
        options=['gpt-3.5-turbo-instruct', 'gpt-4'],
        disabled=True if openai_disabled else False,
        help='ID of the model to use.'
    )
    openai_max_tokens = st.number_input(
        'Max. tokens:',
        min_value=64,
        step=32,
        disabled=True if openai_disabled else False,
        help="The maximum number of tokens to generate in the completion. The token count of your prompt plus max_tokens cannot exceed the model's context length."
    )
    openai_temperature = st.slider(
        'Temperature:',
        min_value=0.,
        max_value=1.,
        value=0.,
        step=.1,
        disabled=True if openai_disabled else False,
        help='What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.'
    )

# Section - Try Yourself
colored_header(
    label='🎯 Try Yourself!',
    description='Experiment the tool with your own data!'
)

col1, col2 = st.columns([.7, .3], gap='medium')
with col1:
    input_documents = st.text_area(
        label='**Documents**',
        height=200,
        help='Each line will be treated as an individual document.'
    )

with col2:
    st.markdown('**Features**')
    st.data_editor(
        data=pd.DataFrame(columns=['Feature Name', 'Data Type']),
        use_container_width=True,
        hide_index=True,
        num_rows='dynamic',
        column_config={
            'Data Type': st.column_config.SelectboxColumn(
                options=[
                    '📃 String',
                    '💯 Integer',
                    '*️⃣ Float',
                    '📅 Date',
                    '🕡 Datetime'
                ]
            )
        }
    )

# Section - Examples
add_vertical_space(10)
colored_header(
    label='💡Examples',
    description='Tree use case examples of using OpenAI/GPT to structure data from unstructured data.'
)

# Example selection
example_id = sac.segmented(
    items=[
        sac.SegmentedItem(label='Example 1 - Books', icon='book'),
        sac.SegmentedItem(label='Example 2 - Resumes', icon='file-richtext'),
        sac.SegmentedItem(label='Example 3 - News', icon='newspaper')
    ],
    align='center',
    grow=True,
    return_index=True
)

# Read example from csv file
df, df_features = read_example(example_id=example_id)

# Display input documents from example
col1, col2 = st.columns([.7, .3])
with col1:
    documents_mkd = "**Documents**\n"
    for i, doc in enumerate(df['Document']):
        documents_mkd += f"\n{i+1}. {doc}"
    st.markdown(body=documents_mkd)

# Display input features and data types
with col2:
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
