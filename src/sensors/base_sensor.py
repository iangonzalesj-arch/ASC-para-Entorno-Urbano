from abc import ABC, abstractmethod
from src.core.types import SensorReading

class DistanceSensor(ABC):
    """
    Clase abstracta que define la interfaz estándar para cualquier
    sensor de distancia del bastón inteligente.
    """
    
    def __init__(self, sensor_id: str):
        self._sensor_id = sensor_id
        self._is_connected = False
        
    @abstractmethod
    def initialize(self) -> bool:
        """
        Inicializa la comunicación con el hardware.
        Debe ser implementado por las clases hijas.
        """
        pass
        
    @abstractmethod
    def get_reading(self) -> SensorReading:
        """
        Obtiene la lectura actual de distancia.
        Debe ser implementado por las clases hijas.
        """
        pass
        
    def get_id(self) -> str:
        """Método concreto heredable."""
        return self._sensor_id