# consultas.py

from conexion import conectar
import mysql.connector

# --------------------------------------------------
# Usuarios predeterminados y login
# --------------------------------------------------
def agregar_usuarios_predeterminados():
    """
    Inserta un conjunto de usuarios predeterminados si no existen ya.
    """
    usuarios = [
        ("admin",    "Perez",   "Lopez",  "admin@example.com",    "admin123",    "Administrador"),
        ("mecanico1","Gomez",   "Ramirez","mecanico1@example.com","meca123",     "Mecanico"),
        ("recepcion","Sanchez", "Diaz",   "recepcion@example.com", "recep123",    "Recepcionista"),
        ("Edson",    "Talamantes","Chavez","edsontchflo@gmail.com","edson9911",   "Administrador")
    ]
    cnx = conectar()
    cursor = cnx.cursor()
    for usuario in usuarios:
        cursor.execute("SELECT * FROM Usuarios WHERE nombre = %s", (usuario[0],))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO Usuarios (nombre, ap_paterno, ap_materno, email, contraseña, rol) VALUES (%s, %s, %s, %s, %s, %s)",
                usuario
            )
    cnx.commit()
    cursor.close()
    cnx.close()

def verificar_credenciales(nombre, password):
    """
    Retorna la tupla (id_usuario, nombre, ap_paterno, ap_materno, email, rol)
    si existe un usuario con (nombre, contraseña), o None en caso contrario.
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "SELECT id_usuario, nombre, ap_paterno, ap_materno, email, rol "
        "FROM Usuarios WHERE nombre = %s AND contraseña = %s",
        (nombre, password)
    )
    usuario = cursor.fetchone()
    cursor.close()
    cnx.close()
    return usuario


# --------------------------------------------------
# Listados generales para "Mostrar Todos los Datos"
# --------------------------------------------------
def obtener_filas(query):
    """
    Ejecuta un SELECT dinámico y devuelve (columnas, filas).
    - `query` debe ser una cadena SQL completa (sin parámetros).
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(query)
    columnas = [desc[0] for desc in cursor.description]
    filas = cursor.fetchall()
    cursor.close()
    cnx.close()
    return columnas, filas

def eliminar_registro(tabla, columna_id, valor_id):
    """
    Elimina un registro de `tabla` donde `columna_id` = valor_id.
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(f"DELETE FROM {tabla} WHERE {columna_id} = %s", (valor_id,))
    cnx.commit()
    cursor.close()
    cnx.close()


# --------------------------------------------------
# CRUD para Proveedores
# --------------------------------------------------
def registrar_proveedor(nombre, contacto, telefono, direccion):
    """
    Inserta un nuevo proveedor en la tabla Proveedores.
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Proveedores (nombre, contacto, telefono, direccion) VALUES (%s, %s, %s, %s)",
        (nombre, contacto, telefono, direccion)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


# --------------------------------------------------
# Órdenes de trabajo asignadas para mecánico
# --------------------------------------------------
def obtener_ordenes_mecanico_por_nombre(nombre_mecanico):
    """
    Retorna una lista de tuplas (id_orden, estado, fecha_inicio, fecha_fin)
    para las órdenes asignadas al mecánico `nombre_mecanico`.
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "SELECT ot.id_orden, ot.estado, ot.fecha_inicio, ot.fecha_fin "
        "FROM Ordenes_Trabajo ot "
        "JOIN Ordenes_Empleados oe ON ot.id_orden = oe.id_orden "
        "JOIN Usuarios u ON oe.id_usuario = u.id_usuario "
        "WHERE u.nombre = %s",
        (nombre_mecanico,)
    )
    filas = cursor.fetchall()
    cursor.close()
    cnx.close()
    return filas


# --------------------------------------------------
# CRUD para Usuarios (Registro)
# --------------------------------------------------
def registrar_usuario(nombre, ap_paterno, ap_materno, email, contraseña, rol, telefono, fecha_contratacion, salario):
    """
    Inserta un nuevo usuario en la tabla Usuarios.
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Usuarios (nombre, ap_paterno, ap_materno, email, contraseña, rol, telefono, fecha_contratacion, salario) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (nombre, ap_paterno, ap_materno, email, contraseña, rol, telefono, fecha_contratacion, salario)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


# --------------------------------------------------
# CRUD para Clientes
# --------------------------------------------------
def registrar_cliente(nombre, ap_paterno, ap_materno, direccion, telefono, email):
    """
    Inserta un nuevo cliente en la tabla Clientes.
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Clientes (nombre, ap_paterno, ap_materno, direccion, telefono, email) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (nombre, ap_paterno, ap_materno, direccion, telefono, email)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


# --------------------------------------------------
# CRUD para Vehículos
# --------------------------------------------------
def registrar_vehiculo(id_cliente, marca, modelo, año, color, placas):
    """
    Inserta un nuevo vehículo en la tabla Vehiculos.
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Vehiculos (id_cliente, marca, modelo, año, color, placas) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (id_cliente, marca, modelo, año, color, placas)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


# --------------------------------------------------
# CRUD para Inventario (Productos)
# --------------------------------------------------
def registrar_producto_inventario(nombre, descripcion, cantidad, precio):
    """
    Inserta un nuevo producto en la tabla Inventario.
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Inventario (nombre, descripcion, cantidad, precio) "
        "VALUES (%s, %s, %s, %s)",
        (nombre, descripcion, cantidad, precio)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


# --------------------------------------------------
# CRUD para Citas
# --------------------------------------------------
def registrar_cita(id_vehiculo, fecha, hora, estado, observaciones):
    """
    Inserta una nueva cita en la tabla Citas.
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Citas (id_vehiculo, fecha, hora, estado, observaciones) "
        "VALUES (%s, %s, %s, %s, %s)",
        (id_vehiculo, fecha, hora, estado, observaciones)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


# --------------------------------------------------
# CRUD para Servicios
# --------------------------------------------------
def registrar_servicio(nombre, descripcion, costo, duracion):
    """
    Inserta un nuevo servicio en la tabla Servicios.
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Servicios (nombre, descripcion, costo, duracion) "
        "VALUES (%s, %s, %s, %s)",
        (nombre, descripcion, costo, duracion)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


# --------------------------------------------------
# CRUD para Vehículos de Empresa
# --------------------------------------------------
def registrar_vehiculo_empresa(tipo, marca, modelo, placas, estado):
    """
    Inserta un nuevo vehículo de empresa en la tabla Vehiculos_Empresa.
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Vehiculos_Empresa (tipo, marca, modelo, placas, estado) "
        "VALUES (%s, %s, %s, %s, %s)",
        (tipo, marca, modelo, placas, estado)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


# --------------------------------------------------
# CRUD para Órdenes de Trabajo y Asignación
# --------------------------------------------------
def registrar_orden_empleado(id_orden, id_usuario):
    """
    Inserta un registro en Ordenes_Empleados (asigna orden a empleado).
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Ordenes_Empleados (id_orden, id_usuario) VALUES (%s, %s)",
        (id_orden, id_usuario)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


# --------------------------------------------------
# Ver agenda del día (fechas de hoy)
# --------------------------------------------------
def obtener_agenda_del_dia():
    """
    Retorna una lista de tuplas (id_cita, placas, fecha, hora, estado)
    para todas las citas cuya fecha = CURDATE().
    """
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "SELECT c.id_cita, v.placas, c.fecha, c.hora, c.estado "
        "FROM Citas c "
        "JOIN Vehiculos v ON c.id_vehiculo = v.id_vehiculo "
        "WHERE c.fecha = CURDATE()"
    )
    filas = cursor.fetchall()
    cursor.close()
    cnx.close()
    return filas
