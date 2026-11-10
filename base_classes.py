from abc import ABC, abstractmethod

class entity(ABC):
    """Clase abracta base para cualquier entidad del sistema Software FJ"""

    def __init__(self, entity_id: str):

        @property
        def entity_id(self) -> str:
            """Devuelve el identificador único de la entidad"""
            return self._entity_id

        @abstractmethod
        def get_summary(self) -> str:
            """Devuelve un resumen de la entidad"""
            pass

class Service(entity):
    """Clase que representa un servicio en el sistema Software FJ"""

    def __init__(self, service_id: str, name: str, base_price: float, is_active: bool = True):
        
        super().__init__(service_id)
        self.name = name
        self.base_price = base_price
        self.is_active = is_active

    def get_summary(self) -> str:
        """Devuelve un resumen del servicio"""
        return f"Service ID: {self.entity_id}, Name: {self.name}, Description: {self.description}"

    @abstractmethod
    def calculate_price(
        self, duration: float, discount: float = 0.0) -> float:
      """Calcula el precio del servicio"""
      pass

    @abstractmethod
    def validate_service(self) -> bool:
        """Valida si el servicio cumple con los criterios necesarios"""
        pass

    def get_summary(self) -> str:
      """Devuelve un resumen del servicio"""
      status = "Available" if self.is_active else "Not Available"
      return f"Service [{self.entity_id}] - {self.name} | Base Price: ${self.base_price:.2f} | Status: {status}"
