import pandas as pd

from analysis.base import BaseAnalyzer


class TransportAnalyzer(BaseAnalyzer):
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.df['route_count'] = self.df['routes'].apply(len)

    def top_n_data(self, n: int) -> pd.DataFrame:
        """Analyzes and returns the top n stops based on route count."""
        grouped = (
            self.df
            .sort_index()
            .groupby('title', as_index=False)
            .agg({
                'route_count': 'sum',
                'latitude': 'first',
                'longitude': 'first'
            })
        )

        top = grouped.sort_values('route_count', ascending=False).head(n)
        return top
