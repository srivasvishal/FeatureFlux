"""
data_utils.py

Contains helper functions for common data operations, such as splitting data,
imputing missing values, or normalizing features.
"""

import pandas as pd
from sklearn.model_selection import train_test_split

def split_data(data: pd.DataFrame, test_size=0.2, random_state=42):
    """
    Splits the DataFrame into training and testing sets.
    
    Parameters:
      data: A pandas DataFrame.
      test_size: Proportion of the dataset to include in the test split.
      random_state: Seed used by the random number generator.
      
    Returns:
      A tuple (train_df, test_df).
    """
    train_df, test_df = train_test_split(data, test_size=test_size, random_state=random_state)
    return train_df, test_df

def impute_missing(data: pd.DataFrame, method="mean"):
    """
    Imputes missing values in the DataFrame.
    
    Parameters:
      data: A pandas DataFrame.
      method: Imputation method ('mean', 'median', or 'mode').
      
    Returns:
      A DataFrame with imputed values.
    """
    if method == "mean":
        return data.fillna(data.mean())
    elif method == "median":
        return data.fillna(data.median())
    elif method == "mode":
        return data.fillna(data.mode().iloc[0])
    else:
        raise ValueError("Unsupported imputation method")