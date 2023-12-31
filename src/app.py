import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

from openai import OpenAI
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.colored_header import colored_header

from data import read_example
from utils import extract_features


st.set_page_config(
    page_title='OpenAI Data Extractor',
    page_icon='💎',
    layout='wide',
    initial_sidebar_state='expanded'
)

with st.sidebar:
    st.title('💎 OpenAI Data Extractor')
    st.markdown("""A powerful OpenAI tool for extracting meaningful features from unstructured text, transforming raw data into structured data.""")

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

    # Check if keys were provide
    openai_disabled = not openai_organization_id or not openai_api_key

    openai_model = st.selectbox(
        'Model:',
        options=['gpt-3.5-turbo', 'gpt-4'],
        disabled=True if openai_disabled else False,
        help='ID of the model to use.'
    )

    # Change to new OpenAI models
    if openai_model == 'gpt-3.5-turbo':
        openai_model = 'gpt-3.5-turbo-1106'
    else:
        openai_model = 'gpt-4-1106-preview'

    openai_max_tokens = st.number_input(
        'Max. tokens:',
        min_value=64,
        step=32,
        disabled=True if openai_disabled else False,
        help="The maximum number of tokens to generate in the completion. The token count of your prompt plus max_tokens cannot exceed the model's context length."
    )

# Section - Try Yourself
colored_header(
    label='🎯 Try Yourself!',
    description='Test the tool using your own data for a personalized experience!'
)

# Display alerts if keys aren't provided
if openai_disabled:
    sac.alert(
        message='OpenAI Configurations', 
        description='Insert your OpenAI Configurations on the left menu to be able to test the tool.',
        type='warning', 
        icon=True
    )
elif (not openai_organization_id.startswith('org-')) or (not openai_api_key.startswith('sk-')):
    sac.alert(
        message='Wrong value for OpenAI credentials.',
        description="Make sure that OpenAI Organization ID starts with 'org-' and OpenAI API Key starts with 'sk-'", 
        type='error', 
        icon=True
    )
else:
    # Initialize OpenAI client
    openai_client = OpenAI(
        api_key=openai_api_key,
        organization=openai_organization_id,
        max_retries=5
    )


col1, col2 = st.columns([.7, .3], gap='medium')
with col1:
    input_documents = st.text_area(
        label='**Documents**',
        height=200,
        help='Each line will be treated as an individual document.',
        disabled=openai_disabled
    )

with col2:
    st.markdown('**Features**')
    df_features_input = st.data_editor(
        data=pd.DataFrame(columns=['Feature Name', 'Data Type']),
        use_container_width=True,
        hide_index=True,
        num_rows='dynamic',
        disabled=openai_disabled,
        column_config={
            'Data Type': st.column_config.SelectboxColumn(
                options=[
                    '📃 String',
                    '💯 Integer',
                    '*️⃣ Float',
                    '📅 Date',
                    '🕡 Datetime'
                ],
                required=True
            )
        }
    )

# Split documents by line
input_documents = input_documents.split('\n')

# Submit button
add_vertical_space(2)
button_cols = st.columns(3)
if button_cols[1].button('Extract', type='primary', use_container_width=True, disabled=openai_disabled):
    add_vertical_space()

    # Alert when no features are provided
    if df_features_input.empty:
        sac.alert(
            message='Input warning',
            description='You must insert documents and features to extract to be able to test the tool.', 
            type='warning', 
            icon=True
        )

    # Extract features and display results
    else:
        # Extract features with OpenAI
        df_features = extract_features(
            df_features_input=df_features_input,
            input_documents=input_documents,
            openai_client=openai_client,
            model=openai_model,
            max_tokens=openai_max_tokens
        )
        
        # Display results
        st.markdown('**Results**')
        st.dataframe(
            data=df_features,
            hide_index=True,
            use_container_width=True
        )

# Section - Examples
add_vertical_space(3)
colored_header(
    label='💡Examples',
    description="Three illustrative examples showcasing how OpenAI's GPT can transform unstructured data into structured formats."
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
