import streamlit as st
import openai
import pandas as pd
import streamlit_antd_components as sac

from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.colored_header import colored_header


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

colored_header(
    label='Examples',
    description='Tree use case examples of using OpenAI/GPT to structure data from unstructured data.'
)

sac.segmented(
    items=[
        sac.SegmentedItem(label='Example 1'),
        sac.SegmentedItem(label='Example 2'),
        sac.SegmentedItem(label='Example 3')
    ],
    align='center',
    grow=True
)

documents = """
In 'Pride and Prejudice' by Jane Austen, Elizabeth Bennet and Mr. Darcy navigate societal pressures and find love.
J.K. Rowling's 'Harry Potter and the Sorcerer's Stone' introduces us to a young wizard discovering his identity.
In 'To Kill a Mockingbird' by Harper Lee, Scout Finch witnesses racial injustice in her hometown.
Bilbo Baggins embarks on an unexpected adventure in J.R.R. Tolkien's 'The Hobbit'.
'Brave New World' by Aldous Huxley depicts a future society driven by technological advancements.
""".strip()
st.text_area(
    label='Samples',
    value=documents,
    height=150
)
st.text_input(
    label='Features to extract',
    value='Title, Author, '
)

df = pd.read_csv('data/book_summaries.csv')
st.dataframe(
    data=df,
    hide_index=True    
)

prompt = """
You are provided with a text in triple backticks. Extract the following details from the text along with their specified data types:

- "Title" (string)
- "Author" (string)
- "Main Character" (string)
- "Plot Summary" (string)

Ensure the response is in JSON format and only includes information explicitly mentioned within the text.


Text:
```
{text}
```

Output:
""".strip()
st.text_area(
    'Prompt',
    value=prompt,
    height=400
)

colored_header(
    label='Try Yourself',
    description='Experiment the tool with your own data!'
)
