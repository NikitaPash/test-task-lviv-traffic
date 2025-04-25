from typing import Dict, List, Any

from pydantic import BaseModel


class StopData(BaseModel):
    """
    Model for raw stop data from the API.
    Structure: [latitude_int, longitude_int, title, routes_dict]
    """
    latitude_int: int
    longitude_int: int
    title: str
    routes_dict: Dict[str, str]

    @property
    def latitude(self) -> float:
        """Convert the raw latitude integer to decimal degrees."""
        return self.latitude_int / 1e6

    @property
    def longitude(self) -> float:
        """Convert the raw longitude integer to decimal degrees."""
        return self.longitude_int / 1e6

    @classmethod
    def from_raw_data(cls, data: List[Any]) -> "StopData":
        """
        Create a StopData object from the raw data.

        Args:
            data: A list containing [latitude_int, longitude_int, title, routes_dict]

        Returns:
            A StopData object
        """
        if len(data) != 4:
            raise ValueError(f"Expected 4 elements in stop data, got {len(data)}")

        return cls(
            latitude_int=data[0],
            longitude_int=data[1],
            title=data[2],
            routes_dict=data[3]
        )
