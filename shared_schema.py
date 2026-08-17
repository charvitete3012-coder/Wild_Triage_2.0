import pandas as pd
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ==========================================
# 1. PYDANTIC SCHEMAS (DATA VALIDATION)
# ==========================================

class CameraSighting(BaseModel):
    """Schema for an individual camera trap detection event."""
    image_id: str
    timestamp: str
    station_id: str
    lat: float
    lon: float
    tiger_id: str = "UNKNOWN"
    confidence: float = 0.0
    is_blank: bool = False
    zone: str = "Core"  # "Core", "Buffer", or "Village_Adjacent"
    file_size_mb: float = 0.0


class AnomalyAlert(BaseModel):
    """Schema for anomaly engine output triggers."""
    alert_id: str
    tiger_id: str
    alert_type: str  # "Village Boundary Breach", "Large Centroid Shift", "Long Absence"
    severity: str    # "CRITICAL", "WARNING", "INFO"
    description: str
    timestamp: str


# ==========================================
# 2. MOCK DATA GENERATOR (FOR OFF-LINE DEV)
# ==========================================

MOCK_SIGHTINGS_DATA = [
    {
        "image_id": "IMG_1001.JPG",
        "timestamp": "2026-08-17 08:30:00",
        "station_id": "ST_CORE_01",
        "lat": 21.1458,
        "lon": 79.0882,
        "tiger_id": "TIGER_001",
        "confidence": 0.94,
        "is_blank": False,
        "zone": "Core",
        "file_size_mb": 4.2
    },
    {
        "image_id": "IMG_1002.JPG",
        "timestamp": "2026-08-17 10:15:00",
        "station_id": "ST_CORE_02",
        "lat": 21.1500,
        "lon": 79.0950,
        "tiger_id": "TIGER_001",
        "confidence": 0.91,
        "is_blank": False,
        "zone": "Core",
        "file_size_mb": 3.8
    },
    {
        "image_id": "IMG_1003.JPG",
        "timestamp": "2026-08-17 14:00:00",
        "station_id": "ST_BUF_01",
        "lat": 21.1400,
        "lon": 79.1000,
        "tiger_id": "TIGER_001",
        "confidence": 0.88,
        "is_blank": False,
        "zone": "Buffer",
        "file_size_mb": 4.0
    },
    {
        "image_id": "IMG_1004.JPG",
        "timestamp": "2026-08-17 09:00:00",
        "station_id": "ST_CORE_03",
        "lat": 21.1700,
        "lon": 79.1100,
        "tiger_id": "TIGER_002",
        "confidence": 0.96,
        "is_blank": False,
        "zone": "Core",
        "file_size_mb": 4.5
    },
    {
        "image_id": "IMG_1005.JPG",
        "timestamp": "2026-08-17 11:30:00",
        "station_id": "ST_CORE_04",
        "lat": 21.1800,
        "lon": 79.1200,
        "tiger_id": "TIGER_002",
        "confidence": 0.93,
        "is_blank": False,
        "zone": "Core",
        "file_size_mb": 4.1
    },
    {
        "image_id": "IMG_1006.JPG",
        "timestamp": "2026-08-17 18:45:00",
        "station_id": "ST_VIL_01",
        "lat": 21.1620,
        "lon": 79.1210,
        "tiger_id": "TIGER_002",
        "confidence": 0.85,
        "is_blank": False,
        "zone": "Village_Adjacent",
        "file_size_mb": 3.9
    },
    {
        "image_id": "IMG_1007.JPG",
        "timestamp": "2026-08-17 07:12:00",
        "station_id": "ST_CORE_01",
        "lat": 21.1458,
        "lon": 79.0882,
        "tiger_id": "NONE",
        "confidence": 0.12,
        "is_blank": True,
        "zone": "Core",
        "file_size_mb": 4.8
    }
]


def load_sightings_dataframe() -> pd.DataFrame:
    """Helper function to return mock sightings directly as a Pandas DataFrame."""
    return pd.DataFrame(MOCK_SIGHTINGS_DATA)