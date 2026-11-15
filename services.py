from abc import abstractmethod

from base_classes import Service          

# EXCEPCION PROPIA

class ServiceError(ValueError):
    """Error lanzado cuando un servicio o sus parametros no son validos."""

# CLASE ABSTRACTA INTERMEDIA
# Clase para servicios que implementa validaciones y resumen, pero sigue siendo abstracta.

class ManagedService(Service):

    def __init__(self, service_id: str, name: str, base_price: float, is_active: bool = True):
        # Primero validamos los parametros de la clase base (Service) y luego llamamos a su constructor.
        if not isinstance(service_id, str) or not service_id.strip():
            raise ServiceError("El ID del servicio es obligatorio.")
        if not isinstance(name, str) or len(name.strip()) < 3:
            raise ServiceError("El nombre del servicio debe tener al menos 3 caracteres.")
        if not isinstance(base_price, (int, float)) or base_price <= 0:
            raise ServiceError("El precio base debe ser un numero mayor que 0.")

        # Llamamos al constructor de la clase base (Service) con los parametros validados.
        super().__init__(service_id.strip(), name.strip(), float(base_price), is_active)

        # Guardamos el ID del servicio en el atributo _entity_id (heredado del concepto de Entity) 
        self._entity_id = service_id.strip()

    @property
    def entity_id(self) -> str:
        """Devuelve el identificador único de la entidad"""
        return self._entity_id

    @property
    def service_id(self) -> str:
        """Devuelve el identificador único del servicio"""
        return self._entity_id

    #  Validacion comun reutilizada por las hijas 
    @staticmethod
    def _check_common(duration: float, discount: float) -> None:
        """Valida duracion y descuento, que son iguales para todo servicio."""
        if not isinstance(duration, (int, float)) or duration <= 0:
            raise ServiceError("La duracion debe ser un numero mayor que 0.")
        if not isinstance(discount, (int, float)) or not 0 <= discount <= 1:
            raise ServiceError("El descuento debe estar entre 0 y 1 (ej: 0.10 = 10%).")

    @staticmethod
    def _apply_discount(amount: float, discount: float) -> float:
        """Aplica descuento y redondea a 2 decimales."""
        return round(amount * (1 - discount), 2)

    def get_summary(self) -> str:
        """Resumen base (de Service) que las hijas ampliaran."""
        return super().get_summary()


# ======================================================================
# Primer servicio: Reserva de sala 
# ======================================================================
class RoomReservation(ManagedService):
    """Reserva de una sala por horas. `duration` = horas."""

    # Si hay mas de este numero de asistentes se cobra recargo.
    ATTENDEES_SURCHARGE_LIMIT = 10
    SURCHARGE_RATE = 0.15  # 15 %

    def __init__(self, service_id, name, base_price, capacity: int, attendees: int, is_active: bool = True):
        super().__init__(service_id, name, base_price, is_active)
        self.capacity = capacity
        self.attendees = attendees

    def validate_service(self) -> bool:
        """Sobrescrito: los asistentes deben caber en la sala."""
        if not isinstance(self.capacity, int) or self.capacity <= 0:
            raise ServiceError("La capacidad de la sala debe ser un entero positivo.")
        if not isinstance(self.attendees, int) or self.attendees <= 0:
            raise ServiceError("Debe haber al menos 1 asistente.")
        if self.attendees > self.capacity:
            raise ServiceError(
                f"{self.attendees} asistentes superan la capacidad ({self.capacity})."
            )
        return True

    def calculate_price(self, duration: float, discount: float = 0.0) -> float:
        """Sobrescrito: precio por hora + recargo si el grupo es grande."""
        self._check_common(duration, discount)
        self.validate_service()

        total = self.base_price * duration
        if self.attendees > self.ATTENDEES_SURCHARGE_LIMIT:
            total *= 1 + self.SURCHARGE_RATE
        return self._apply_discount(total, discount)

    def get_summary(self) -> str:
        """Sobrescrito: agrega datos propios de la sala al resumen base."""
        return (f"{super().get_summary()} | Tipo: Reserva de sala | "
                f"Capacidad: {self.capacity} | Asistentes: {self.attendees}")


# ======================================================================
# Segundo servicio: Alquiler de equipos
# ======================================================================
class EquipmentRental(ManagedService):
    """Alquiler de equipos por dias. `duration` = dias."""

    INSURANCE_RATE = 0.05  # 5 % de seguro sobre el alquiler

    def __init__(self, service_id, name, base_price, units: int, insured: bool = True, is_active: bool = True):
        super().__init__(service_id, name, base_price, is_active)
        self.units = units
        self.insured = insured

    def validate_service(self) -> bool:
        """Sobrescrito: debe alquilarse al menos una unidad."""
        if not isinstance(self.units, int) or self.units <= 0:
            raise ServiceError("Las unidades a alquilar deben ser un entero positivo.")
        if self.units > 50:
            raise ServiceError("No se pueden alquilar mas de 50 unidades a la vez.")
        return True

    def calculate_price(self, duration: float, discount: float = 0.0) -> float:
        """Sobrescrito: dias x unidades (+ seguro opcional)."""
        self._check_common(duration, discount)
        self.validate_service()

        total = self.base_price * self.units * duration
        if self.insured:
            total *= 1 + self.INSURANCE_RATE
        return self._apply_discount(total, discount)

    def get_summary(self) -> str:
        insurance = "con seguro" if self.insured else "sin seguro"
        return (f"{super().get_summary()} | Tipo: Alquiler de equipos | "
                f"Unidades: {self.units} ({insurance})")


# ======================================================================
# Tercer servicio: Asesoria especializada
# ======================================================================
class SpecializedConsulting(ManagedService):
    """Asesoria por horas con tarifa segun nivel. `duration` = horas."""

    # Multiplicador de tarifa segun el nivel del asesor.
    LEVEL_MULTIPLIER = {"junior": 1.0, "senior": 1.5, "experto": 2.0}
    MIN_BILLABLE_HOURS = 1  # se cobra minimo 1 hora

    def __init__(self, service_id, name, base_price, level: str, is_active: bool = True):
        super().__init__(service_id, name, base_price, is_active)
        self.level = level.lower() if isinstance(level, str) else level

    def validate_service(self) -> bool:
        """Sobrescrito: el nivel debe existir en la tabla de tarifas."""
        if self.level not in self.LEVEL_MULTIPLIER:
            valid = ", ".join(self.LEVEL_MULTIPLIER)
            raise ServiceError(f"Nivel '{self.level}' no valido. Opciones: {valid}.")
        return True

    def calculate_price(self, duration: float, discount: float = 0.0) -> float:
        """Sobrescrito: tarifa x multiplicador de nivel x horas (minimo 1)."""
        self._check_common(duration, discount)
        self.validate_service()

        billable_hours = max(duration, self.MIN_BILLABLE_HOURS)
        total = self.base_price * self.LEVEL_MULTIPLIER[self.level] * billable_hours
        return self._apply_discount(total, discount)

    def get_summary(self) -> str:
        return (f"{super().get_summary()} | Tipo: Asesoria especializada | "
                f"Nivel: {self.level}")

