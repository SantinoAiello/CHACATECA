import mysql.connector
from mysql.connector import Error
import time
from datetime import datetime
import os

# DATABASE CONNECTION
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Santy.1503',
            database='chacateca'
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
        return connection
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class TurnoUsuario:
    def __init__(self):
        self.turnos = {
            'mañana': 'Usuario_Mañana',
            'tarde': 'Usuario_Tarde',
            'noche': 'Usuario_Noche'
        }

    def seleccionar_turno(self):
        while True:
            turno = input("Seleccione su turno (mañana/tarde/noche) o escriba 'salir' para cancelar: ").lower()

            if turno == "salir":
                print("Proceso cancelado.")
                break

            if turno in self.turnos:
                usuario = self.turnos[turno]
                print(f"Hola, {usuario}")
                
                while True:
                    contraseña = input("Ingrese su contraseña (o escriba 'atras' para seleccionar otro turno): ")

                    if contraseña.lower() == "atras":
                        break

                    if self.verificar_contraseña(usuario, contraseña):
                        print("Acceso concedido.")
                        time.sleep(1.5)  # Esperar 1.5 segundos
                        print(f"Bienvenido, {usuario}.")
                        self.mostrar_menu(usuario)  # Llamar al menú
                        break  # Salir del bucle de contraseña
                    else:
                        print("Contraseña incorrecta. Vuelve a intentarlo.")
            else:
                print("Turno no válido. Inténtelo nuevamente.")

    def verificar_contraseña(self, usuario, contraseña):
        conexion = create_connection()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta = "SELECT * FROM usuarios WHERE nombre = %s AND contrasena = %s"
                cursor.execute(consulta, (usuario, contraseña))
                resultado = cursor.fetchone()
                cursor.close()
                conexion.close()
                return resultado is not None
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return False
        else:
            print("No se pudo establecer la conexión con la base de datos.")
            return False

    def mostrar_menu(self, usuario):
        while True:
            clear_console()  # Limpiar la consola al mostrar el menú
            print("\n--- Menú de Opciones ---")
            print("1. Préstamo Diario")
            print("2. Préstamo Domicilio")
            print("3. Tabla de Préstamos")
            print("4. Configuración")
            print("5. Cerrar Sesión")
            print("6. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.prestamo_diario()
            elif opcion == '2':
                self.prestamo_domicilio()
            elif opcion == '3':
                self.tabla_prestamos()
            elif opcion == '4':
                self.configuraciones(usuario)                
            elif opcion == '5':
                print("Cerrando sesión...")
                return  # Volver a la selección de turno
            elif opcion == '6':
                print("Saliendo del programa...")
                exit()  # Terminar el programa
            else:
                print("Opción no válida. Inténtelo nuevamente.")

    def tabla_prestamos(self):
        while True:
            clear_console()  # Limpiar la consola al mostrar el menú de la tabla de préstamos
            print("\n--- Menú Tabla de Préstamos ---")
            print("1. Préstamos a Domicilio")
            print("2. Préstamos Diarios")
            print("3. Regresar al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.tabla_a_domicilio()
            elif opcion == '2':
                self.tabla_diarios()
            elif opcion == '3':
                print("Regresando al menú principal...")
                break
            else:
                print("Opción no válida. Por favor, elija una opción válida.")

    def tabla_a_domicilio(self):
        while True:
            clear_console()
            print("\n--- Menú Préstamos a Domicilio ---")
            print("1. Ver Préstamos")
            print("2. Buscar Préstamos por DNI")
            print("3. Eliminar Préstamos por DNI")
            print("4. Volver Atrás")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.ver_prestamos_a_domicilio()
            elif opcion == '2':
                self.buscar_prestamos_por_dni()
            elif opcion == '3':
                self.eliminar_prestamos_por_dni()
            elif opcion == '4':
                break
            else:
                print("Opción no válida. Inténtelo nuevamente.")

    def configuraciones(self, usuario):
        while True:
            clear_console()  # Limpiar la consola al mostrar el menú de configuraciones
            print("\n--- Menú de Configuraciones ---")
            print("1. Cambiar Contraseña")
            print("2. Regresar al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.cambiar_contraseña(usuario)
            elif opcion == '2':
                print("Regresando al menú principal...")
                break
            else:
                print("Opción no válida. Por favor, elija una opción del menú.")

    def cambiar_contraseña(self, usuario):
        conexion = create_connection()
        if conexion:
            try:
                cursor = conexion.cursor()
                
                # Solicitar la contraseña actual
                contraseña_actual = input("Ingrese su contraseña actual: ")
                
                # Verificar si la contraseña actual es correcta
                consulta = "SELECT * FROM usuarios WHERE nombre = %s AND contrasena = %s"
                cursor.execute(consulta, (usuario, contraseña_actual))
                resultado = cursor.fetchone()

                if resultado:
                    # Solicitar la nueva contraseña
                    nueva_contraseña = input("Ingrese su nueva contraseña: ")
                    confirmar_contraseña = input("Confirme su nueva contraseña: ")

                    if nueva_contraseña == confirmar_contraseña:
                        # Actualizar la contraseña en la base de datos
                        actualizar = "UPDATE usuarios SET contrasena = %s WHERE nombre = %s"
                        cursor.execute(actualizar, (nueva_contraseña, usuario))
                        conexion.commit()
                        print("Contraseña actualizada con éxito.")
                    else:
                        print("Las contraseñas no coinciden. Inténtelo nuevamente.")
                else:
                    print("La contraseña actual es incorrecta.")
            except mysql.connector.Error as err:
                print(f"Error al actualizar la contraseña: {err}")
            finally:
                cursor.close()
                conexion.close()

    def prestamo_diario(self):
        while True:
            clear_console()  # Limpiar la consola al entrar al menú de préstamo diario
            print("\n--- Menú de Préstamo Diario ---")
            print("1. Préstamo de Libro")
            print("2. Préstamo de Juego")
            print("3. Préstamo de Utilidad")
            print("4. Regresar al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.prestamo_libro()
            elif opcion == '2':
                self.prestamo_juego()
            elif opcion == '3':
                self.prestamo_utilidad()
            elif opcion == '4':
                print("Regresando al menú principal...")
                break  # Salir del menú de préstamo diario
            else:
                print("Opción no válida. Por favor, elija una opción del menú.")

    def prestamo_libro(self):
        clear_console()  # Limpiar la consola al entrar al préstamo de libro
        print("Ejecutando Préstamo de Libro...")

        # Mostrar todos los campos a rellenar
        nombre = input("Ingrese su nombre: ")
        curso = input("Ingrese su curso: ")
        titulo_libro = input("Ingrese el título del libro: ")
        hora_prestamo = datetime.now()  # Hora actual
        
        # Ingreso de hora de devolución
        while True:
            try:
                hora_devolucion_input = input("Ingrese la hora de devolución (formato HH:MM): ")
                hora_devolucion = datetime.strptime(hora_devolucion_input, '%H:%M').time()
                break  # Salir del bucle si la hora es válida
            except ValueError:
                print("Formato de hora inválido. Por favor, use el formato HH:MM.")

        conexion = create_connection()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta = """
                INSERT INTO prestamo_libros (nombre, curso, titulo_libro, hora_prestamo, hora_devolucion)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(consulta, (nombre, curso, titulo_libro, hora_prestamo, hora_devolucion))
                conexion.commit()  # Confirmar la transacción
                print("Préstamo de libro registrado con éxito.")
            except mysql.connector.Error as err:
                print(f"Error al registrar el préstamo de libro: {err}")
            finally:
                cursor.close()
                conexion.close()

    def prestamo_domicilio(self):
        clear_console()
        print("\n--- Menú de Préstamo a Domicilio ---")
        print("1. Clientes")
        print("2. Formulario")
        print("3. Regresar al Menú Principal")
    
        while True:
            opcion = input("Seleccione una opción: ")
    
            if opcion == '1':
                self.menu_clientes()
            elif opcion == '2':
                self.formulario_prestamo_domicilio()
            elif opcion == '3':
                print("Regresando al menú principal...")
                break
            else:
                print("Opción no válida. Por favor, elija una opción del menú.")

    def menu_clientes(self):
        while True:
            clear_console()  # Limpiar la consola al entrar al menú de clientes
            print("\n--- Menú de Clientes ---")
            print("1. Añadir Cliente")
            print("2. Editar Cliente")
            print("3. Buscar Cliente")
            print("4. Regresar al Menú de Préstamo Domicilio")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.ingresar_nuevo_cliente()
            elif opcion == '2':
                self.editar_cliente()
            elif opcion == '3':
                self.buscar_cliente()
            elif opcion == '4':
                print("Regresando al menú de préstamo a domicilio...")
                break
            else:
                print("Opción no válida. Por favor, elija una opción del menú.")

    def ingresar_nuevo_cliente(self):
        clear_console()
        print("Añadir Nuevo Cliente")

        nombre_completo = input("Ingrese el nombre completo: ")
        domicilio = input("Ingrese el domicilio: ")
        localidad = input("Ingrese la localidad: ")

        while True:
            telefono = input("Ingrese el teléfono: ")
            if telefono.isdigit() and len(telefono) >= 7:  # Asegura que el teléfono sea válido
                break
            else:
                print("Teléfono inválido. Debe contener al menos 7 dígitos.")

        while True:
            dni = input("Ingrese el DNI: ")
            if dni.isdigit() and len(dni) == 8:  # Asegura que el DNI sea válido
                break
            else:
                print("DNI inválido. Debe contener 8 dígitos.")

        conexion = create_connection()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta = """
                INSERT INTO clientes (nombre_completo, domicilio, localidad, telefono, dni)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(consulta, (nombre_completo, domicilio, localidad, telefono, dni))
                conexion.commit()
                print("Cliente registrado con éxito.")
            except mysql.connector.Error as err:
                print(f"Error al registrar el cliente: {err}")
            finally:
                cursor.close()
                conexion.close()


    def buscar_cliente(self):
        clear_console()
        print("\n--- Buscar Cliente ---")
        dni_cliente = input("Ingrese el DNI del cliente: ")

        conexion = create_connection()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta = "SELECT * FROM clientes WHERE dni = %s"
                cursor.execute(consulta, (dni_cliente,))
                cliente = cursor.fetchone()

                if cliente:
                    print("\nCliente encontrado:")
                    print(f"Nombre Completo: {cliente[1]}")
                    print(f"Domicilio: {cliente[2]}")
                    print(f"Localidad: {cliente[3]}")
                    print(f"Teléfono: {cliente[4]}")
                    print(f"DNI: {cliente[5]}")
                else:
                    print(f"No se encontró ningún cliente con el DNI: {dni_cliente}")
            except mysql.connector.Error as err:
                print(f"Error al buscar el cliente: {err}")
            finally:
                cursor.close()
                conexion.close()
        
        input("Presione Enter para continuar...")


    def editar_cliente(self):
        clear_console()
        print("\n--- Editar Cliente ---")
        dni_cliente = input("Ingrese el DNI del cliente a editar: ")

        conexion = create_connection()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta = "SELECT * FROM clientes WHERE dni = %s"
                cursor.execute(consulta, (dni_cliente,))
                cliente = cursor.fetchone()

                if cliente:
                    print("Cliente encontrado:")
                    print(f"Nombre Completo: {cliente[1]}")
                    print(f"Domicilio: {cliente[2]}")
                    print(f"Localidad: {cliente[3]}")
                    print(f"Teléfono: {cliente[4]}")
                    print(f"DNI: {cliente[5]}")

                    nuevo_nombre = input("Ingrese el nuevo nombre completo (o presione Enter para no cambiar): ")
                    nuevo_domicilio = input("Ingrese el nuevo domicilio (o presione Enter para no cambiar): ")
                    nueva_localidad = input("Ingrese la nueva localidad (o presione Enter para no cambiar): ")
                    nuevo_telefono = input("Ingrese el nuevo teléfono (o presione Enter para no cambiar): ")

                    consulta_actualizacion = "UPDATE clientes SET "
                    valores_actualizacion = []
                    if nuevo_nombre:
                        consulta_actualizacion += "nombre_completo = %s, "
                        valores_actualizacion.append(nuevo_nombre)
                    if nuevo_domicilio:
                        consulta_actualizacion += "domicilio = %s, "
                        valores_actualizacion.append(nuevo_domicilio)
                    if nueva_localidad:
                        consulta_actualizacion += "localidad = %s, "
                        valores_actualizacion.append(nueva_localidad)
                    if nuevo_telefono:
                        consulta_actualizacion += "telefono = %s, "
                        valores_actualizacion.append(nuevo_telefono)

                    consulta_actualizacion = consulta_actualizacion.rstrip(", ") + " WHERE dni = %s"
                    valores_actualizacion.append(dni_cliente)

                    cursor.execute(consulta_actualizacion, tuple(valores_actualizacion))
                    conexion.commit()
                    print("Cliente actualizado con éxito.")
                else:
                    print(f"No se encontró ningún cliente con el DNI: {dni_cliente}")
            except mysql.connector.Error as err:
                print(f"Error al editar el cliente: {err}")
            finally:
                cursor.close()
                conexion.close()

    def prestamo_utilidad(self):
        clear_console()  # Limpiar la consola al entrar al préstamo de utilidad
        print("Ejecutando Préstamo de Utilidad...")

        # Mostrar todos los campos a rellenar
        nombre = input("Ingrese su nombre: ")
        curso = input("Ingrese su curso: ")
        titulo_utilidad = input("Ingrese el título de la utilidad: ")
        hora_prestamo = datetime.now()  # Hora actual
        
        # Ingreso de hora de devolución
        while True:
            try:
                hora_devolucion_input = input("Ingrese la hora de devolución (formato HH:MM): ")
                hora_devolucion = datetime.strptime(hora_devolucion_input, '%H:%M').time()
                break  # Salir del bucle si la hora es válida
            except ValueError:
                print("Formato de hora inválido. Por favor, use el formato HH:MM.")

        conexion = create_connection()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta = """
                INSERT INTO prestamo_utilidades (nombre, curso, titulo_utilidad, hora_prestamo, hora_devolucion)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(consulta, (nombre, curso, titulo_utilidad, hora_prestamo, hora_devolucion))
                conexion.commit()  # Confirmar la transacción
                print("Préstamo de utilidad registrado con éxito.")
            except mysql.connector.Error as err:
                print(f"Error al registrar el préstamo de utilidad: {err}")
            finally:
                cursor.close()
                conexion.close()

    def formulario_prestamo_domicilio(self):
        clear_console()  # Limpiar la consola al entrar al formulario
        print("\n--- Formulario de Préstamo a Domicilio ---")
    
        dni = input("Ingrese el DNI: ")
        libro = input("Ingrese el título del libro: ")
    
        # Obtener fecha actual automáticamente para "Día solicitado"
        dia_solicitado = datetime.now().date()

        # Solicitar la fecha de devolución
        while True:
            try:
                dia_devolucion_input = input("Ingrese el día de devolución (formato YYYY-MM-DD): ")
                dia_devolucion = datetime.strptime(dia_devolucion_input, '%Y-%m-%d').date()
                break  # Salir del bucle si la fecha es válida
            except ValueError:
                print("Formato de fecha inválido. Por favor, use el formato YYYY-MM-DD.")

    # Conectar a la base de datos y almacenar los datos
        conexion = create_connection()
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta = """
                INSERT INTO prestamos_domicilio (dni, libro, dia_solicitado, dia_devolucion)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(consulta, (dni, libro, dia_solicitado, dia_devolucion))
                conexion.commit()
                print("Préstamo a domicilio registrado con éxito.")
            except mysql.connector.Error as err:
                print(f"Error al registrar el préstamo a domicilio: {err}")
            finally:
                cursor.close()
                conexion.close()

# RUNNING THE PROGRAM
if __name__ == "__main__":
    sistema_turno = TurnoUsuario()
    sistema_turno.seleccionar_turno()
