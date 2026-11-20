from datetime import datetime
from base_classes import entity
from client import Client
from services import ManagedService


class ReservationError(Exception):
    pass


class InvalidReservationDataError(ReservationError):
    pass


class ServiceUnavailableError(ReservationError):
    pass


class DuplicateReservationError(ReservationError):
    pass


class Reservation(entity):
    def __init__(
        self,
        reservation_id: str,
        client: Client,
        service: ManagedService,
        scheduled_date: str,
        duration: float,
        discount: float = 0.0,
    ):
        if not isinstance(reservation_id, str) or not reservation_id.strip():
            raise InvalidReservationDataError("El ID de la reserva es obligatorio.")
        if not isinstance(client, Client):
            raise InvalidReservationDataError("Debe asociar un cliente válido.")
        if not isinstance(service, ManagedService):
            raise InvalidReservationDataError("Debe asociar un servicio válido.")
        if not service.is_active:
            raise ServiceUnavailableError(f"El servicio '{service.name}' no está disponible.")

        service.validate_service()

        super().__init__(reservation_id.strip())
        self._entity_id = reservation_id.strip()
        self.client = client
        self.service = service
        self.scheduled_date = scheduled_date
        self.duration = duration
        self.discount = discount
        self._status = "CONFIRMADA"

    @property
    def reservation_id(self) -> str:
        return self._entity_id

    @property
    def scheduled_date(self) -> str:
        return self._scheduled_date

    @scheduled_date.setter
    def scheduled_date(self, value: str):
        try:
            datetime.strptime(value.strip(), "%Y-%m-%d")
        except (ValueError, AttributeError):
            raise InvalidReservationDataError(
                f"Fecha '{value}' inválida. Use formato YYYY-MM-DD."
            )
        self._scheduled_date = value.strip()

    @property
    def duration(self) -> float:
        return self._duration

    @duration.setter
    def duration(self, value: float):
        if not isinstance(value, (int, float)) or value <= 0:
            raise InvalidReservationDataError("La duración debe ser mayor a 0.")
        self._duration = float(value)

    @property
    def discount(self) -> float:
        return self._discount

    @discount.setter
    def discount(self, value: float):
        if not isinstance(value, (int, float)) or not (0.0 <= value <= 1.0):
            raise InvalidReservationDataError("El descuento debe estar entre 0.0 y 1.0.")
        self._discount = float(value)

    @property
    def status(self) -> str:
        return self._status

    def calculate_total(self) -> float:
        if self._status == "CANCELADA":
            return 0.0
        return self.service.calculate_price(self._duration, self._discount)

    def cancel(self):
        if self._status == "CANCELADA":
            raise ReservationError(f"La reserva '{self.reservation_id}' ya está cancelada.")
        self._status = "CANCELADA"

    def get_summary(self) -> str:
        total = self.calculate_total()
        return (
            f"Reserva [{self.reservation_id}] | Estado: {self._status} | Fecha: {self._scheduled_date}\n"
            f"  -> Cliente: {self.client.name} (ID: {self.client.client_id})\n"
            f"  -> Servicio: {self.service.name} | Duración: {self._duration} | Total: ${total:,.2f}"
        )


class ReservationManager:
    def __init__(self):
        self._reservations: dict[str, Reservation] = {}

    def register_reservation(self, reservation: Reservation):
        if not isinstance(reservation, Reservation):
            raise InvalidReservationDataError("Solo se pueden registrar objetos Reservation.")
        if reservation.reservation_id in self._reservations:
            raise DuplicateReservationError(f"Ya existe la reserva '{reservation.reservation_id}'.")
        self._reservations[reservation.reservation_id] = reservation

    def get_reservation(self, reservation_id: str) -> Reservation:
        if reservation_id not in self._reservations:
            raise ReservationError(f"No existe la reserva '{reservation_id}'.")
        return self._reservations[reservation_id]

    def cancel_reservation(self, reservation_id: str):
        reserva = self.get_reservation(reservation_id)
        reserva.cancel()