from pathlib import Path

import pandas as pd


def save_dataframe_to_csv(
        df: pd.DataFrame,
        base_path: Path,
        subdir: str,
        filename: str
) -> Path:
    """
    Ensure <base_path>/<subdir> exists, write df to CSV there and return the full file path.
    """
    out_dir = base_path / subdir
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        file_path = out_dir / filename
        df.to_csv(file_path, index=False)
        print(f"Saved DataFrame to CSV: {file_path}")
        return file_path
    except Exception as exc:
        print(f"Failed to save DataFrame to {subdir}/{filename}")
        raise exc
