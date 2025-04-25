from abc import ABC, abstractmethod

import pandas as pd


class BaseAnalyzer(ABC):
    @abstractmethod
    def __init__(self, df: pd.DataFrame):
        pass

    @abstractmethod
    def top_n_data(self, n: int) -> pd.DataFrame:
        """Returns top n records based on analysis criteria."""
        pass
