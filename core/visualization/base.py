from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class BaseVisualizer(ABC):
    @abstractmethod
    def __init__(self, output_dir: Path):
        pass

    @abstractmethod
    def bar_chart(self, df: pd.DataFrame, filename: str):
        """Creates a bar chart visualization."""
        pass

    @abstractmethod
    def heatmap(self, df: pd.DataFrame, filename: str):
        """Creates a heatmap visualization."""
        pass
