import pandas as pd


def read_example(
        example_id: int
) -> pd.DataFrame:
    """
    Reads a specific example dataset based on the provided example ID.

    Args:
        example_id (int): The ID corresponding to the desired dataset.
                          - 0: Book summaries.
                          - 1: Resumes.
                          - 2: News.

    Returns:
        pd.DataFrame: The corresponding dataset as a pandas DataFrame.

    Raises:
        ValueError: If the provided example_id is not valid (0, 1, or 2).

    Examples:
        >>> df = read_example(0)
        >>> print(df.head())
        # Outputs the first few rows of the book summaries dataset.
    """
    if example_id == 0:
        df = pd.read_csv('data/book_summaries.csv')
        return df

    elif example_id == 1:
        df = pd.read_csv('data/resumes.csv')
        return df

    elif example_id == 2:
        df = pd.read_csv('data/news.csv')
        return df

    else:
        raise ValueError('Invalid example id!')
