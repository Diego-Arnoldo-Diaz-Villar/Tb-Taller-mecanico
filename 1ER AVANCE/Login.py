import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tobias",
        database="TallerMecanico"
    )

def agregar_usuarios_predeterminados():
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
        "Usuarios": "SELECT * FROM Usuarios",
        "Clientes": "SELECT * FROM Clientes",
        "Vehículos": "SELECT * FROM Vehiculos",
        "Servicios": "SELECT * FROM Servicios",
        "Citas": "SELECT * FROM Citas",
        "Empleados": "SELECT * FROM Empleados",
        "Órdenes de Trabajo": "SELECT * FROM Ordenes_Trabajo",
        "Inventario": "SELECT * FROM Inventario",
        "Proveedores": "SELECT * FROM Proveedores",
        "Vehículos Empresa": "SELECT * FROM Vehiculos_Empresa"
    }

    conexion = conectar()
    cursor = conexion.cursor()

    for nombre_tabla, query in tablas.items():
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=nombre_tabla)
        tree = ttk.Treeview(frame)
        tree.pack(expand=True, fill="both")

        cursor.execute(query)
        columnas = [desc[0] for desc in cursor.description]
        tree["columns"] = columnas
        tree["show"] = "headings"

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    conexion.close()

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
    ventana.geometry("400x400")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    campos = [
        ("Nombre", "nombre"),
        ("Apellido Paterno", "ap_paterno"),
        ("Apellido Materno", "ap_materno"),
        ("Correo Electrónico", "email"),
        ("Contraseña", "contraseña"),
    ]
    entradas = {}

    for i, (label, key) in enumerate(campos):
        ttk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=5)
        entry = ttk.Entry(frame, width=30, show="*" if key == "contraseña" else "")
        entry.grid(row=i, column=1, pady=5)
        entradas[key] = entry

    ttk.Label(frame, text="Rol:").grid(row=len(campos), column=0, sticky="w", pady=5)
    rol_var = tk.StringVar()
    combo_rol = ttk.Combobox(frame, textvariable=rol_var, state="readonly", values=["Administrador", "Mecanico", "Recepcionista"])
    combo_rol.grid(row=len(campos), column=1, pady=5)

    def guardar():
        datos = {k: e.get() for k, e in entradas.items()}
        rol = rol_var.get()
        if not all([datos["nombre"], datos["ap_paterno"], datos["email"], datos["contraseña"], rol]):
            messagebox.showerror("Error", "Por favor completa todos los campos obligatorios.")
            return
        conexion = conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO Usuarios (nombre, ap_paterno, ap_materno, email, contraseña, rol) VALUES (%s, %s, %s, %s, %s, %s)",
                           (datos["nombre"], datos["ap_paterno"], datos["ap_materno"], datos["email"], datos["contraseña"], rol))
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
        ttk.Button(frame, text="Cerrar", command=menu.destroy).pack(fill="x", pady=5)
    elif usuario[5] == "Mecanico":
        ttk.Button(frame, text="Ver Órdenes de Trabajo", command=lambda: ver_ordenes_mecanico(usuario)).pack(fill="x", pady=5)
        ttk.Button(frame, text="Cerrar", command=menu.destroy).pack(fill="x", pady=5)
    elif usuario[5] == "Recepcionista":
        ttk.Button(frame, text="Registrar Citas").pack(fill="x", pady=5)
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
