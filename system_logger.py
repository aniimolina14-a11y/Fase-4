import logging

# Configuración del registro del sistema
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("SoftwareFJ")


def registrar_operacion(mensaje):
    logger.info(mensaje)


def registrar_error(mensaje):
    logger.error(mensaje)


def registrar_advertencia(mensaje):
    logger.warning(mensaje)