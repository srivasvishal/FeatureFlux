"""
versioning.py

Implements a simple versioning system for feature schemas.
This module can maintain a version number and list of known features.
"""

import json
import os

VERSION_FILE = "feature_schema_version.json"

def load_version():
    """Load the current schema version from file, or return default."""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            return json.load(f)
    else:
        # Default version 1 with no features
        return {"version": 1, "features": []}

def update_version(new_features):
    """
    Update the schema version if new features are found.
    new_features: list of feature names from the new record.
    """
    current = load_version()
    current_features = set(current["features"])
    new_features_set = set(new_features)
    if new_features_set - current_features:
        # New feature detected; increment version and merge feature lists.
        current["version"] += 1
        current["features"] = list(current_features.union(new_features_set))
        with open(VERSION_FILE, "w") as f:
            json.dump(current, f)
        print(f"Schema version updated to {current['version']} with features {current['features']}")
    return current