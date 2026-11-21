
from client import Client
from services import (
    RoomReservation,
    EquipmentRental,
    SpecializedConsulting
)
from reservations import (
    Reservation,
    ReservationManager,
    ReservationError
)
from system_logger import (
    registrar_operacion,
    registrar_error
)


# ADMINISTRADOR DE RESERVAS
gestor = ReservationManager()


def ejecutar_prueba(numero, descripcion, operacion):
    print(f"\n--- Operación {numero}: {descripcion} ---")

    try:
        resultado = operacion()

    except (ValueError, ReservationError) as error:
        print(f"Error controlado: {error}")
        registrar_error(f"Operación {numero}: {error}")

    except Exception as error:
        print(f"Error inesperado: {error}")
        registrar_error(f"Error inesperado en operación {numero}: {error}")

    else:
        print(resultado)
        registrar_operacion(
            f"Operación {numero} exitosa: {descripcion}"
        )

    finally:
        print("Operación finalizada.")


# CLIENTES
cliente1 = Client("C001", "Ana Torres", "ana@gmail.com", "3001234567")
cliente2 = Client("C002", "Luis Perez", "luis@gmail.com", "3101234567")


# SERVICIOS
sala = RoomReservation("S001", "Sala principal", 100, 20, 12)
equipo = EquipmentRental("S002", "Proyector", 50, 2)
asesoria = SpecializedConsulting("S003", "Asesoria", 80, "senior")


# FUNCIONES DE PRUEBA

def crear_reserva1():
    reserva = Reservation(
        "R001", cliente1, sala, "2026-11-21", 2
    )
    gestor.register_reservation(reserva)
    return reserva.get_summary()


def crear_reserva2():
    reserva = Reservation(
        "R002", cliente2, equipo, "2026-11-22", 3, 0.10
    )
    gestor.register_reservation(reserva)
    return reserva.get_summary()


def crear_reserva3():
    reserva = Reservation(
        "R003", cliente1, asesoria, "2026-11-23", 2
    )
    gestor.register_reservation(reserva)
    return reserva.get_summary()


def cliente_invalido():
    return Reservation(
        "R004", "No es cliente", sala, "2026-11-24", 2
    )


def servicio_invalido():
    return Reservation(
        "R005", cliente1, "No es servicio", "2026-11-24", 2
    )


def servicio_inactivo():
    servicio = RoomReservation(
        "S004", "Sala cerrada", 100, 10, 5, False
    )
    return Reservation(
        "R006", cliente1, servicio, "2026-11-25", 2
    )


def consultar_reserva():
    return gestor.get_reservation("R001").get_summary()


def cancelar_reserva():
    gestor.cancel_reservation("R002")
    return gestor.get_reservation("R002").get_summary()


def cancelar_reserva_nuevamente():
    gestor.cancel_reservation("R002")
    return "Reserva cancelada nuevamente"


def cliente_datos_invalidos():
    return Client("C003", "L", "correo incorrecto", "123")


# DIEZ OPERACIONES INTEGRALES

ejecutar_prueba(1, "Crear reserva de sala", crear_reserva1)
ejecutar_prueba(2, "Crear reserva de equipos", crear_reserva2)
ejecutar_prueba(3, "Crear reserva de asesoria", crear_reserva3)
ejecutar_prueba(4, "Intentar reservar con cliente invalido", cliente_invalido)
ejecutar_prueba(5, "Intentar reservar con servicio invalido", servicio_invalido)
ejecutar_prueba(6, "Intentar reservar servicio inactivo", servicio_inactivo)
ejecutar_prueba(7, "Consultar una reserva", consultar_reserva)
ejecutar_prueba(8, "Cancelar una reserva", cancelar_reserva)
ejecutar_prueba(9, "Intentar cancelar una reserva dos veces", cancelar_reserva_nuevamente)
ejecutar_prueba(10, "Crear cliente con datos invalidos", cliente_datos_invalidos)


print("\nProceso de pruebas finalizado.")
print("Consulte el archivo software_fj.log para revisar los registros.")
