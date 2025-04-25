from typing import List, Dict, Any

import pandas as pd

from .base import DataProcessor
from .data_models import StopData


class EasyWayProcessor(DataProcessor):
    def __init__(
            self,
            raw_data: Dict[str, List[Any]],
            valid_transport_types: List[str]
    ):
        self.raw_data = raw_data
        self.valid_transport_types = set(valid_transport_types)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Turn raw data into a DataFrame, using StopData to validate & parse the list.
        """
        records = []
        for stop_id, raw in self.raw_data.items():
            try:
                stop = StopData.from_raw_data(raw)
            except ValueError as e:
                print(f"Skipping stop {stop_id}: {str(e)}")
                continue

            records.append({
                "stop_id": stop_id,
                "latitude": stop.latitude,
                "longitude": stop.longitude,
                "title": stop.title,
                "routes_dict": stop.routes_dict,
            })

        df_raw = pd.DataFrame.from_records(records)
        print(f"Built raw DataFrame with {len(df_raw)} rows")
        return df_raw

    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Take the raw DataFrame and:
          - convert lat/long to decimal degrees
          - drop on-demand stops
          - parse & filter routes by valid_transport_types
          - drop any stops with zero remaining routes
        """
        df = df.copy()

        df = df[~df["title"].str.lower().eq("on demand")]

        def _clean(routes_dict: Dict[str, str]) -> List[Dict[str, str]]:
            """Clean up the routes_dict to a list of dicts with name and transport_type."""
            out: List[Dict[str, str]] = []
            for t_type, route_vals in routes_dict.items():
                if t_type not in self.valid_transport_types or not route_vals:
                    continue
                nums = [n.strip() for n in route_vals.split(",") if n.strip()]
                for num in nums:
                    out.append({
                        "name": num,
                        "transport_type": t_type
                    })
            return out

        df["routes"] = df["routes_dict"].apply(_clean)

        df = df[df["routes"].map(bool)]

        final = df[[
            "stop_id", "title", "latitude", "longitude", "routes"
        ]].reset_index(drop=True)

        return final

    def process_data(self) -> pd.DataFrame:
        df_raw = self.to_dataframe()
        df_final = self.process_dataframe(df_raw)
        print(f"Parsed {len(df_final)} stops with valid routes")
        return df_final
