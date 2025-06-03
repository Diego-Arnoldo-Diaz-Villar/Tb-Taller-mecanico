
from conexion import conectar
from datetime import datetime



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
    """Retorna la tupla """
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

def obtener_filas(query):
    """Ejecuta un SELECT dinámico y devuelve (columnas, filas)."""
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(query)
    columnas = [desc[0] for desc in cursor.description]
    filas = cursor.fetchall()
    cursor.close()
    cnx.close()
    return columnas, filas

def eliminar_registro(tabla, columna_id, valor_id):
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(f"DELETE FROM {tabla} WHERE {columna_id} = %s", (valor_id,))
    cnx.commit()
    cursor.close()
    cnx.close()



def registrar_proveedor(nombre, contacto, telefono, direccion):

    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Proveedores (nombre, contacto, telefono, direccion) VALUES (%s, %s, %s, %s)",
        (nombre, contacto, telefono, direccion)
    )
    cnx.commit()
    cursor.close()
    cnx.close()



def obtener_ordenes_mecanico_por_nombre(nombre):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            ot.id_orden,
            ot.id_cliente,
            ot.id_vehiculo,
            s.nombre AS servicio_nombre,
            ot.descripcion,
            ot.estado,
            ot.fecha_registro,
            ot.fecha_fin
        FROM Ordenes_Trabajo ot
        JOIN Servicios s ON ot.id_servicio = s.id_servicio
        JOIN Ordenes_Empleados oe ON ot.id_orden = oe.id_orden
        JOIN Usuarios u ON oe.id_usuario = u.id_usuario
        WHERE u.nombre = %s
    """, (nombre,))
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return filas  # devuelve lista de dicts



def registrar_usuario(nombre, ap_paterno, ap_materno, email, contraseña, rol, telefono, fecha_contratacion, salario):
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



def registrar_cliente(nombre, ap_paterno, ap_materno, direccion, telefono, email):
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



def registrar_vehiculo(id_cliente, marca, modelo, anio, color, placas):
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Vehiculos "
        "(id_cliente, marca, modelo, anio, color, placas) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (id_cliente, marca, modelo, anio, color, placas)
    )
    cnx.commit()
    cursor.close()
    cnx.close()



def registrar_producto_inventario(nombre, descripcion, cantidad, precio):
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



def registrar_cita(id_vehiculo, fecha, hora, estado, observaciones):
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


def registrar_servicio(nombre, descripcion, costo, duracion):
    cnx    = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Servicios (nombre, descripcion, costo, duracion) VALUES (%s, %s, %s, %s)",
        (nombre, descripcion, costo, duracion)
    )
    cnx.commit()
    cursor.close()
    cnx.close()


def registrar_vehiculo_empresa(tipo, marca, modelo, placas, estado):
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
def registrar_orden_trabajo(id_cliente, id_vehiculo, id_servicio, descripcion, fecha_registro, estado="Pendiente"):
    """Inserta una orden de trabajo vinculando un cliente, vehículo y un único servicio. Devuelve el id_orden generado."""
    cnx    = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        """
        INSERT INTO Ordenes_Trabajo
          (id_cliente, id_vehiculo, id_servicio, descripcion, estado, fecha_registro)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (id_cliente, id_vehiculo, id_servicio, descripcion, estado, fecha_registro)
    )
    cnx.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    cnx.close()
    return nuevo_id


def registrar_orden_empleado(id_orden, id_usuario):
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Ordenes_Empleados (id_orden, id_usuario) VALUES (%s, %s)",
        (id_orden, id_usuario)
    )
    cnx.commit()
    cursor.close()
    cnx.close()



def obtener_agenda_del_dia():
    """Retorna una lista de tuplas (id_cita, placas, fecha, hora, estado) para todas las citas cuya fecha = CURDATE()."""
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


def obtener_clientes():
    """Devuelve una lista de diccionarios con los clientes existentes, """
    cnx = conectar()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(
        "SELECT id_cliente, nombre, ap_paterno, ap_materno "
        "FROM Clientes"
    )
    resultados = cursor.fetchall()
    cursor.close()
    cnx.close()
    return resultados

def obtener_vehiculos_modelo():
    """Devuelve una lista de diccionarios con los vehículos existentes, cada uno con sus campos:"""
    cnx = conectar()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(
        "SELECT id_vehiculo, modelo FROM Vehiculos"
    )
    resultados = cursor.fetchall()
    cursor.close()
    cnx.close()
    return resultados

def obtener_servicios():
    """Devuelve lista de diccionarios con todos los servicios"""
    cnx    = conectar()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT id_servicio, nombre, descripcion, costo, duracion FROM Servicios")
    resultados = cursor.fetchall()
    cursor.close()
    cnx.close()
    return resultados

def obtener_ordenes_con_servicio_y_mecanicos():
    """Devuelve lista de tuplas  para todas las órdenes. (Usa JOIN y subconsulta con GROUP_CONCAT)."""
    cnx    = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        """
        SELECT 
          o.id_orden,
          o.id_cliente,
          o.id_vehiculo,
          s.nombre AS servicio_nombre,
          o.descripcion,
          o.estado,
          o.fecha_registro,
          o.fecha_fin,
          IFNULL(
            (
              SELECT GROUP_CONCAT(CONCAT(u.nombre,' ',u.ap_paterno) SEPARATOR ', ')
              FROM Ordenes_Empleados oe
              JOIN Usuarios u ON oe.id_usuario = u.id_usuario
              WHERE oe.id_orden = o.id_orden
            ),
            'Sin mecánicos'
          ) AS empleados_asignados
        FROM Ordenes_Trabajo o
        JOIN Servicios s ON o.id_servicio = s.id_servicio
        """
    )
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    cursor.close()
    cnx.close()
    return columnas, filas

def obtener_mecanicos():
    """Devuelve lista de diccionarios con:de todos los usuarios cuyo rol = 'Mecanico'."""
    cnx    = conectar()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(
        "SELECT id_usuario, nombre, ap_paterno, ap_materno FROM Usuarios WHERE rol = 'Mecanico'"
    )
    resultados = cursor.fetchall()
    cursor.close()
    cnx.close()
    return resultados
def asignar_empleado_a_orden(id_orden, id_usuario):
    cnx    = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO Ordenes_Empleados (id_orden, id_usuario) VALUES (%s, %s)",
        (id_orden, id_usuario)
    )
    cnx.commit()
    cursor.close()
    cnx.close()

def obtener_empleados_de_orden(id_orden):
    """Retorna lista de diccionariosde los empleados asignados a una orden específica."""
    cnx    = conectar()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT u.id_usuario, u.nombre, u.ap_paterno, u.ap_materno
        FROM Usuarios u
        JOIN Ordenes_Empleados oe ON u.id_usuario = oe.id_usuario
        WHERE oe.id_orden = %s
        """,
        (id_orden,)
    )
    resultados = cursor.fetchall()
    cursor.close()
    cnx.close()
    return resultados

def quitar_empleado_de_orden(id_orden, id_usuario):
    cnx    = conectar()
    cursor = cnx.cursor()
    cursor.execute(
        "DELETE FROM Ordenes_Empleados WHERE id_orden = %s AND id_usuario = %s",
        (id_orden, id_usuario)
    )
    cnx.commit()
    cursor.close()
    cnx.close()

def actualizar_estado_orden(id_orden, nuevo_estado):
    conexion = conectar()
    cursor = conexion.cursor()

    if nuevo_estado == "Completada":
        fecha_fin = datetime.today().strftime('%Y-%m-%d')
        cursor.execute("""
            UPDATE Ordenes_Trabajo
            SET estado = %s, fecha_fin = %s
            WHERE id_orden = %s
        """, (nuevo_estado, fecha_fin, id_orden))
    else:
        cursor.execute("""
            UPDATE Ordenes_Trabajo
            SET estado = %s
            WHERE id_orden = %s
        """, (nuevo_estado, id_orden))

    conexion.commit()
    cursor.close()
    conexion.close()
