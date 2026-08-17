# gis_module.py
import folium
import numpy as np

def generate_map(records):
    """
    Plots camera stations, tiger observations, and center locations.
    """
    # Extract coordinates for non-blank detections
    coords = [[r["lat"], r["lon"]] for r in records if not r["is_blank"]]
    
    if not coords:
        # Default center if no records exist
        center = [21.1458, 79.0882]
    else:
        center = np.mean(coords, axis=0).tolist()

    m = folium.Map(location=center, zoom_start=12, tiles="OpenStreetMap")

    # Plot camera stations
    for rec in records:
        if rec["is_blank"]:
            continue
            
        color = "red" if rec["station_type"] == "village_adjacent" else "green"
        
        folium.Marker(
            location=[rec["lat"], rec["lon"]],
            popup=f"Tiger: {rec['tiger_id']} | Station: {rec['station_id']}",
            tooltip=f"{rec['tiger_id']} ({rec['region_type']})",
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)

    return m