import re
from base_classes import entity


class Client(entity):
    """Representa un cliente de Software FJ."""

    def __init__(self, client_id, name, email, phone):
        """Inicializa los datos del cliente."""

        super().__init__(client_id)
        
         # Identificador y datos encapsulados
        self._entity_id = self._validate_id(client_id)
        self.__name = self._validate_name(name)
        self.__email = self._validate_email(email)
        self.__phone = self._validate_phone(phone)

    # ---------- VALIDACIONES ----------

    @staticmethod
    def _validate_id(client_id):
        if not isinstance(client_id, str) or not client_id.strip():
            raise ValueError("El ID del cliente es obligatorio.")
        return client_id.strip()
    
    @staticmethod
    def _validate_name(name):
        if not isinstance(name, str) or len(name.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")

        if not all(
            character.isalpha() or character in (" ", "-", "'")
            for character in name.strip()
        ):
            raise ValueError("El nombre contiene caracteres no válidos.")

        return name.strip()
    
    @staticmethod
    def _validate_email(email):
        if not isinstance(email, str):
            raise ValueError("El correo debe ingresarse como texto.")

        pattern = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        if not re.fullmatch(pattern, email.strip()):
            raise ValueError("El correo electrónico no es válido.")

        return email.strip().lower()
    
    @staticmethod
    def _validate_phone(phone):
        if not isinstance(phone, str):
            raise ValueError("El teléfono debe ingresarse como texto.")

        phone = phone.strip()

        if not re.fullmatch(r"\+?[\d\s-]+", phone):
            raise ValueError("El teléfono contiene caracteres no válidos.")

        digits = re.sub(r"\D", "", phone)
        
        if not 7 <= len(digits) <= 15:
            raise ValueError("El teléfono debe tener entre 7 y 15 dígitos.")

        return phone

    # ---------- PROPIEDADES ENCAPSULADAS ----------

    @property
    def client_id(self):
        return self._entity_id
    
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = self._validate_name(value)

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, value):
        self.__email = self._validate_email(value)

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = self._validate_phone(value)

    # ---------- RESUMEN DEL CLIENTE ----------
    
    def get_summary(self):
        return (
            f"Cliente: {self.name} | "
            f"ID: {self.client_id} | "
            f"Correo: {self.email} | "
            f"Teléfono: {self.phone}"
        )
