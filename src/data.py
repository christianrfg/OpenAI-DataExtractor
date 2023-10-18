from typing import Tuple

import pandas as pd


def read_example(
        example_id: int
) -> tuple[pd.DataFrame]:
    """
    Reads a specific example dataset based on the provided example ID.

    Args:
        example_id (int): The ID corresponding to the desired dataset.
                          - 0: Book summaries.
                          - 1: Resumes.
                          - 2: News.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: The corresponding dataset as a pandas DataFrame and it's features.

    Raises:
        ValueError: If the provided example_id is not valid (0, 1, or 2).

    Examples:
        >>> df, df_features = read_example(0)
        >>> print(df.head())
        # Outputs the first few rows of the book summaries dataset.
        >>> print(df_features)
        # Outputs the features extracted from the dataset.
    """
    if example_id == 0:
        df = pd.read_csv('data/book_summaries.csv')

        df_features = pd.DataFrame(
            data=[
                ['Title', '📃 String'],
                ['Author', '📃 String'],
                ['Main Character', '📃 String'],
                ['Plot Summary', '📃 String']
            ],
            columns=['Feature Name', 'Data Type']
        )

        return df, df_features

    elif example_id == 1:
        df = pd.read_csv('data/resumes.csv')

        df_features = pd.DataFrame(
            data=[
                ['Name', '📃 String'],
                ['Company', '📃 String'],
                ['Start Year', '💯 Integer'],
                ['End Yer', '💯 Integer'],
                ['Position', '📃 String']
            ],
            columns=['Feature Name', 'Data Type']
        )

        return df, df_features

    elif example_id == 2:
        df = pd.read_csv('data/news.csv')

        df_features = pd.DataFrame(
            data=[
                ['Date', '📅 Date'],
                ['Location', '📃 String'],
                ['Event', '📃 String'],
                ['Impact', '📃 String']
            ],
            columns=['Feature Name', 'Data Type']
        )

        return df, df_features

    else:
        raise ValueError('Invalid example id!')
