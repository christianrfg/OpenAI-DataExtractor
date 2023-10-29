import json

from typing import List

import openai
import pandas as pd


def gen_prompt(
        df_features_input: pd.DataFrame
) -> str:
    # Prompt header with instructions
    prompt = "You are provided with a text in triple backticks. Extract the following details from the text along with their specified data types:\n\n"

    # Append input features to extract
    for _, row in df_features_input.iterrows():
        feature_name = row['Feature Name']
        data_type = row['Data Type']

        if (feature_name is not None) and (data_type is not None):
            prompt += f'- "{feature_name}" ({data_type})\n'

    # Prompt footer with final instructions
    prompt += (
        '\nEnsure the response is in JSON format and only includes information explicitly mentioned within the text.\n\n'
        'Text:\n'
        '```\n'
        '{text}\n'
        '```\n\n'
        'Output:'
    )

    return prompt


def extract_features(
        df_features_input: pd.DataFrame,
        input_documents: List[str],
        model: str,
        max_tokens: int,
        temperature: float
) -> pd.DataFrame:
    # Generate prompt
    prompt = gen_prompt(
        df_features_input=df_features_input
    )

    # Extract features for each document
    results = []
    for text in input_documents:
        response = openai.ChatCompletion.create(
            messages=[
                {'role': 'user', 'content': prompt.format(text=text)}
            ],
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )

        r = json.loads(response.choices[0].text.strip('```'))
        results.append(r)

    # Convert to DataFrame to display
    df = pd.DataFrame(results)

    return df
