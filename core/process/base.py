from abc import ABC, abstractmethod

import pandas as pd


class DataProcessor(ABC):

    @abstractmethod
    def to_dataframe(self) -> pd.DataFrame:
        """Converts raw data to a DataFrame."""
        pass

    @abstractmethod
    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processes the DataFrame."""
        pass

    @abstractmethod
    def process_data(self) -> pd.DataFrame:
        """Converts raw json response into a DataFrame and then processes it."""
        pass
