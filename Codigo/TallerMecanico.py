# TallerMecanico.py

import tkinter as tk
from tkinter import messagebox, ttk

import mysql

# No se importa mysql.connector directamente: todo se hace via 'consultas' y 'conexion'
from conexion import conectar
from consultas import (
    agregar_usuarios_predeterminados,
    verificar_credenciales,
    obtener_filas,
    eliminar_registro,
    registrar_proveedor,
    obtener_ordenes_mecanico_por_nombre,
    registrar_usuario,
    registrar_cliente,
    registrar_vehiculo,
    registrar_producto_inventario,
    registrar_cita,
    registrar_servicio,
    registrar_vehiculo_empresa,
    registrar_orden_empleado,
    obtener_agenda_del_dia
)


def mostrar_todos_los_datos():
    ventana = tk.Toplevel()
    ventana.title("Datos Completos del Sistema")
    ventana.geometry("900x600")
    ventana.minsize(700, 400)

    notebook = ttk.Notebook(ventana)
    notebook.pack(expand=True, fill="both")

    tablas = {
        "Usuarios":           ("SELECT * FROM Usuarios",           "Usuarios",            "id_usuario"),
        "Clientes":           ("SELECT * FROM Clientes",           "Clientes",            "id_cliente"),
        "Vehículos":          ("SELECT * FROM Vehiculos",          "Vehiculos",           "id_vehiculo"),
        "Servicios":          ("SELECT * FROM Servicios",          "Servicios",           "id_servicio"),
        "Citas":              ("SELECT * FROM Citas",              "Citas",               "id_cita"),
        "Órdenes de Trabajo": ("SELECT * FROM Ordenes_Trabajo",     "Ordenes_Trabajo",     "id_orden"),
        "Inventario":         ("SELECT * FROM Inventario",         "Inventario",          "id_producto"),
        "Proveedores":        ("SELECT * FROM Proveedores",        "Proveedores",         "id_proveedor"),
        "Vehículos Empresa":  ("SELECT * FROM Vehiculos_Empresa",  "Vehiculos_Empresa",   "id_vehiculo_empresa"),
        "Órdenes Empleados":  ("SELECT * FROM Ordenes_Empleados",  "Ordenes_Empleados",   "id_orden")
    }

    for nombre_tabla, (query_sql, nombre_sql, id_columna) in tablas.items():
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=nombre_tabla)

        contenedor = ttk.Frame(frame)
        contenedor.pack(expand=True, fill="both")

        scroll_y = ttk.Scrollbar(contenedor, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        scroll_x = ttk.Scrollbar(contenedor, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        tree = ttk.Treeview(
            contenedor,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        tree.pack(side="left", fill="both", expand=True)

        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)

        # Cargar datos usando la función genérica de consultas
        columnas, filas = obtener_filas(query_sql)
        tree["columns"] = columnas
        tree["show"] = "headings"
        for col in columnas:
            texto_col = col.replace("_", " ").title()
            tree.heading(col, text=texto_col)
            if col.startswith("id_"):
                tree.column(col, width=0, stretch=False)
            else:
                tree.column(col, anchor="center")
        for row in filas:
            tree.insert("", "end", values=row)

        def eliminar_registro_activo(treeview=tree, tabla=nombre_sql, col_id=id_columna):
            selected_item = treeview.selection()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecciona un registro para eliminar.")
                return
            item = treeview.item(selected_item[0])
            record_id = item["values"][0]
            confirm = messagebox.askyesno("Confirmar", f"¿Eliminar registro {record_id} de {tabla}?")
            if confirm:
                try:
                    eliminar_registro(tabla, col_id, record_id)
                    treeview.delete(selected_item[0])
                    messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"No se pudo eliminar: {e}")

        # Frame de botones
        botones_frame = ttk.Frame(frame)
        botones_frame.pack(pady=5)

        ttk.Button(
            botones_frame,
            text="Eliminar Seleccionado",
            command=eliminar_registro_activo
        ).pack(side="left", padx=5)

        # Botones de registro según la tabla
        if nombre_tabla == "Usuarios":
            ttk.Button(
                botones_frame,
                text="Registrar Nuevo Usuario",
                command=registrar_usuario
            ).pack(side="left", padx=5)
        elif nombre_tabla == "Clientes":
            ttk.Button(
                botones_frame,
                text="Registrar Nuevo Cliente",
                command=registrar_cliente
            ).pack(side="left", padx=5)
        elif nombre_tabla == "Vehículos":
            ttk.Button(
                botones_frame,
                text="Registrar Nuevo Vehículo",
                command=registrar_vehiculo
            ).pack(side="left", padx=5)
        elif nombre_tabla == "Servicios":
            ttk.Button(
                botones_frame,
                text="Registrar Nuevo Servicio",
                command=registrar_servicio
            ).pack(side="left", padx=5)
        elif nombre_tabla == "Citas":
            ttk.Button(
                botones_frame,
                text="Registrar Nueva Cita",
                command=registrar_cita
            ).pack(side="left", padx=5)
        elif nombre_tabla == "Inventario":
            ttk.Button(
                botones_frame,
                text="Registrar Nuevo Producto",
                command=registrar_producto_inventario
            ).pack(side="left", padx=5)
        elif nombre_tabla == "Proveedores":
            ttk.Button(
                botones_frame,
                text="Registrar Nuevo Proveedor",
                command=registrar_proveedor
            ).pack(side="left", padx=5)
        elif nombre_tabla == "Vehículos Empresa":
            ttk.Button(
                botones_frame,
                text="Registrar Vehículo de Empresa",
                command=registrar_vehiculo_empresa
            ).pack(side="left", padx=5)
        elif nombre_tabla == "Órdenes Empleados":
            ttk.Button(
                botones_frame,
                text="Asignar Orden a Empleado",
                command=registrar_orden_empleado
            ).pack(side="left", padx=5)


def ver_ordenes_mecanico(usuario):
    ventana = tk.Toplevel()
    ventana.title("Órdenes de Trabajo Asignadas")
    ventana.geometry("800x500")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=10)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(
        frame,
        columns=("ID Orden", "Estado", "Fecha Inicio", "Fecha Fin"),
        show="headings"
    )
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True)

    filas = obtener_ordenes_mecanico_por_nombre(usuario[1])
    for fila in filas:
        tree.insert("", "end", values=fila)


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

        try:
            registrar_usuario(
                datos["nombre"],
                datos["ap_paterno"],
                datos["ap_materno"],
                datos["email"],
                datos["contraseña"],
                datos["rol"],
                datos["telefono"],
                datos["fecha_contratacion"],
                salario
            )
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

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
        try:
            registrar_cliente(
                datos["nombre"],
                datos["ap_paterno"],
                datos["ap_materno"],
                datos["direccion"],
                datos["telefono"],
                datos["email"]
            )
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    ttk.Button(frame, text="Registrar Cliente", command=guardar).grid(row=len(campos)+1, column=0, columnspan=2, pady=20)


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

        try:
            registrar_vehiculo(
                datos["id_cliente"],
                datos["marca"],
                datos["modelo"],
                año_int,
                datos["color"],
                datos["placas"]
            )
            messagebox.showinfo("Éxito", "Vehículo registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    ttk.Button(frame, text="Registrar Vehículo", command=guardar).grid(
        row=len(campos)+1, column=0, columnspan=2, pady=20
    )


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

        try:
            registrar_producto_inventario(
                datos["nombre"],
                datos["descripcion"],
                cantidad,
                precio
            )
            messagebox.showinfo("Éxito", "Producto registrado en inventario.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    ttk.Button(frame, text="Registrar Producto", command=guardar).grid(
        row=len(campos)+1, column=0, columnspan=2, pady=20
    )


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
    estado_combo = ttk.Combobox(
        frame,
        textvariable=estado_var,
        state="readonly",
        values=["Pendiente", "Completado", "Cancelado"]
    )
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

        try:
            registrar_cita(
                id_vehiculo,
                fecha,
                hora,
                estado,
                observaciones
            )
            messagebox.showinfo("Éxito", "Cita registrada correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    ttk.Button(frame, text="Registrar Cita", command=guardar).grid(
        row=5, column=0, columnspan=2, pady=20
    )


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
            messagebox.showerror("Error", "Costo debe ser número y duracion un entero.")
            return

        try:
            registrar_servicio(
                datos["nombre"],
                datos["descripcion"],
                costo_float,
                duracion_int
            )
            messagebox.showinfo("Éxito", "Servicio registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    ttk.Button(frame, text="Registrar Servicio", command=guardar).grid(
        row=len(campos)+1, column=0, columnspan=2, pady=20
    )


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
            combo_estado = ttk.Combobox(
                frame,
                textvariable=estado_var,
                state="readonly",
                values=["Disponible", "En mantenimiento"]
            )
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

        try:
            registrar_vehiculo_empresa(
                datos["tipo"],
                datos["marca"],
                datos["modelo"],
                datos["placas"],
                datos["estado"]
            )
            messagebox.showinfo("Éxito", "Vehículo de empresa registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    ttk.Button(frame, text="Registrar Vehículo", command=guardar).grid(
        row=len(campos), column=0, columnspan=2, pady=20
    )


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

        try:
            registrar_orden_empleado(id_orden, id_usuario)
            messagebox.showinfo("Éxito", "Orden asignada correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo asignar: {e}")

    ttk.Button(frame, text="Asignar Orden", command=guardar).grid(row=2, column=0, columnspan=2, pady=20)


def ver_agenda_dia():
    ventana = tk.Toplevel()
    ventana.title("Agenda del Día")
    ventana.geometry("800x400")

    frame = ttk.Frame(ventana, padding=10)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(
        frame,
        columns=("ID Cita", "Vehículo", "Fecha", "Hora", "Estado"),
        show="headings"
    )
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True)

    filas = obtener_agenda_del_dia()
    for fila in filas:
        tree.insert("", "end", values=fila)


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
        ttk.Button(frame, text="Cerrar", command=menu.destroy).pack(fill="x", pady=5)

    elif usuario[5] == "Mecanico":
        ttk.Button(frame, text="Ver Órdenes de Trabajo", command=lambda: ver_ordenes_mecanico(usuario)).pack(fill="x", pady=5)
        ttk.Button(frame, text="Cerrar", command=menu.destroy).pack(fill="x", pady=5)

    elif usuario[5] == "Recepcionista":
        ttk.Button(frame, text="Registrar Citas", command=registrar_cita).pack(fill="x", pady=5)
        ttk.Button(frame, text="Ver Agenda del Día", command=ver_agenda_dia).pack(fill="x", pady=5)
        ttk.Button(frame, text="Cerrar", command=menu.destroy).pack(fill="x", pady=5)


def iniciar_sesion():
    nombre = entry_usuario.get()
    password = entry_password.get()
    if not nombre or not password:
        messagebox.showwarning("Campos vacíos", "Por favor, ingresa usuario y contraseña.")
        return
    usuario = verificar_credenciales(nombre, password)
    if usuario:
        messagebox.showinfo("Bienvenido", f"Hola {usuario[1]} ({usuario[5]})")
        ventana.destroy()
        mostrar_menu(usuario)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


def crear_ventana_login():
    global entry_usuario, entry_password, ventana
    ventana = tk.Tk()
    ventana.title("Login - Taller Mecánico")
    ventana.geometry("350x220")
    ventana.minsize(300, 200)
    ventana.resizable(False, False)
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

    ttk.Button(frame, text="Iniciar sesión", command=iniciar_sesion).grid(
        row=2, column=0, columnspan=2, pady=15
    )

    ventana.mainloop()


if __name__ == "__main__":
    # Conservamos la llamada original para cargar usuarios predeterminados
    agregar_usuarios_predeterminados()
    crear_ventana_login()
