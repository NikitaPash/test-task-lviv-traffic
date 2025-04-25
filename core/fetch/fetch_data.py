from typing import Dict, Any, List

import cloudscraper

from config import settings
from fetch.base import DataFetcher


class EwayStopsFetcher(DataFetcher):
    def __init__(self, base_url: str, ajax_path: str, city: str, language: str):
        self.base_url = base_url
        self.ajax_path = ajax_path
        self.city = city
        self.language = language
        self.scraper = cloudscraper.create_scraper(
            browser={"custom": settings.USER_AGENT}
        )
        self.scraper.cookies.set("city[key]", self.city)
        self.scraper.cookies.set("lang", self.language)

    def fetch_data(self) -> Dict[str, List[Any]]:
        """Fetches stop data from the Eway."""
        url = f"{self.base_url}{self.ajax_path}/{self.language}/{self.city}/stops"
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"{self.base_url}/{self.language}/cities/{self.city}/routes"
        }
        try:
            print(f"Fetching stops from {url}")
            response = self.scraper.get(url, headers=headers)
            response.raise_for_status()
            raw_stops = response.json()
            print(f"Fetched {len(raw_stops)} stops successfully")
            return raw_stops
        except Exception as e:
            print(f"Failed to fetch stops: {str(e)}")
            raise e
