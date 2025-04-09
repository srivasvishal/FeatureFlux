"""
statistics.py

Provides utility functions to compute and update feature-level statistics.
This module computes running statistics for each feature using Welford’s algorithm.
It provides functions to update and finalize stats.
"""

import numpy as np

class FeatureStatsManager:
    def __init__(self):
        # Initialize an empty dict to hold stats for each feature.
        # Each entry will be a dict with keys: count, mean, M2 (for variance computation), min, max.
        self.stats = {}

    def update(self, feature_name: str, value: float):
        """Update statistics for a single feature using Welford's algorithm."""
        if feature_name not in self.stats:
            self.stats[feature_name] = {
                'count': 1,
                'mean': value,
                'M2': 0.0,
                'min': value,
                'max': value
            }
        else:
            stat = self.stats[feature_name]
            stat['count'] += 1
            delta = value - stat['mean']
            stat['mean'] += delta / stat['count']
            delta2 = value - stat['mean']
            stat['M2'] += delta * delta2
            stat['min'] = min(stat['min'], value)
            stat['max'] = max(stat['max'], value)

    def finalize(self, feature_name: str):
        """Finalize and return the statistics for a given feature."""
        stat = self.stats.get(feature_name)
        if stat is None or stat['count'] < 2:
            variance = 0.0
        else:
            variance = stat['M2'] / (stat['count'] - 1)
        return {
            'count': stat['count'],
            'mean': stat['mean'],
            'variance': variance,
            'std': np.sqrt(variance),
            'min': stat['min'],
            'max': stat['max']
        }

    def get_all_stats(self):
        """Return finalized statistics for all features."""
        return {feature: self.finalize(feature) for feature in self.stats}