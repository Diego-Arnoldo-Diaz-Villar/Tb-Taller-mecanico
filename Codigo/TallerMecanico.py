import re
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from consultas import (
    agregar_usuarios_predeterminados,
    verificar_credenciales,
    obtener_filas,
    eliminar_registro,
    registrar_usuario as db_registrar_usuario,
    registrar_cliente as db_registrar_cliente,
    obtener_clientes,
    registrar_vehiculo as db_registrar_vehiculo,
    obtener_vehiculos_modelo,
    registrar_cita as db_registrar_cita,
    obtener_ordenes_mecanico_por_nombre,
    registrar_producto_inventario,
    registrar_proveedor,
    registrar_vehiculo_empresa,
    registrar_servicio as db_registrar_servicio,
    obtener_servicios,
    registrar_orden_trabajo as db_registrar_orden_trabajo,
    obtener_ordenes_con_servicio_y_mecanicos,
    obtener_mecanicos,
    asignar_empleado_a_orden as db_asignar_empleado_a_orden,
    obtener_agenda_del_dia, actualizar_estado_orden
)


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


        "Citas": (
            """
            SELECT 
                c.id_cita          AS id_cita,
                v.id_cliente       AS id_cliente,
                v.modelo           AS modelo,
                c.fecha            AS fecha,
                c.hora             AS hora,
                c.estado           AS estado,
                c.observaciones    AS observaciones
            FROM Citas c
            JOIN Vehiculos v ON c.id_vehiculo = v.id_vehiculo
            """,
            "Citas",
            "id_cita"
        ),


        "Órdenes de Trabajo": (
            """
            SELECT 
              o.id_orden,
              o.id_cliente,
              o.id_vehiculo,
              s.nombre           AS servicio_nombre,
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
            """,
            "Ordenes_Trabajo",
            "id_orden"
        ),

        "Inventario": ("SELECT * FROM Inventario", "Inventario", "id_producto"),
        "Proveedores": ("SELECT * FROM Proveedores", "Proveedores", "id_proveedor"),
        "Vehículos Empresa": ("SELECT * FROM Vehiculos_Empresa", "Vehiculos_Empresa", "id_vehiculo_empresa")
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

        # Función para refrescar
        def crear_refresh(tabla_tree, sql_query):
            def refrescar_tabla():
                for item in tabla_tree.get_children():
                    tabla_tree.delete(item)
                _, nuevas_filas = obtener_filas(sql_query)
                for nueva in nuevas_filas:
                    tabla_tree.insert("", "end", values=nueva)
            return refrescar_tabla

        refresh_callback = crear_refresh(tree, query_sql)


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

        # botones
        botones_frame = ttk.Frame(frame)
        botones_frame.pack(pady=5)

        ttk.Button(
            botones_frame,
            text="Eliminar Seleccionado",
            command=eliminar_registro_activo
        ).pack(side="left", padx=5)

        ttk.Button(
            botones_frame,
            text="Refresh",
            command=refresh_callback
        ).pack(side="left", padx=5)


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
                command=registrar_servicio_ui
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
                command=registrar_inventario
            ).pack(side="left", padx=5)


        elif nombre_tabla == "Vehículos Empresa":
            ttk.Button(
                botones_frame,
                text="Registrar Vehículo de Empresa",
                command=registrar_vehiculo_empresa_ui
            ).pack(side="left", padx=5)


        elif nombre_tabla == "Órdenes de Trabajo":
            ttk.Button(
                botones_frame,
                text="Registrar Nueva Orden",
                command=registrar_orden_trabajo_ui
            ).pack(side="left", padx=5)
            ttk.Button(
                botones_frame,
                text="Asignar Empleado",
                command=asignar_empleado_a_orden_ui
            ).pack(side="left", padx=5)

        elif nombre_tabla == "Proveedores":
            ttk.Button(
                botones_frame,
                text="Registrar Nuevo Proveedor",
                command=registrar_proveedor_ui
            ).pack(side="left", padx=5)

def ver_ordenes_mecanico(usuario):
    ventana = tk.Toplevel()
    ventana.title("Órdenes de Trabajo Asignadas")
    ventana.geometry("1050x450")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=10)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(
        frame,
        columns=("ID Orden", "ID Cliente", "ID Vehículo", "Servicio", "Descripción", "Estado", "Fecha Registro", "Fecha Fin"),
        show="headings"
    )
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    tree.pack(fill="both", expand=True)

    def cargar_datos():
        for item in tree.get_children():
            tree.delete(item)
        filas = obtener_ordenes_mecanico_por_nombre(usuario[1])
        for f in filas:
            tree.insert("", "end", values=(
                f["id_orden"], f["id_cliente"], f["id_vehiculo"],
                f["servicio_nombre"], f["descripcion"], f["estado"],
                f["fecha_registro"], f["fecha_fin"]
            ))

    cargar_datos()

    # Sección para actualizar estado
    control_frame = ttk.Frame(ventana, padding=10)
    control_frame.pack()

    ttk.Label(control_frame, text="Nuevo estado:").pack(side="left", padx=5)
    estado_var = tk.StringVar()
    estado_combo = ttk.Combobox(
        control_frame,
        textvariable=estado_var,
        values=["Pendiente", "En Proceso", "Completada"],
        state="readonly",
        width=20
    )
    estado_combo.pack(side="left", padx=5)

    def cambiar_estado():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona una orden.")
            return

        item = tree.item(seleccionado[0])
        id_orden = item["values"][0]
        nuevo_estado = estado_var.get()

        if not nuevo_estado:
            messagebox.showwarning("Advertencia", "Selecciona un nuevo estado.")
            return

        try:
            actualizar_estado_orden(id_orden, nuevo_estado)
            messagebox.showinfo("Éxito", f"Estado actualizado a '{nuevo_estado}' para orden {id_orden}")
            cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el estado:\n{e}")

    ttk.Button(control_frame, text="Actualizar Estado", command=cambiar_estado).pack(side="left", padx=10)

def registrar_usuario():
    ventana = tk.Toplevel()
    ventana.title("Registrar Usuario")
    ventana.geometry("450x550")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    def validar_telefono(nuevo_valor):
        if nuevo_valor == "":
            return True
        return nuevo_valor.isdigit() and len(nuevo_valor) <= 10

    vcmd_tel = frame.register(validar_telefono)


    def validar_salario(nuevo_valor):
        if nuevo_valor == "":
            return True
        return re.match(r"^\d*\.?\d{0,2}$", nuevo_valor) is not None

    vcmd_salario = frame.register(validar_salario)

    campos = [
        ("Nombre", "nombre"),
        ("Apellido Paterno", "ap_paterno"),
        ("Apellido Materno", "ap_materno"),
        ("Correo Electrónico", "email"),
        ("Contraseña", "contrasena"),
        ("Rol", "rol"),
        ("Teléfono", "telefono"),
        ("Fecha de Contratación", "fecha_cont"),
        ("Salario", "salario")
    ]
    entradas = {}

    for i, (label, key) in enumerate(campos):
        ttk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=5)

        if key == "contrasena":
            entry = ttk.Entry(frame, width=30, show="*")
            entry.grid(row=i, column=1, pady=5)
            entradas[key] = entry

        elif key == "rol":
            combo = ttk.Combobox(
                frame,
                values=["Administrador", "Mecanico", "Recepcionista"],
                state="readonly",
                width=28
            )
            combo.set("Administrador")
            combo.grid(row=i, column=1, pady=5)
            entradas[key] = combo

        elif key == "telefono":
            entry = ttk.Entry(frame, width=30, validate="key", validatecommand=(vcmd_tel, "%P"))
            entry.grid(row=i, column=1, pady=5)
            entradas[key] = entry

        elif key == "fecha_cont":
            entry = DateEntry(frame, date_pattern='yyyy-MM-dd')
            entry.grid(row=i, column=1, pady=5)
            entradas[key] = entry

        elif key == "salario":
            entry = ttk.Entry(frame, width=30, validate="key", validatecommand=(vcmd_salario, "%P"))
            entry.grid(row=i, column=1, pady=5)

            def formatear_salario(event, e=entry):
                txt = e.get().strip().replace(",", "")
                if txt:
                    try:
                        val = float(txt)
                        e.delete(0, tk.END)
                        e.insert(0, f"{val:,.2f}")
                    except ValueError:
                        pass

            entry.bind("<FocusOut>", formatear_salario)
            entradas[key] = entry

        else:
            entry = ttk.Entry(frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            entradas[key] = entry

    def guardar():
        datos = {}
        for k, widget in entradas.items():
            if k == "fecha_cont":
                f = widget.get_date()
                datos[k] = f.strftime("%Y-%m-%d")
            else:
                datos[k] = widget.get().strip()

        obligatorios = [
            "nombre", "ap_paterno", "email",
            "contrasena", "rol", "telefono",
            "fecha_cont", "salario"
        ]
        vacio = [c for c in obligatorios if datos.get(c, "") == ""]
        if vacio:
            messagebox.showerror("Error", f"Faltan completar campos obligatorios: {vacio}")
            return

        tel = datos["telefono"]
        if not (tel.isdigit() and len(tel) == 10):
            messagebox.showerror("Error", "El teléfono debe contener exactamente 10 dígitos.")
            return

        salario_txt = datos["salario"].replace(",", "")
        try:
            salario = float(salario_txt)
        except ValueError:
            messagebox.showerror("Error", "El salario ingresado no es un número válido.")
            return

        try:
            db_registrar_usuario(
                datos["nombre"],
                datos["ap_paterno"],
                datos["ap_materno"],
                datos["email"],
                datos["contrasena"],
                datos["rol"],
                datos["telefono"],
                datos["fecha_cont"],
                salario
            )
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario:\n{e}")

    ttk.Button(frame, text="Registrar Usuario", command=guardar).grid(
        row=len(campos), column=0, columnspan=2, pady=20
    )


def registrar_cliente():
    ventana = tk.Toplevel()
    ventana.title("Registrar Cliente")
    ventana.geometry("450x450")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    def validar_telefono(nuevo_valor):
        if nuevo_valor == "":
            return True
        return nuevo_valor.isdigit() and len(nuevo_valor) <= 10

    vcmd_tel = frame.register(validar_telefono)

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

        if key == "telefono":
            entry = ttk.Entry(frame, width=30, validate="key", validatecommand=(vcmd_tel, "%P"))
            entry.grid(row=i, column=1, pady=5)
            entradas[key] = entry
        else:
            entry = ttk.Entry(frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            entradas[key] = entry

    def guardar():
        datos = {k: e.get().strip() for k, e in entradas.items()}

        obligatorios = ["nombre", "ap_paterno", "telefono"]
        vacio = [c for c in obligatorios if datos.get(c, "") == ""]
        if vacio:
            messagebox.showerror("Error", f"Faltan completar campos obligatorios: {vacio}")
            return

        tel = datos["telefono"]
        if not (tel.isdigit() and len(tel) == 10):
            messagebox.showerror("Error", "El teléfono debe contener exactamente 10 dígitos.")
            return

        try:
            db_registrar_cliente(
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
            messagebox.showerror("Error", f"No se pudo registrar el cliente:\n{e}")

    ttk.Button(frame, text="Registrar Cliente", command=guardar).grid(
        row=len(campos), column=0, columnspan=2, pady=20
    )


def registrar_vehiculo():
    ventana = tk.Toplevel()
    ventana.title("Registrar Vehículo")
    ventana.geometry("450x500")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")


    def validar_anio(nuevo_valor):
        if nuevo_valor == "":
            return True
        return nuevo_valor.isdigit() and len(nuevo_valor) <= 4

    vcmd_anio = frame.register(validar_anio)

    def validar_placas(nuevo_valor):
        if nuevo_valor == "":
            return True
        if len(nuevo_valor) > 9:
            return False
        return all(c.isalnum() or c == '-' for c in nuevo_valor.upper())

    vcmd_placas = frame.register(validar_placas)


    ttk.Label(frame, text="Cliente:").grid(row=0, column=0, sticky="w", pady=5)
    clientes = obtener_clientes()
    opciones = [
        f"{c['id_cliente']} - {c['nombre']} {c['ap_paterno']} {c['ap_materno']}"
        for c in clientes
    ]
    combo_clientes = ttk.Combobox(
        frame,
        values=opciones,
        state="readonly",
        width=30
    )
    combo_clientes.grid(row=0, column=1, pady=5)


    ttk.Label(frame, text="Marca:").grid(row=1, column=0, sticky="w", pady=5)
    entry_marca = ttk.Entry(frame, width=30)
    entry_marca.grid(row=1, column=1, pady=5)


    ttk.Label(frame, text="Modelo:").grid(row=2, column=0, sticky="w", pady=5)
    entry_modelo = ttk.Entry(frame, width=30)
    entry_modelo.grid(row=2, column=1, pady=5)


    ttk.Label(frame, text="Año:").grid(row=3, column=0, sticky="w", pady=5)
    entry_anio = ttk.Entry(
        frame,
        width=30,
        validate="key",
        validatecommand=(vcmd_anio, "%P")
    )
    entry_anio.grid(row=3, column=1, pady=5)


    ttk.Label(frame, text="Color:").grid(row=4, column=0, sticky="w", pady=5)
    entry_color = ttk.Entry(frame, width=30)
    entry_color.grid(row=4, column=1, pady=5)


    ttk.Label(frame, text="Placas (ABC-123-D):").grid(row=5, column=0, sticky="w", pady=5)
    entry_placas = ttk.Entry(
        frame,
        width=30,
        validate="key",
        validatecommand=(vcmd_placas, "%P")
    )
    entry_placas.grid(row=5, column=1, pady=5)

    def guardar():
        seleccion = combo_clientes.get()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un cliente.")
            return
        try:
            id_cliente = int(seleccion.split(" - ")[0])
        except ValueError:
            messagebox.showerror("Error", "Cliente inválido.")
            return

        marca = entry_marca.get().strip()
        modelo = entry_modelo.get().strip()
        anio_txt = entry_anio.get().strip()
        color = entry_color.get().strip()
        placas = entry_placas.get().strip().upper()

        if not all([marca, modelo, anio_txt, color, placas]):
            messagebox.showerror("Error", "Completa todos los campos.")
            return

        if not re.fullmatch(r"\d{4}", anio_txt):
            messagebox.showerror("Error", "El año debe tener 4 dígitos (p.ej. 2025).")
            return
        anio = int(anio_txt)
        if anio < 1900:
            messagebox.showerror("Error", "El año debe ser ≥ 1900.")
            return

        if not re.fullmatch(r"[A-Z]{3}-\d{3}-[A-Z]", placas):
            messagebox.showerror(
                "Error",
                "Formato de placas inválido. Debe ser 3 letras, guion, 3 números, guion, 1 letra.\nEjemplo: ABC-123-D"
            )
            return

        try:
            db_registrar_vehiculo(
                id_cliente,
                marca,
                modelo,
                anio,
                color,
                placas
            )
            messagebox.showinfo("Éxito", "Vehículo registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el vehículo:\n{e}")

    ttk.Button(frame, text="Registrar Vehículo", command=guardar).grid(
        row=6, column=0, columnspan=2, pady=20
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
            messagebox.showerror("Error", "Cantidad debe ser entero ≥ 0 y Precio número válido.")
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
    ventana.geometry("450x500")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text="Vehículo (ID - Modelo):").grid(row=0, column=0, sticky="w", pady=5)
    vehiculos = obtener_vehiculos_modelo()
    opciones_veh = [f"{v['id_vehiculo']} - {v['modelo']}" for v in vehiculos]
    combo_vehiculos = ttk.Combobox(frame, values=opciones_veh, state="readonly", width=28)
    combo_vehiculos.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", pady=5)
    fecha_entry = DateEntry(frame, date_pattern="yyyy-MM-dd")
    fecha_entry.grid(row=1, column=1, pady=5)

    ttk.Label(frame, text="Hora (HH:MM):").grid(row=2, column=0, sticky="w", pady=5)
    entry_hora = ttk.Entry(frame, width=30)
    entry_hora.grid(row=2, column=1, pady=5)

    ttk.Label(frame, text="Estado:").grid(row=3, column=0, sticky="w", pady=5)
    estado_var = tk.StringVar()
    estado_combo = ttk.Combobox(
        frame,
        textvariable=estado_var,
        state="readonly",
        values=["Pendiente", "Completado", "Cancelado"],
        width=28
    )
    estado_combo.set("Pendiente")
    estado_combo.grid(row=3, column=1, pady=5)

    ttk.Label(frame, text="Observaciones:").grid(row=4, column=0, sticky="w", pady=5)
    entry_observ = ttk.Entry(frame, width=30)
    entry_observ.grid(row=4, column=1, pady=5)

    def guardar():
        sel = combo_vehiculos.get()
        if not sel:
            messagebox.showerror("Error", "Selecciona un vehículo.")
            return
        try:
            id_vehiculo = int(sel.split(" - ")[0])
        except ValueError:
            messagebox.showerror("Error", "Vehículo inválido.")
            return

        fecha = fecha_entry.get_date().strftime("%Y-%m-%d")
        hora = entry_hora.get().strip()
        estado = estado_var.get().strip()
        observaciones = entry_observ.get().strip()

        if not (hora and fecha):
            messagebox.showerror("Error", "Fecha y hora son obligatorios.")
            return
        if not re.fullmatch(r"\d{2}:\d{2}", hora):
            messagebox.showerror("Error", "Hora inválida. Usa formato HH:MM")
            return

        try:
            db_registrar_cita(
                id_vehiculo,
                fecha,
                hora,
                estado,
                observaciones
            )
            messagebox.showinfo("Éxito", "Cita registrada correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar la cita:\n{e}")

    ttk.Button(frame, text="Registrar Cita", command=guardar).grid(
        row=5, column=0, columnspan=2, pady=20
    )


def registrar_servicio_ui():
    ventana = tk.Toplevel()
    ventana.title("Registrar Servicio")
    ventana.geometry("450x400")
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
        datos = {k: e.get().strip() for k, e in entradas.items()}
        if not all(datos.values()):
            messagebox.showerror("Error", "Por favor completa todos los campos.")
            return
        try:
            costo_float = float(datos["costo"])
            duracion_int = int(datos["duracion"])
        except ValueError:
            messagebox.showerror("Error", "Costo debe ser número y Duración entero.")
            return

        try:
            db_registrar_servicio(
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
        row=len(campos) + 1, column=0, columnspan=2, pady=20
    )


def registrar_orden_trabajo_ui():
    ventana = tk.Toplevel()
    ventana.title("Registrar Orden de Trabajo")
    ventana.geometry("550x450")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    # (ID - Nombre)
    ttk.Label(frame, text="Cliente (ID - Nombre):").grid(row=0, column=0, sticky="w", pady=5)

    clientes = obtener_clientes()
    opciones_clientes = [
        f"{c['id_cliente']} - {c['nombre']} {c['ap_paterno']} {c['ap_materno'] or ''}".strip()
        for c in clientes
    ]
    combo_clientes = ttk.Combobox(frame, values=opciones_clientes, state="readonly", width=37)
    combo_clientes.grid(row=0, column=1, pady=5)

    # Vehículo
    ttk.Label(frame, text="Vehículo (ID - Modelo):").grid(row=1, column=0, sticky="w", pady=5)
    vehiculos = obtener_vehiculos_modelo()
    opciones_veh = [f"{v['id_vehiculo']} - {v['modelo']}" for v in vehiculos]
    combo_vehiculos = ttk.Combobox(frame, values=opciones_veh, state="readonly", width=37)
    combo_vehiculos.grid(row=1, column=1, pady=5)

    # Servicio
    ttk.Label(frame, text="Servicio (ID - Nombre):").grid(row=2, column=0, sticky="w", pady=5)
    servicios = obtener_servicios()
    opciones_serv = [f"{s['id_servicio']} - {s['nombre']}" for s in servicios]
    combo_servicios = ttk.Combobox(frame, values=opciones_serv, state="readonly", width=37)
    combo_servicios.grid(row=2, column=1, pady=5)

    # Descripción
    ttk.Label(frame, text="Descripción:").grid(row=3, column=0, sticky="w", pady=5)
    entry_descripcion = ttk.Entry(frame, width=40)
    entry_descripcion.grid(row=3, column=1, pady=5)

    # Fecha de Registro
    ttk.Label(frame, text="Fecha de Registro:").grid(row=4, column=0, sticky="w", pady=5)
    fecha_entry = DateEntry(frame, date_pattern="yyyy-MM-dd")
    fecha_entry.grid(row=4, column=1, pady=5)

    # Estado
    ttk.Label(frame, text="Estado:").grid(row=5, column=0, sticky="w", pady=5)
    estado_var = tk.StringVar()
    estado_combo = ttk.Combobox(
        frame,
        textvariable=estado_var,
        values=["Pendiente", "En Proceso", "Completada"],
        state="readonly",
        width=37
    )
    estado_combo.set("Pendiente")
    estado_combo.grid(row=5, column=1, pady=5)

    def guardar_orden():
        cliente_seleccionado = combo_clientes.get()
        if not cliente_seleccionado:
            messagebox.showerror("Error", "Selecciona un cliente.")
            return
        try:
            id_cliente = int(cliente_seleccionado.split(" - ")[0])
        except ValueError:
            messagebox.showerror("Error", "Cliente inválido.")
            return

        sel_veh = combo_vehiculos.get()
        sel_serv = combo_servicios.get()
        descripcion = entry_descripcion.get().strip()
        fecha_reg = fecha_entry.get_date().strftime("%Y-%m-%d")
        estado = estado_var.get().strip()

        if not sel_veh or not sel_serv or not descripcion:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            id_vehiculo = int(sel_veh.split(" - ")[0])
            id_servicio = int(sel_serv.split(" - ")[0])
        except ValueError:
            messagebox.showerror("Error", "Vehículo o servicio inválido.")
            return

        try:
            nuevo_id = db_registrar_orden_trabajo(
                id_cliente,
                id_vehiculo,
                id_servicio,
                descripcion,
                fecha_reg,
                estado
            )
            messagebox.showinfo("Éxito", f"Orden registrada con ID = {nuevo_id}")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar la orden:\n{e}")

    ttk.Button(frame, text="Registrar Orden", command=guardar_orden).grid(
        row=6, column=0, columnspan=2, pady=20
    )



def asignar_empleado_a_orden_ui():
    ventana = tk.Toplevel()
    ventana.title("Asignar Empleado a Orden")
    ventana.geometry("500x300")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text="Orden (ID - Servicio):").grid(row=0, column=0, sticky="w", pady=5)
    ordenes = obtener_ordenes_con_servicio_y_mecanicos()[1]
    opciones_ord = [f"{fila[0]} - {fila[3]}" for fila in ordenes]
    combo_ordenes = ttk.Combobox(frame, values=opciones_ord, state="readonly", width=45)
    combo_ordenes.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="Mecánico (ID - Nombre):").grid(row=1, column=0, sticky="w", pady=5)
    mecanicos = obtener_mecanicos()
    opciones_mec = [f"{m['id_usuario']} - {m['nombre']} {m['ap_paterno']}" for m in mecanicos]
    combo_mec = ttk.Combobox(frame, values=opciones_mec, state="readonly", width=45)
    combo_mec.grid(row=1, column=1, pady=5)

    def guardar_asignacion():
        sel_ord = combo_ordenes.get()
        sel_mec = combo_mec.get()
        if not sel_ord:
            messagebox.showerror("Error", "Selecciona una orden.")
            return
        if not sel_mec:
            messagebox.showerror("Error", "Selecciona un mecánico.")
            return

        try:
            id_orden = int(sel_ord.split(" - ")[0])
            id_usuario = int(sel_mec.split(" - ")[0])
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos.")
            return

        try:
            db_asignar_empleado_a_orden(id_orden, id_usuario)
            messagebox.showinfo("Éxito", f"Mecánico {id_usuario} asignado a la orden {id_orden}.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo asignar al empleado:\n{e}")

    ttk.Button(frame, text="Asignar Empleado", command=guardar_asignacion).grid(
        row=2, column=0, columnspan=2, pady=20
    )


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

def registrar_vehiculo_empresa_ui():
    ventana = tk.Toplevel()
    ventana.title("Registrar Vehículo de Empresa")
    ventana.geometry("450x400")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")



    ttk.Label(frame, text="Tipo:").grid(row=0, column=0, sticky="w", pady=5)
    entry_tipo = ttk.Entry(frame, width=30)
    entry_tipo.grid(row=0, column=1, pady=5)


    ttk.Label(frame, text="Marca:").grid(row=1, column=0, sticky="w", pady=5)
    entry_marca = ttk.Entry(frame, width=30)
    entry_marca.grid(row=1, column=1, pady=5)


    ttk.Label(frame, text="Modelo:").grid(row=2, column=0, sticky="w", pady=5)
    entry_modelo = ttk.Entry(frame, width=30)
    entry_modelo.grid(row=2, column=1, pady=5)


    ttk.Label(frame, text="Placas (formato ABC-123-D):").grid(row=3, column=0, sticky="w", pady=5)
    entry_placas = ttk.Entry(frame, width=30)
    entry_placas.grid(row=3, column=1, pady=5)

    # Estado (combo con las dos opciones)
    ttk.Label(frame, text="Estado:").grid(row=4, column=0, sticky="w", pady=5)
    estado_var = tk.StringVar()
    combo_estado = ttk.Combobox(
        frame,
        textvariable=estado_var,
        values=["Disponible", "En mantenimiento"],
        state="readonly",
        width=28
    )
    combo_estado.set("Disponible")
    combo_estado.grid(row=4, column=1, pady=5)


    def guardar():
        tipo = entry_tipo.get().strip()
        marca = entry_marca.get().strip()
        modelo = entry_modelo.get().strip()
        placas = entry_placas.get().strip().upper()
        estado = estado_var.get().strip()


        if not (tipo and marca and modelo and placas):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Validar formato de placas
        if not re.fullmatch(r"[A-Z]{3}-\d{3}-[A-Z]", placas):
            messagebox.showerror(
                "Error",
                "Formato de placas inválido.\nDebe ser 3 letras, guion, 3 números, guion, 1 letra.\nEjemplo: ABC-123-D"
            )
            return

        try:

            registrar_vehiculo_empresa(tipo, marca, modelo, placas, estado)
            messagebox.showinfo("Éxito", "Vehículo de empresa registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el vehículo de empresa:\n{e}")

    ttk.Button(frame, text="Registrar Vehículo de Empresa", command=guardar).grid(
        row=5, column=0, columnspan=2, pady=20
    )

def registrar_proveedor_ui():
    ventana = tk.Toplevel()
    ventana.title("Registrar Proveedor")
    ventana.geometry("450x400")
    ventana.configure(bg="#f2f2f2")

    frame = ttk.Frame(ventana, padding=20)
    frame.pack(expand=True, fill="both")


    def validar_telefono(nuevo_valor):
        if nuevo_valor == "":
            return True
        return nuevo_valor.isdigit() and len(nuevo_valor) <= 10

    vcmd_tel = frame.register(validar_telefono)


    ttk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
    entry_nombre = ttk.Entry(frame, width=30)
    entry_nombre.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="Contacto:").grid(row=1, column=0, sticky="w", pady=5)
    entry_contacto = ttk.Entry(frame, width=30)
    entry_contacto.grid(row=1, column=1, pady=5)

    ttk.Label(frame, text="Teléfono:").grid(row=2, column=0, sticky="w", pady=5)
    entry_telefono = ttk.Entry(frame, width=30, validate="key", validatecommand=(vcmd_tel, "%P"))
    entry_telefono.grid(row=2, column=1, pady=5)

    ttk.Label(frame, text="Dirección:").grid(row=3, column=0, sticky="w", pady=5)
    entry_direccion = ttk.Entry(frame, width=30)
    entry_direccion.grid(row=3, column=1, pady=5)


    def guardar():
        nombre   = entry_nombre.get().strip()
        contacto = entry_contacto.get().strip()
        telefono = entry_telefono.get().strip()
        direccion= entry_direccion.get().strip()


        if not (nombre and contacto and telefono and direccion):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not (telefono.isdigit() and len(telefono) == 10):
            messagebox.showerror("Error", "El teléfono debe tener exactamente 10 dígitos.")
            return

        try:

            registrar_proveedor(nombre, contacto, telefono, direccion)
            messagebox.showinfo("Éxito", "Proveedor registrado correctamente.")
            ventana.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el proveedor:\n{e}")

    ttk.Button(frame, text="Registrar Proveedor", command=guardar).grid(
        row=4, column=0, columnspan=2, pady=20
    )

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
        ttk.Button(frame, text="Registrar Orden", command=registrar_orden_trabajo_ui).pack(fill="x", pady=5)
        ttk.Button(frame, text="Registrar Servicio", command=registrar_servicio_ui).pack(fill="x", pady=5)
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
    agregar_usuarios_predeterminados()
    crear_ventana_login()
