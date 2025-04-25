import os
from pathlib import Path

import folium
import matplotlib.pyplot as plt
from folium.plugins import HeatMap

from visualization.base import BaseVisualizer


class TrafficVisualisation(BaseVisualizer):
    def __init__(self, output_dir: Path):
        self.out_dir = Path(output_dir)
        self.out_dir.mkdir(exist_ok=True)

    def bar_chart(self, df, filename: str = "top_stops.png"):
        fig, ax = plt.subplots(figsize=(8, 5))
        df_sorted = df.sort_values('route_count')
        ax.barh(df_sorted['title'], df_sorted['route_count'])
        ax.set_xlabel('Unique Routes')
        ax.set_title('Top Stops by Route Count')
        fig.tight_layout()
        out = self.out_dir / filename
        fig.savefig(out)
        print(f"Bar chart saved to {out}")

    def heatmap(self, df, filename: str = "heatmap.html"):
        m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], zoom_start=13)
        HeatMap(
            data=df[['latitude', 'longitude']].values.tolist(),
            radius=15,
            blur=25
        ).add_to(m)
        for _, row in df.iterrows():
            folium.Circle(
                location=(row.latitude, row.longitude),
                radius=100,
                weight=1,
                color='blue',
                fill=True,
                fill_opacity=0.1,
                popup=f"{row.title}: {row.route_count} routes"
            ).add_to(m)
        path = os.path.join(self.out_dir, filename)
        m.save(path)
        print(f"Heatmap saved to {path}")
