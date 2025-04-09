"""
correlation.py

Provides functions to compute and display the Pearson correlation matrix of a dataset.
Uses pandas to compute correlation.
"""

import pandas as pd

def compute_correlation(data: pd.DataFrame) -> pd.DataFrame:
    """
    Computes and returns the Pearson correlation matrix for the given DataFrame.
    
    Parameters:
      data: Pandas DataFrame containing numeric features.
      
    Returns:
      A DataFrame representing the correlation matrix.
    """
    return data.corr()

def print_correlation_matrix(data: pd.DataFrame):
    """
    Prints the correlation matrix in a nicely formatted way.
    """
    corr_matrix = compute_correlation(data)
    print("Correlation Matrix:")
    print(corr_matrix)