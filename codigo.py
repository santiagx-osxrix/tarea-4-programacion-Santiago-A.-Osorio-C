"""
Sistema Integral de Gestion de Clientes, Servicios y Reservas - Software FJ
Curso: Programacion 213023 - Fase 4 (Practicas Simuladas)
Estudiante: Santiago Andres Osorio Cuellar
Institucion: Universidad Nacional Abierta y a Distancia - UNAD
Sede: Pitalito, Huila
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime

# Configuracion sencilla del archivo de logs
logging.basicConfig(
    filename="errores_sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# ==========================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================
class ErrorSistemaFJ(Exception):
    """Clase base para errores del sistema Software FJ."""
    pass


class ClienteInvalidoError(ErrorSistemaFJ):
    """Error cuando los datos del cliente son invalidos."""
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Error cuando un servicio tiene parametros invalidos."""
    pass


class ReservaInvalidaError(ErrorSistemaFJ):
    """Error cuando ocurre un fallo al crear o procesar una reserva."""
    pass


# ==========================================
# CLASES ABSTRACTAS Y ENTIDADES BASE
# ==========================================
class EntidadBase(ABC):
    """Clase abstracta general para las entidades del sistema."""

    @abstractmethod
    def obtener_detalles(self):
        pass


class Cliente(EntidadBase):
    """Clase Cliente con encapsulacion (atributos privados) y validaciones."""

    def __init__(self, identificacion, nombre, correo, telefono):
        self.__identificacion = ""
        self.__nombre = ""
        self.__correo = ""
        self.__telefono = ""

        self.set_identificacion(identificacion)
        self.set_nombre(nombre)
        self.set_correo(correo)
        self.set_telefono(telefono)

    def set_identificacion(self, identificacion):
        if not identificacion or not identificacion.strip():
            raise ClienteInvalidoError("La identificacion no puede estar vacia.")
        if not identificacion.isdigit():
            raise ClienteInvalidoError(f"Identificacion invalida '{identificacion}': debe tener solo numeros.")
        self.__identificacion = identificacion.strip()

    def get_identificacion(self):
        return self.__identificacion

    def set_nombre(self, nombre):
        if not nombre or len(nombre.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 letras.")
        self.__nombre = nombre.strip()

    def get_nombre(self):
        return self.__nombre

    def set_correo(self, correo):
        if not correo or "@" not in correo or "." not in correo:
            raise ClienteInvalidoError(f"Correo invalido: '{correo}'.")
        self.__correo = correo.strip()

    def get_correo(self):
        return self.__correo

    def set_telefono(self, telefono):
        if not telefono or not telefono.isdigit() or len(telefono) < 7:
            raise ClienteInvalidoError(f"Telefono invalido: '{telefono}'. Debe tener al menos 7 numeros.")
        self.__telefono = telefono.strip()

    def get_telefono(self):
        return self.__telefono

    def obtener_detalles(self):
        return f"Cliente [ID: {self.__identificacion}, Nombre: {self.__nombre}, Correo: {self.__correo}, Tel: {self.__telefono}]"


class Servicio(EntidadBase, ABC):
    """Clase abstracta Servicio que hereda de EntidadBase."""

    def __init__(self, codigo_servicio, descripcion_base, tarifa_base):
        if not codigo_servicio or not codigo_servicio.strip():
            raise ServicioNoDisponibleError("El codigo del servicio no puede estar vacio.")
        if tarifa_base <= 0:
            raise ServicioNoDisponibleError(f"La tarifa base (${tarifa_base}) debe ser mayor a cero.")

        self._codigo_servicio = codigo_servicio.strip()
        self._descripcion_base = descripcion_base
        self._tarifa_base = tarifa_base

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    @abstractmethod
    def calcular_costo(self, duracion):
        pass

    @abstractmethod
    def obtener_detalles(self):
        pass


# ==========================================
# SERVICIOS ESPECIALIZADOS (HERENCIA Y POLIMORFISMO)
# ==========================================
class ReservaSala(Servicio):
    """Servicio especializado 1: Reserva de salas."""

    def __init__(self, codigo_servicio, capacidad, tarifa_base):
        super().__init__(codigo_servicio, "Reserva de Sala", tarifa_base)
        if capacidad <= 0:
            raise ServicioNoDisponibleError("La capacidad de la sala debe ser mayor a cero.")
        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        if duracion <= 0 or duracion > 12:
            raise ServicioNoDisponibleError("La reserva de sala debe ser entre 1 y 12 horas.")

    # Metodo sobrecargado usando parametros con valores por defecto
    def calcular_costo(self, duracion, descuento_porcentaje=0.0, incluir_impuesto=True):
        self.validar_parametros(duracion)
        if descuento_porcentaje < 0 or descuento_porcentaje > 100:
            raise ServicioNoDisponibleError("El porcentaje de descuento debe estar entre 0 y 100.")

        subtotal = self._tarifa_base * duracion
        subtotal = subtotal - (subtotal * (descuento_porcentaje / 100))

        if incluir_impuesto:
            subtotal = subtotal * 1.19  # IVA del 19%

        return round(subtotal, 2)

    def obtener_detalles(self):
        return f"Servicio [{self._codigo_servicio}]: {self._descripcion_base} (Capacidad: {self.capacidad} personas, Tarifa: ${self._tarifa_base})"


class AlquilerEquipo(Servicio):
    """Servicio especializado 2: Alquiler de equipos."""

    def __init__(self, codigo_servicio, tipo_equipo, tarifa_base):
        super().__init__(codigo_servicio, "Alquiler de Equipo", tarifa_base)
        if not tipo_equipo or not tipo_equipo.strip():
            raise ServicioNoDisponibleError("Debe indicar el tipo de equipo.")
        self.tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ServicioNoDisponibleError("Las horas de alquiler deben ser mayores a cero.")

    # Metodo sobrecargado con parametros opcionales
    def calcular_costo(self, duracion, seguro_adicional=False, tarifa_seguro=15000.0):
        self.validar_parametros(duracion)
        costo = self._tarifa_base * duracion
        if seguro_adicional:
            costo = costo + tarifa_seguro
        return round(costo, 2)

    def obtener_detalles(self):
        return f"Servicio [{self._codigo_servicio}]: {self._descripcion_base} (Equipo: {self.tipo_equipo}, Tarifa: ${self._tarifa_base})"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado 3: Asesoria tecnica."""

    def __init__(self, codigo_servicio, area_especialidad, tarifa_base):
        super().__init__(codigo_servicio, "Asesoria Especializada", tarifa_base)
        if not area_especialidad or not area_especialidad.strip():
            raise ServicioNoDisponibleError("Debe indicar el area de especialidad.")
        self.area_especialidad = area_especialidad.strip()

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ServicioNoDisponibleError("La duracion de la asesoria debe ser mayor a cero.")

    # Metodo sobrecargado con parametro opcional
    def calcular_costo(self, duracion, complejidad_alta=False):
        self.validar_parametros(duracion)
        costo = self._tarifa_base * duracion
        if complejidad_alta:
            costo = costo * 1.35  # 35% adicional por alta complejidad
        return round(costo, 2)

    def obtener_detalles(self):
        return f"Servicio [{self._codigo_servicio}]: {self._descripcion_base} (Area: {self.area_especialidad}, Tarifa: ${self._tarifa_base})"


# ==========================================
# CLASE RESERVA (INTEGRACION Y MANEJO DE ESTADOS)
# ==========================================
class Reserva(EntidadBase):
    """Clase Reserva que integra cliente, servicio, duracion y estado."""

    contador_reservas = 1000

    def __init__(self, cliente, servicio, duracion, descuento=0.0, impuesto=True, seguro=False, complejidad=False):
        Reserva.contador_reservas += 1
        self.id_reserva = f"RES-{Reserva.contador_reservas}"
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Creada"
        self.costo_total = 0.0
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Opciones para calcular el costo segun el servicio
        self.descuento = descuento
        self.impuesto = impuesto
        self.seguro = seguro
        self.complejidad = complejidad

    def confirmar_reserva(self):
        if self.estado == "Creada":
            self.estado = "Confirmada"
            logging.info(f"Reserva {self.id_reserva} confirmada.")
        else:
            raise ReservaInvalidaError(f"No se puede confirmar la reserva {self.id_reserva} en estado {self.estado}.")

    def procesar_reserva(self):
        print(f"\n[Procesando] Reserva {self.id_reserva} para {self.cliente.get_nombre()}...")
        logging.info(f"Iniciando procesamiento de reserva {self.id_reserva}.")

        try:
            self.servicio.validar_parametros(self.duracion)

            if isinstance(self.servicio, ReservaSala):
                self.costo_total = self.servicio.calcular_costo(self.duracion, self.descuento, self.impuesto)
            elif isinstance(self.servicio, AlquilerEquipo):
                self.costo_total = self.servicio.calcular_costo(self.duracion, self.seguro)
            elif isinstance(self.servicio, AsesoriaEspecializada):
                self.costo_total = self.servicio.calcular_costo(self.duracion, self.complejidad)

            self.confirmar_reserva()
            print(f"[Exito] Reserva {self.id_reserva} confirmada. Total a pagar: ${self.costo_total:,.2f}")
            logging.info(f"Reserva {self.id_reserva} confirmada. Total: ${self.costo_total:,.2f}")

        except (ServicioNoDisponibleError, ReservaInvalidaError) as error:
            self.estado = "Fallida"
            print(f"[Error] No se pudo procesar {self.id_reserva}: {error}")
            logging.error(f"Error en reserva {self.id_reserva}: {error}")
            raise ReservaInvalidaError(error)

        finally:
            print(f"[Fin proceso] Estado actual de {self.id_reserva}: {self.estado}")

    def cancelar_reserva(self):
        if self.estado == "Confirmada":
            self.estado = "Cancelada"
            print(f"[Cancelada] La reserva {self.id_reserva} fue cancelada correctamente.")
            logging.info(f"Reserva {self.id_reserva} cancelada.")
        else:
            print(f"[Aviso] No se puede cancelar {self.id_reserva} porque esta en estado: {self.estado}")
            logging.warning(f"Intento fallido de cancelar {self.id_reserva} en estado {self.estado}.")

    def obtener_detalles(self):
        return f"Reserva {self.id_reserva} | Cliente: {self.cliente.get_nombre()} | Estado: {self.estado} | Total: ${self.costo_total:,.2f}"


# ==========================================
# SIMULACION DE 12 OPERACIONES COMPLETAS
# ==========================================
def ejecutar_simulacion():
    print("==================================================")
    print(" INICIO DE SIMULACION DE OPERACIONES - SOFTWARE FJ")
    print(" Estudiante: Santiago Osorio")
    print("==================================================")

    operaciones_exitosas = 0
    operaciones_fallidas = 0

    # Operacion 1: Cliente valido y Reserva de Sala exitosa (con descuento e IVA)
    print("\n--- Operacion 1: Cliente valido y Reserva de Sala ---")
    try:
        c1 = Cliente("1085300123", "Carlos Perez", "carlos.perez@email.com", "3112345678")
        s1 = ReservaSala("SAL-01", 15, 50000.0)
        r1 = Reserva(c1, s1, 3.0, descuento=10.0, impuesto=True)
        r1.procesar_reserva()
        operaciones_exitosas += 1
    except ErrorSistemaFJ as e:
        print(f"[Excepcion Controlada]: {e}")
        operaciones_fallidas += 1

    # Operacion 2: Cliente con identificacion invalida
    print("\n--- Operacion 2: Cliente con identificacion invalida ---")
    try:
        c2 = Cliente("1085ABC", "Ana Gomez", "ana@email.com", "3201234567")
        operaciones_exitosas += 1
    except ClienteInvalidoError as e:
        print(f"[Excepcion Controlada]: {e}")
        logging.warning(f"Operacion 2 rechazada: {e}")
        operaciones_fallidas += 1

    # Operacion 3: Alquiler de equipo con seguro adicional
    print("\n--- Operacion 3: Alquiler de equipo con seguro ---")
    try:
        c3 = Cliente("98765432", "Maria Rodriguez", "maria.rodriguez@email.com", "3159876543")
        s2 = AlquilerEquipo("EQ-05", "Portatil Core i7", 25000.0)
        r3 = Reserva(c3, s2, 5.0, seguro=True)
        r3.procesar_reserva()
        operaciones_exitosas += 1
    except ErrorSistemaFJ as e:
        print(f"[Excepcion Controlada]: {e}")
        operaciones_fallidas += 1

    # Operacion 4: Asesoria especializada con complejidad alta
    print("\n--- Operacion 4: Asesoria especializada con complejidad alta ---")
    try:
        c4 = Cliente("1122334455", "Luis Torres", "luis.torres@email.com", "3184567890")
        s3 = AsesoriaEspecializada("ASE-02", "Arquitectura Cloud Python", 80000.0)
        r4 = Reserva(c4, s3, 2.5, complejidad=True)
        r4.procesar_reserva()
        operaciones_exitosas += 1
    except ErrorSistemaFJ as e:
        print(f"[Excepcion Controlada]: {e}")
        operaciones_fallidas += 1

    # Operacion 5: Creacion INCORRECTA de servicio (tarifa negativa)
    print("\n--- Operacion 5: Creacion incorrecta de servicio (tarifa negativa) ---")
    try:
        s_malo = ReservaSala("SAL-99", 10, -30000.0)
        operaciones_exitosas += 1
    except ServicioNoDisponibleError as e:
        print(f"[Excepcion Controlada]: {e}")
        logging.warning(f"Operacion 5 rechazada: {e}")
        operaciones_fallidas += 1

    # Operacion 6: Creacion INCORRECTA de servicio (capacidad cero)
    print("\n--- Operacion 6: Creacion incorrecta de sala (capacidad cero) ---")
    try:
        s_malo2 = ReservaSala("SAL-98", 0, 40000.0)
        operaciones_exitosas += 1
    except ServicioNoDisponibleError as e:
        print(f"[Excepcion Controlada]: {e}")
        logging.warning(f"Operacion 6 rechazada: {e}")
        operaciones_fallidas += 1

    # Operacion 7: Reserva con duracion negativa (Fallo controlado)
    print("\n--- Operacion 7: Reserva con duracion negativa ---")
    try:
        c5 = Cliente("1020304050", "Sofia Castro", "sofia.castro@email.com", "3101112233")
        s4 = ReservaSala("SAL-02", 10, 40000.0)
        r5 = Reserva(c5, s4, -2.0)
        r5.procesar_reserva()
        operaciones_exitosas += 1
    except ReservaInvalidaError as e:
        print(f"[Excepcion Controlada]: {e}")
        operaciones_fallidas += 1

    # Operacion 8: Cliente con correo electronico invalido
    print("\n--- Operacion 8: Cliente con correo electronico invalido ---")
    try:
        c6 = Cliente("5544332211", "Pedro Infante", "pedro-correo-sin-arroba", "3127778899")
        operaciones_exitosas += 1
    except ClienteInvalidoError as e:
        print(f"[Excepcion Controlada]: {e}")
        logging.warning(f"Operacion 8 rechazada: {e}")
        operaciones_fallidas += 1

    # Operacion 9: Alquiler de equipo sin seguro (demostrando sobrecarga por defecto)
    print("\n--- Operacion 9: Alquiler de equipo sin seguro ---")
    try:
        c7 = Cliente("7788990011", "Lucia Mendez", "lucia.mendez@email.com", "3145556677")
        s5 = AlquilerEquipo("EQ-09", "Proyector Laser 4K", 35000.0)
        r7 = Reserva(c7, s5, 4.0)
        r7.procesar_reserva()
        operaciones_exitosas += 1
    except ErrorSistemaFJ as e:
        print(f"[Excepcion Controlada]: {e}")
        operaciones_fallidas += 1

    # Operacion 10: Asesoria con duracion cero (Error controlado)
    print("\n--- Operacion 10: Asesoria con duracion cero ---")
    try:
        c8 = Cliente("3322114455", "Jorge Eliecer", "jorge.eliecer@email.com", "3178889900")
        s6 = AsesoriaEspecializada("ASE-08", "Ciberseguridad", 90000.0)
        r8 = Reserva(c8, s6, 0.0)
        r8.procesar_reserva()
        operaciones_exitosas += 1
    except ReservaInvalidaError as e:
        print(f"[Excepcion Controlada]: {e}")
        operaciones_fallidas += 1

    # Operacion 11: Cancelacion exitosa de una reserva confirmada
    print("\n--- Operacion 11: Cancelacion de reserva confirmada ---")
    try:
        c9 = Cliente("2233445566", "Andrea Valdes", "andrea.valdes@email.com", "3193334455")
        s7 = ReservaSala("SAL-03", 8, 45000.0)
        r9 = Reserva(c9, s7, 2.0)
        r9.procesar_reserva()
        r9.cancelar_reserva()
        operaciones_exitosas += 1
    except ErrorSistemaFJ as e:
        print(f"[Excepcion Controlada]: {e}")
        operaciones_fallidas += 1

    # Operacion 12: Cliente con telefono invalido
    print("\n--- Operacion 12: Cliente con telefono invalido ---")
    try:
        c10 = Cliente("9988776655", "Gabriel Garcia", "gabriel@email.com", "312ABC5566")
        operaciones_exitosas += 1
    except ClienteInvalidoError as e:
        print(f"[Excepcion Controlada]: {e}")
        logging.warning(f"Operacion 12 rechazada: {e}")
        operaciones_fallidas += 1

    print("\n==================================================")
    print(" RESUMEN DE LA SIMULACION - SOFTWARE FJ")
    print(f" Operaciones Exitosas: {operaciones_exitosas}")
    print(f" Operaciones con Errores Controlados: {operaciones_fallidas}")
    print(" Registros guardados en 'errores_sistema.log'.")
    print("==================================================")


if __name__ == "__main__":
    ejecutar_simulacion()
