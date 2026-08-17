# shared_schema.py

MOCK_DATABASE = [
    {
        "image_id": "IMG_101.jpg",
        "timestamp": "2026-08-17 08:30:00",
        "station_id": "ST_CORE_01",
        "lat": 21.1458,
        "lon": 79.0882,
        "tiger_id": "TIGER_001",
        "is_blank": False,
        "confidence": 0.94,
        "file_size_mb": 3.8,
        "region_type": "Core",
        "last_seen_days": 2,
        "station_type": "standard"
    },
    {
        "image_id": "IMG_102.jpg",
        "timestamp": "2026-08-17 09:15:00",
        "station_id": "ST_CORE_02",
        "lat": 21.1520,
        "lon": 79.0950,
        "tiger_id": "TIGER_001",
        "is_blank": False,
        "confidence": 0.91,
        "file_size_mb": 4.1,
        "region_type": "Core",
        "last_seen_days": 2,
        "station_type": "standard"
    },
    {
        "image_id": "IMG_103.jpg",
        "timestamp": "2026-08-17 10:00:00",
        "station_id": "ST_BUF_05",
        "lat": 21.1800,
        "lon": 79.1200,
        "tiger_id": "TIGER_002",
        "is_blank": False,
        "confidence": 0.88,
        "file_size_mb": 3.5,
        "region_type": "Buffer",
        "last_seen_days": 45,
        "station_type": "village_adjacent"
    },
    {
        "image_id": "IMG_104.jpg",
        "timestamp": "2026-08-17 11:20:00",
        "station_id": "ST_CORE_03",
        "lat": 21.1390,
        "lon": 79.0750,
        "tiger_id": "NONE",
        "is_blank": True,
        "confidence": 0.12,
        "file_size_mb": 2.9,
        "region_type": "Core",
        "last_seen_days": 0,
        "station_type": "standard"
    }
]