import math
from typing import Optional


def calculate_haversine_distance(
    lat1: Optional[float],
    lon1: Optional[float],
    lat2: Optional[float],
    lon2: Optional[float]
) -> Optional[float]:
    """
    Calculate the great circle distance between two points on the earth
    specified in decimal degrees using the Haversine formula.
    Returns distance in kilometers, rounded to 2 decimal places.
    """
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return None

    # Earth radius in kilometers
    R = 6371.0

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return round(R * c, 2)
