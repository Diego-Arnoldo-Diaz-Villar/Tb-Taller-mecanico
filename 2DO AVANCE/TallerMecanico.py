import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk


def conectar():
    #De preferencia mover esto a un archivo json o cualquier otro
    #No conectarse con root crear usuario y solo tener permisos para el uso de la bd (se refiere a la bd directamente)
    #TODA LA INTERACCION DE BD TIENE QUE ESTAR EN UN SCRIPT APARTE
    #Tratar de validar erorres de conexiones a bd
    #Hacer las transacciones atomicas o tener atomicidad y las conexiones
    #validar conexion en cada consulta de la bd
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="edson9911",
        database="TallerMecanico"
    )

def agregar_usuarios_predeterminados():
    #SACAR DATOS DEL CODIGO
    usuarios = [
        ("admin", "Perez", "Lopez", "admin@example.com", "admin123", "Administrador"),
        ("mecanico1", "Gomez", "Ramirez", "mecanico1@example.com", "meca123", "Mecanico"),
        ("recepcion", "Sanchez", "Diaz", "recepcion@example.com", "recep123", "Recepcionista"),
        ("Edson", "Talamantes", "Chavez", "edsontchflo@gmail.com", "edson9911", "Administrador")
    ]
    conexion = conectar()
    cursor = conexion.cursor()
    for usuario in usuarios:
        cursor.execute("SELECT * FROM Usuarios WHERE nombre = %s", (usuario[0],))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO Usuarios (nombre, ap_paterno, ap_materno, email, contraseña, rol) VALUES (%s, %s, %s, %s, %s, %s)", usuario)
    conexion.commit()
    conexion.close()


def verificar_credenciales(nombre, password):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuario, nombre, ap_paterno, ap_materno, email, rol FROM Usuarios WHERE nombre = %s AND contraseña = %s", (nombre, password))
    usuario = cursor.fetchone()
    conexion.close()
    return usuario

def mostrar_todos_los_datos():
    ventana = tk.Toplevel()
    ventana.title("Datos Completos del Sistema")
    ventana.geometry("900x600")
    ventana.minsize(700, 400)

    notebook = ttk.Notebook(ventana)
    notebook.pack(expand=True, fill="both")

    tablas = {
        "Usuarios": ("SELECT * FROM Usuarios", "Usuarios", "id_usuario"),
        "Clientes": ("SELECT * FROM Clientes", "Clientes", "id_cliente"),
        "Vehículos": ("SELECT * FROM Vehiculos", "Vehiculos", "id_vehiculo"),
        "Servicios": ("SELECT * FROM Servicios", "Servicios", "id_servicio"),
        "Citas": ("SELECT * FROM Citas", "Citas", "id_cita"),
        "Órdenes de Trabajo": ("SELECT * FROM Ordenes_Trabajo", "Ordenes_Trabajo", "id_orden"),
        "Inventario": ("SELECT * FROM Inventario", "Inventario", "id_producto"),
        "Proveedores": ("SELECT * FROM Proveedores", "Proveedores", "id_proveedor"),
        "Vehículos Empresa": ("SELECT * FROM Vehiculos_Empresa", "Vehiculos_Empresa", "id_vehiculo_empresa"),
        "Órdenes Empleados": ("SELECT * FROM Ordenes_Empleados", "Ordenes_Empleados", "id_orden")
    }

    conexion = conectar()
    cursor = conexion.cursor()

    for nombre_tabla, (query, nombre_sql, id_columna) in tablas.items():
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=nombre_tabla)

        tree = ttk.Treeview(frame)
        tree.pack(expand=True, fill="both")

        # Cargar datos
        cursor.execute(query)
        columnas = [desc[0] for desc in cursor.description]
        tree["columns"] = columnas
        tree["show"] = "headings"

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

        def eliminar_registro(treeview=tree, tabla=nombre_sql, col_id=id_columna):
            selected_item = treeview.selection()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecciona un registro para eliminar.")
                return
            item = treeview.item(selected_item[0])
            record_id = item["values"][0]

            confirm = messagebox.askyesno("Confirmar", f"¿Eliminar registro {record_id} de {tabla}?")
            if confirm:
                try:
                    con = conectar()
                    cur = con.cursor()
                    cur.execute(f"DELETE FROM {tabla} WHERE {col_id} = %s", (record_id,))
                    con.commit()
                    treeview.delete(selected_item[0])
                    messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"No se pudo eliminar: {e}")
                finally:
                    con.close()

        ttk.Button(frame, text="Eliminar Seleccionado", command=eliminar_registro).pack(pady=10)

    conexion.close()


def registrar_proveedor():
    ventana = tk.Toplevel()
    ventana.title("Registrar Proveedor")
    ventana.geometry("400x400")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    campos = [
        ("Nombre del Proveedor", "nombre"),
        ("Nombre del Contacto", "contacto"),
        ("Teléfono", "telefono"),
        ("Dirección", "direccion")
    ]
    entradas = {}

    for i, (label, key) in enumerate(campos):
        ttk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=5)
        entry = ttk.Entry(frame, width=30)
        entry.grid(row=i, column=1, pady=5)
        entradas[key] = entry

    def guardar():
        datos = {k: e.get().strip() for k, e in entradas.items()}
        if not datos["nombre"]:
            messagebox.showerror("Error", "El nombre del proveedor es obligatorio.")
            return

        conexion = conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO Proveedores (nombre, contacto, telefono, direccion)
                VALUES (%s, %s, %s, %s)
            """, (datos["nombre"], datos["contacto"], datos["telefono"], datos["direccion"]))
            conexion.commit()
            messagebox.showinfo("Éxito", "Proveedor registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
        finally:
            conexion.close()

    ttk.Button(frame, text="Registrar Proveedor", command=guardar).grid(row=len(campos)+1, column=0, columnspan=2, pady=20)




def ver_ordenes_mecanico(usuario):
    ventana = tk.Toplevel()
    ventana.title("Órdenes de Trabajo Asignadas")
    ventana.geometry("800x500")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=10)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("ID Orden", "Estado", "Fecha Inicio", "Fecha Fin"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True)

    def cargar_ordenes():
        for row in tree.get_children():
            tree.delete(row)
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT ot.id_orden, ot.estado, ot.fecha_inicio, ot.fecha_fin
            FROM Ordenes_Trabajo ot
            JOIN Ordenes_Empleados oe ON ot.id_orden = oe.id_orden
            JOIN Empleados e ON oe.id_empleado = e.id_empleado
            WHERE e.nombre = %s
        """, (usuario[1],))
        for fila in cursor.fetchall():
            tree.insert("", "end", values=fila)
        conexion.close()

    cargar_ordenes()

def registrar_usuario():
    ventana = tk.Toplevel()
    ventana.title("Registrar Usuario")
    ventana.geometry("450x500")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    campos = [
        ("Nombre", "nombre"),
        ("Apellido Paterno", "ap_paterno"),
        ("Apellido Materno", "ap_materno"),
        ("Correo Electrónico", "email"),
        ("Contraseña", "contraseña"),
        ("Rol", "rol"),
        ("Teléfono", "telefono"),
        ("Fecha de Contratación (YYYY-MM-DD)", "fecha_contratacion"),
        ("Salario", "salario")
    ]

    entradas = {}
    for i, (label, key) in enumerate(campos):
        ttk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=5)
        entry = ttk.Entry(frame, width=30, show="*" if key == "contraseña" else "")
        entry.grid(row=i, column=1, pady=5)
        entradas[key] = entry

    def guardar():
        datos = {k: e.get().strip() for k, e in entradas.items()}
        if not all([datos["nombre"], datos["ap_paterno"], datos["email"], datos["contraseña"], datos["rol"], datos["fecha_contratacion"], datos["salario"]]):
            messagebox.showerror("Error", "Por favor completa todos los campos obligatorios.")
            return
        try:
            salario = float(datos["salario"])
        except ValueError:
            messagebox.showerror("Error", "El salario debe ser un número.")
            return

        conexion = conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO Usuarios (nombre, ap_paterno, ap_materno, email, contraseña, rol, telefono, fecha_contratacion, salario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                datos["nombre"], datos["ap_paterno"], datos["ap_materno"],
                datos["email"], datos["contraseña"], datos["rol"],
                datos["telefono"], datos["fecha_contratacion"], salario
            ))
            conexion.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
        finally:
            conexion.close()

    ttk.Button(frame, text="Registrar Usuario", command=guardar).grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

def registrar_cliente():
    ventana = tk.Toplevel()
    ventana.title("Registrar Cliente")
    ventana.geometry("400x400")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    campos = [
        ("Nombre", "nombre"),
        ("Apellido Paterno", "ap_paterno"),
        ("Apellido Materno", "ap_materno"),
        ("Dirección", "direccion"),
        ("Teléfono", "telefono"),
        ("Correo Electrónico", "email")
    ]
    entradas = {}

    for i, (label, key) in enumerate(campos):
        ttk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=5)
        entry = ttk.Entry(frame, width=30)
        entry.grid(row=i, column=1, pady=5)
        entradas[key] = entry

    def guardar():
        datos = {k: e.get() for k, e in entradas.items()}
        if not all([datos["nombre"], datos["ap_paterno"], datos["telefono"]]):
            messagebox.showerror("Error", "Nombre, Apellido Paterno y Teléfono son obligatorios.")
            return
        conexion = conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO Clientes (nombre, ap_paterno, ap_materno, direccion, telefono, email) VALUES (%s, %s, %s, %s, %s, %s)",
                           (datos["nombre"], datos["ap_paterno"], datos["ap_materno"], datos["direccion"], datos["telefono"], datos["email"]))
            conexion.commit()
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
        finally:
            conexion.close()

    ttk.Button(frame, text="Registrar Cliente", command=guardar).grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

def registrar_empleado():
    ventana = tk.Toplevel()
    ventana.title("Registrar Empleado")
    ventana.geometry("450x450")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    campos = [
        ("Nombre", "nombre"),
        ("Apellido Paterno", "ap_paterno"),
        ("Apellido Materno", "ap_materno"),
        ("Cargo", "cargo"),
        ("Teléfono", "telefono"),
        ("Correo Electrónico", "email"),
        ("Fecha de Contratación (YYYY-MM-DD)", "fecha_contratacion"),
        ("Salario", "salario")
    ]
    entradas = {}

    for i, (label, key) in enumerate(campos):
        ttk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=5)
        entry = ttk.Entry(frame, width=30)
        entry.grid(row=i, column=1, pady=5)
        entradas[key] = entry

    def guardar():
        datos = {k: e.get() for k, e in entradas.items()}
        if not all([datos["nombre"], datos["ap_paterno"], datos["cargo"], datos["fecha_contratacion"], datos["salario"]]):
            messagebox.showerror("Error", "Por favor completa todos los campos obligatorios.")
            return
        try:
            salario_float = float(datos["salario"])
        except ValueError:
            messagebox.showerror("Error", "El salario debe ser un número.")
            return

        conexion = conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO Empleados (nombre, ap_paterno, ap_materno, cargo, telefono, email, fecha_contratacion, salario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (datos["nombre"], datos["ap_paterno"], datos["ap_materno"], datos["cargo"],
             datos["telefono"], datos["email"], datos["fecha_contratacion"], salario_float))
            conexion.commit()
            messagebox.showinfo("Éxito", "Empleado registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
        finally:
            conexion.close()

    ttk.Button(frame, text="Registrar Empleado", command=guardar).grid(row=len(campos) + 1, column=0, columnspan=2,
                                                                       pady=20)


def registrar_vehiculo():
    ventana = tk.Toplevel()
    ventana.title("Registrar Vehículo")
    ventana.geometry("400x400")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    campos = [
        ("ID Cliente", "id_cliente"),
        ("Marca", "marca"),
        ("Modelo", "modelo"),
        ("Año", "año"),
        ("Color", "color"),
        ("Placas", "placas")
    ]
    entradas = {}

    for i, (label, key) in enumerate(campos):
        ttk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=5)
        entry = ttk.Entry(frame, width=30)
        entry.grid(row=i, column=1, pady=5)
        entradas[key] = entry

    def guardar():
        datos = {k: e.get() for k, e in entradas.items()}
        if not all([datos["id_cliente"], datos["marca"], datos["modelo"], datos["año"], datos["placas"]]):
            messagebox.showerror("Error", "Por favor completa todos los campos obligatorios.")
            return
        try:
            año_int = int(datos["año"])
        except ValueError:
            messagebox.showerror("Error", "El año debe ser un número entero.")
            return

        conexion = conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO Vehiculos (id_cliente, marca, modelo, año, color, placas) VALUES (%s, %s, %s, %s, %s, %s)",
                           (datos["id_cliente"], datos["marca"], datos["modelo"], año_int, datos["color"], datos["placas"]))
            conexion.commit()
            messagebox.showinfo("Éxito", "Vehículo registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
        finally:
            conexion.close()

    ttk.Button(frame, text="Registrar Vehículo", command=guardar).grid(row=len(campos)+1, column=0, columnspan=2, pady=20)


def registrar_inventario():
    ventana = tk.Toplevel()
    ventana.title("Registrar Producto en Inventario")
    ventana.geometry("400x400")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    campos = [
        ("Nombre del Producto", "nombre"),
        ("Descripción", "descripcion"),
        ("Cantidad", "cantidad"),
        ("Precio", "precio")
    ]
    entradas = {}

    for i, (label, key) in enumerate(campos):
        ttk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=5)
        entry = ttk.Entry(frame, width=30)
        entry.grid(row=i, column=1, pady=5)
        entradas[key] = entry

    def guardar():
        datos = {k: e.get().strip() for k, e in entradas.items()}
        if not all([datos["nombre"], datos["cantidad"], datos["precio"]]):
            messagebox.showerror("Error", "Nombre, Cantidad y Precio son obligatorios.")
            return
        try:
            cantidad = int(datos["cantidad"])
            precio = float(datos["precio"])
            if cantidad < 0:
                raise ValueError("Cantidad negativa")
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un entero ≥ 0 y Precio un número válido.")
            return

        conexion = conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO Inventario (nombre, descripcion, cantidad, precio)
                VALUES (%s, %s, %s, %s)
            """, (datos["nombre"], datos["descripcion"], cantidad, precio))
            conexion.commit()
            messagebox.showinfo("Éxito", "Producto registrado en inventario.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
        finally:
            conexion.close()

    ttk.Button(frame, text="Registrar Producto", command=guardar).grid(row=len(campos)+1, column=0, columnspan=2, pady=20)


def registrar_cita():
    ventana = tk.Toplevel()
    ventana.title("Registrar Cita")
    ventana.geometry("400x450")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text="ID Vehículo:").grid(row=0, column=0, sticky="w", pady=5)
    id_vehiculo_entry = ttk.Entry(frame, width=30)
    id_vehiculo_entry.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", pady=5)
    fecha_entry = ttk.Entry(frame, width=30)
    fecha_entry.grid(row=1, column=1, pady=5)

    ttk.Label(frame, text="Hora (HH:MM):").grid(row=2, column=0, sticky="w", pady=5)
    hora_entry = ttk.Entry(frame, width=30)
    hora_entry.grid(row=2, column=1, pady=5)

    ttk.Label(frame, text="Estado:").grid(row=3, column=0, sticky="w", pady=5)
    estado_var = tk.StringVar()
    estado_combo = ttk.Combobox(frame, textvariable=estado_var, state="readonly",
                                 values=["Pendiente", "Completado", "Cancelado"])
    estado_combo.set("Pendiente")
    estado_combo.grid(row=3, column=1, pady=5)

    ttk.Label(frame, text="Observaciones:").grid(row=4, column=0, sticky="w", pady=5)
    observaciones_entry = ttk.Entry(frame, width=30)
    observaciones_entry.grid(row=4, column=1, pady=5)

    def guardar():
        id_vehiculo = id_vehiculo_entry.get().strip()
        fecha = fecha_entry.get().strip()
        hora = hora_entry.get().strip()
        estado = estado_var.get().strip()
        observaciones = observaciones_entry.get().strip()

        if not all([id_vehiculo, fecha, hora]):
            messagebox.showerror("Error", "ID Vehículo, Fecha y Hora son obligatorios.")
            return

        conexion = conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO Citas (id_vehiculo, fecha, hora, estado, observaciones)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_vehiculo, fecha, hora, estado, observaciones))
            conexion.commit()
            messagebox.showinfo("Éxito", "Cita registrada correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
        finally:
            conexion.close()

    ttk.Button(frame, text="Registrar Cita", command=guardar).grid(row=5, column=0, columnspan=2, pady=20)


def registrar_servicio():
    ventana = tk.Toplevel()
    ventana.title("Registrar Servicio")
    ventana.geometry("400x350")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    campos = [
        ("Nombre del Servicio", "nombre"),
        ("Descripción", "descripcion"),
        ("Costo", "costo"),
        ("Duración (minutos)", "duracion")
    ]
    entradas = {}

    for i, (label, key) in enumerate(campos):
        ttk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=5)
        entry = ttk.Entry(frame, width=30)
        entry.grid(row=i, column=1, pady=5)
        entradas[key] = entry

    def guardar():
        datos = {k: e.get() for k, e in entradas.items()}
        if not all(datos.values()):
            messagebox.showerror("Error", "Por favor completa todos los campos.")
            return
        try:
            costo_float = float(datos["costo"])
            duracion_int = int(datos["duracion"])
        except ValueError:
            messagebox.showerror("Error", "Costo debe ser número y duración un entero.")
            return

        conexion = conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO Servicios (nombre, descripcion, costo, duracion) VALUES (%s, %s, %s, %s)",
                           (datos["nombre"], datos["descripcion"], costo_float, duracion_int))
            conexion.commit()
            messagebox.showinfo("Éxito", "Servicio registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
        finally:
            conexion.close()

    ttk.Button(frame, text="Registrar Servicio", command=guardar).grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

def registrar_vehiculo_empresa():
    ventana = tk.Toplevel()
    ventana.title("Registrar Vehículo de Empresa")
    ventana.geometry("400x350")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(fill="both", expand=True)

    campos = [
        ("Tipo (Ej: Grúa, Camioneta)", "tipo"),
        ("Marca", "marca"),
        ("Modelo", "modelo"),
        ("Placas", "placas"),
        ("Estado", "estado")
    ]
    entradas = {}

    for i, (label, key) in enumerate(campos):
        ttk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=5)
        if key == "estado":
            estado_var = tk.StringVar()
            combo_estado = ttk.Combobox(frame, textvariable=estado_var, state="readonly",
                                        values=["Disponible", "En mantenimiento"])
            combo_estado.grid(row=i, column=1, pady=5)
            combo_estado.set("Disponible")
            entradas[key] = estado_var
        else:
            entry = ttk.Entry(frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            entradas[key] = entry

    def guardar():
        datos = {k: e.get().strip() for k, e in entradas.items()}
        if not all([datos["tipo"], datos["placas"], datos["estado"]]):
            messagebox.showerror("Error", "Tipo, Placas y Estado son obligatorios.")
            return

        conexion = conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO Vehiculos_Empresa (tipo, marca, modelo, placas, estado)
                VALUES (%s, %s, %s, %s, %s)
            """, (datos["tipo"], datos["marca"], datos["modelo"], datos["placas"], datos["estado"]))
            conexion.commit()
            messagebox.showinfo("Éxito", "Vehículo de empresa registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
        finally:
            conexion.close()

    ttk.Button(frame, text="Registrar Vehículo", command=guardar).grid(row=len(campos), column=0, columnspan=2, pady=20)

import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="edson9911",
        database="TallerMecanico"
    )

# ... (resto del código omitido por brevedad, mantenlo igual hasta la definición del menú)

def registrar_orden_empleado():
    ventana = tk.Toplevel()
    ventana.title("Asignar Orden a Empleado")
    ventana.geometry("400x300")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text="ID Orden:").grid(row=0, column=0, sticky="w", pady=5)
    id_orden_entry = ttk.Entry(frame, width=30)
    id_orden_entry.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="ID Usuario (Empleado):").grid(row=1, column=0, sticky="w", pady=5)
    id_usuario_entry = ttk.Entry(frame, width=30)
    id_usuario_entry.grid(row=1, column=1, pady=5)

    def guardar():
        id_orden = id_orden_entry.get().strip()
        id_usuario = id_usuario_entry.get().strip()
        if not id_orden or not id_usuario:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        conexion = conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO Ordenes_Empleados (id_orden, id_usuario) VALUES (%s, %s)", (id_orden, id_usuario))
            conexion.commit()
            messagebox.showinfo("Éxito", "Orden asignada correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo asignar: {e}")
        finally:
            conexion.close()

    ttk.Button(frame, text="Asignar Orden", command=guardar).grid(row=2, column=0, columnspan=2, pady=20)

def mostrar_menu(usuario):
    menu = tk.Tk()
    menu.title("Menú Principal")
    menu.geometry("400x400")
    menu.minsize(300, 250)
    menu.resizable(True, True)
    menu.configure(bg="#f2f2f2")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Segoe UI", 10), padding=6)
    style.configure("TLabel", font=("Segoe UI", 12), background="#f2f2f2")

    frame = ttk.Frame(menu, padding=20)
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text=f"Bienvenido, {usuario[1]} ({usuario[5]})").pack(pady=10)

    if usuario[5] == "Administrador":
        ttk.Button(frame, text="Ver Todos los Datos", command=mostrar_todos_los_datos).pack(fill="x", pady=5)
        ttk.Button(frame, text="Registrar Usuario", command=registrar_usuario).pack(fill="x", pady=5)
        ttk.Button(frame, text="Registrar Cliente", command=registrar_cliente).pack(fill="x", pady=5)
        ttk.Button(frame, text="Registrar Vehiculo", command=registrar_vehiculo).pack(fill="x", pady=5)
        ttk.Button(frame, text="Registrar Servicio", command=registrar_servicio).pack(fill="x", pady=5)
        ttk.Button(frame, text="Registrar Producto", command=registrar_inventario).pack(fill="x", pady=5)
        ttk.Button(frame, text="Registrar Proveedor", command=registrar_proveedor).pack(fill="x", pady=5)
        ttk.Button(frame, text="Registrar Vehículo Empresa", command=registrar_vehiculo_empresa).pack(fill="x", pady=5)
        ttk.Button(frame, text="Asignar Orden a Empleado", command=registrar_orden_empleado).pack(fill="x", pady=5)
        ttk.Button(frame, text="Cerrar", command=menu.destroy).pack(fill="x", pady=5)
    elif usuario[5] == "Mecanico":
        ttk.Button(frame, text="Ver Órdenes de Trabajo", command=lambda: ver_ordenes_mecanico(usuario)).pack(fill="x", pady=5)
        ttk.Button(frame, text="Cerrar", command=menu.destroy).pack(fill="x", pady=5)
    elif usuario[5] == "Recepcionista":
        ttk.Button(frame, text="Registrar Citas", command=registrar_cita).pack(fill="x", pady=5)
        ttk.Button(frame, text="Ver Agenda del Día").pack(fill="x", pady=5)
        ttk.Button(frame, text="Cerrar", command=menu.destroy).pack(fill="x", pady=5)



def login():
    nombre = entry_usuario.get()
    password = entry_password.get()
    usuario = verificar_credenciales(nombre, password)
    if usuario:
        messagebox.showinfo("Inicio de sesión", f"Acceso concedido. Bienvenido, {nombre}!")
        ventana.destroy()
        mostrar_menu(usuario)
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

def crear_ventana_login():
    global entry_usuario, entry_password, ventana
    ventana = tk.Tk()
    ventana.title("Login - Taller Mecánico")
    ventana.geometry("350x220")
    ventana.minsize(300, 200)
    ventana.resizable(True, True)
    ventana.configure(bg="#f2f2f2")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", font=("Segoe UI", 10), background="#f2f2f2")
    style.configure("TEntry", font=("Segoe UI", 10), padding=5)
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

    frame = ttk.Frame(ventana, padding="20")
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text="Usuario:").grid(row=0, column=0, sticky="w", pady=5)
    entry_usuario = ttk.Entry(frame, width=30)
    entry_usuario.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=5)
    entry_password = ttk.Entry(frame, show="*", width=30)
    entry_password.grid(row=1, column=1, pady=5)

    ttk.Button(frame, text="Iniciar sesión", command=login).grid(row=2, column=0, columnspan=2, pady=15)

    ventana.mainloop()

if __name__ == "__main__":
    agregar_usuarios_predeterminados()
    crear_ventana_login()