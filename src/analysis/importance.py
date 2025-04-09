"""
importance.py

Provides functions to compute feature importance.
For scikit-learn models, it retrieves the feature_importances_ attribute.
For other models, it could integrate SHAP values (not implemented here for brevity).
"""

def get_feature_importance(model):
    """
    Given a trained model that has a feature_importances_ attribute, return a dict mapping
    feature names to their importance.
    """
    if hasattr(model, "feature_importances_"):
        # Assume model has attribute 'feature_names_in_' listing the features.
        return dict(zip(model.feature_names_in_, model.feature_importances_))
    else:
        raise ValueError("Model does not support feature importance extraction.")

