from enum import Enum
from dataclasses import dataclass

class ObstacleType(Enum):
    NONE = "Ninguno"
    GROUND_DROP = "Fosa o desnivel"
    FRONTAL = "Obstáculo frontal"
    AERIAL = "Obstáculo aéreo"

class SensorState(Enum):
    ONLINE = "En línea"
    OFFLINE = "Fuera de línea"
    ERROR = "Error de lectura"

@dataclass
class SensorReading:
    distance_cm: float
    is_valid: bool
    state: SensorState