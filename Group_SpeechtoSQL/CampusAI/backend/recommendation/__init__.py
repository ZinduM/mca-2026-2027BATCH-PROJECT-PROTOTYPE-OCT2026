"""
Recommendation package for Campus ERP.

Contains TF-IDF based query recommendation system.
"""

from .recommender import Recommender
from .ir_engine import ir_engine, IREngine


__all__ = [
    "Recommender",
    "ir_engine",
    "IREngine"
]