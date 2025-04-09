"""
bayesian_net.py

Provides functions to create and perform inference on a Bayesian Network.
Uses the pgmpy library for structure learning and inference.
"""

from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator, BayesianEstimator
from pgmpy.inference import VariableElimination
import pandas as pd

def create_bayesian_network(data: pd.DataFrame, structure: list = None) -> BayesianNetwork:
    """
    Creates and fits a Bayesian Network using the given data.
    
    Parameters:
      data: Pandas DataFrame containing the dataset.
      structure: Optional list of tuples representing edges in the BN.
                 If not provided, a simple structure may be inferred or manually defined.
                 
    Returns:
      A fitted BayesianNetwork model.
    """
    if structure is None:
        # For demonstration, define a trivial structure using the first two columns.
        columns = data.columns.tolist()
        if len(columns) < 2:
            raise ValueError("Not enough columns to create a Bayesian Network.")
        structure = [(columns[0], columns[1])]
    
    bn = BayesianNetwork(structure)
    # Fit the parameters using Maximum Likelihood Estimation
    bn.fit(data, estimator=MaximumLikelihoodEstimator)
    return bn

def perform_inference(bn: BayesianNetwork, query: str, evidence: dict):
    """
    Performs inference on the Bayesian Network.
    
    Parameters:
      bn: The BayesianNetwork model.
      query: The variable to query.
      evidence: A dict of evidence variables and their values.
      
    Returns:
      The probability distribution over the query variable.
    """
    infer = VariableElimination(bn)
    result = infer.query(variables=[query], evidence=evidence)
    return result