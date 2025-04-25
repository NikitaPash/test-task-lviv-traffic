from pathlib import Path
from typing import List, Dict

from analysis.analyzer import TransportAnalyzer
from config import settings
from fetch.fetch_data import EwayStopsFetcher
from process.process_data import EasyWayProcessor
from storage.mysql_store import MySQLStore
from utils.io import save_dataframe_to_csv
from visualization.plots import TrafficVisualisation


def main():
    # Fetch
    fetcher = EwayStopsFetcher(settings.BASE_URL, settings.AJAX_PATH, settings.CITY, settings.LANGUAGE)
    print("\n===== FETCHING RAW DATA =====")
    raw_stops = fetcher.fetch_data()

    # Process
    processor = EasyWayProcessor(raw_stops, valid_transport_types=settings.VALID_TRANSPORT_TYPES)
    print("\n===== PROCESSING RAW DATA =====")
    stops_df = processor.process_data()

    # Save to CSV
    BASE_DIR = Path(__file__).resolve().parent.parent
    print("\n===== SAVING PROCESSES DATA AS CSV =====")
    csv_path = save_dataframe_to_csv(
        stops_df,
        base_path=BASE_DIR,
        subdir=settings.OUTPUT_DIR,
        filename=settings.FULL_CSV_FILENAME,
    )
    print(f"Full processed data saved at {csv_path}")

    # Store
    records: List[Dict] = stops_df.to_dict(orient="records")
    store = MySQLStore()
    print("\n===== DATABASE UPDATE =====")
    print("Starting database refresh...")
    store.save(records)
    print("Database update completed successfully.")

    # Analyze
    analyzer = TransportAnalyzer(stops_df)
    print("\n===== ANALYZE DATA =====")
    top = analyzer.top_n_data(settings.TOP_N)
    print(top)

    # Visualize
    viz = TrafficVisualisation(settings.OUTPUT_DIR)
    print("\n===== VISUALIZE DATA =====")
    viz.bar_chart(top)
    viz.heatmap(top)


if __name__ == '__main__':
    main()
