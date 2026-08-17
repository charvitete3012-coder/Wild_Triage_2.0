import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon
import folium

def calculate_tiger_metrics(df: pd.DataFrame, tiger_id: str) -> dict:
    """Calculates Activity Centroid, Home Range Polygon, and Area in sq km."""
    tiger_data = df[df['tiger_id'] == tiger_id]
    
    if tiger_data.empty:
        return {"centroid": (0.0, 0.0), "hull_points": [], "area_sq_km": 0.0}

    points = tiger_data[['lat', 'lon']].values

    # Activity Centroid
    centroid_lat = float(np.mean(points[:, 0]))
    centroid_lon = float(np.mean(points[:, 1]))

    # Convex Hull (Requires at least 3 distinct points)
    if len(points) >= 3:
        try:
            hull = ConvexHull(points)
            hull_points = points[hull.vertices]
            poly = Polygon(hull_points)
            
            # Approximate lat/lon area conversion to sq km
            avg_lat_rad = np.radians(centroid_lat)
            lat_km = 111.0
            lon_km = 111.0 * np.cos(avg_lat_rad)
            area_sq_km = poly.area * lat_km * lon_km
        except Exception:
            hull_points = points
            area_sq_km = 0.0
    else:
        hull_points = points
        area_sq_km = 0.0

    return {
        "centroid": (round(centroid_lat, 5), round(centroid_lon, 5)),
        "hull_points": hull_points.tolist(),
        "area_sq_km": round(area_sq_km, 2)
    }


def generate_interactive_map(df: pd.DataFrame, village_coords: tuple = (21.1600, 79.1200)) -> folium.Map:
    """Generates Folium map with markers, centroids, home range polygons, and buffer zones."""
    if df.empty:
        return folium.Map(location=[21.1458, 79.0882], zoom_start=12)

    center_lat = df['lat'].mean()
    center_lon = df['lon'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="CartoDB positron")

    color_palette = {
        "TIGER_001": "#E63946",
        "TIGER_002": "#1D3557",
        "TIGER_003": "#2A9D8F",
        "TIGER_004": "#F4A261"
    }

    # Red dashed alert boundary around village settlement
    folium.Circle(
        location=village_coords,
        radius=2500,
        color="red",
        dash_array="5, 5",
        fill=True,
        fill_color="red",
        fill_opacity=0.1,
        popup="CRITICAL ALERT ZONE: Village Settlement Buffer"
    ).add_to(m)

    for tiger_id in df['tiger_id'].unique():
        color = color_palette.get(tiger_id, "#800080")
        metrics = calculate_tiger_metrics(df, tiger_id)
        tiger_df = df[df['tiger_id'] == tiger_id]

        # Sighting Markers
        for _, row in tiger_df.iterrows():
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=5,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.8,
                popup=f"<b>{tiger_id}</b><br>Zone: {row.get('zone', 'N/A')}"
            ).add_to(m)

        # Centroid Marker
        folium.Marker(
            location=metrics['centroid'],
            popup=f"Centroid of {tiger_id}",
            icon=folium.Icon(color="red" if color == "#E63946" else "blue", icon="star")
        ).add_to(m)

        # Home Range Polygon
        if len(metrics['hull_points']) >= 3:
            folium.Polygon(
                locations=metrics['hull_points'],
                color=color,
                weight=2,
                fill=True,
                fill_color=color,
                fill_opacity=0.25,
                popup=f"Home Range ({tiger_id}): {metrics['area_sq_km']} sq km"
            ).add_to(m)

    return m


def export_to_geojson(df: pd.DataFrame) -> dict:
    """Exports sight data as GeoJSON dict."""
    features = []
    for _, row in df.iterrows():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(row['lon']), float(row['lat'])]
            },
            "properties": {
                "tiger_id": str(row['tiger_id']),
                "timestamp": str(row.get('timestamp', '')),
                "zone": str(row.get('zone', 'Core'))
            }
        })
    return {"type": "FeatureCollection", "features": features}