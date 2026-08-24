import customtkinter as ctk
from tkinter import ttk, messagebox
from app.controllers.paciente_controller import PacienteController

class VistaPacientes(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#F5F6FA")

        self.p_controller = PacienteController()
        self.tree = None
        self.pacientes_cargados = []

        self.crear_encabezado()
        self.crear_contenido_principal()

    def crear_encabezado(self):
        header_frame = ctk.CTkFrame(self, fg_color="#F5F6FA")
        header_frame.pack(fill="x", pady=(20, 10), padx=20)

        title_label = ctk.CTkLabel(header_frame, text="Gestión de Pacientes",
                                   font=ctk.CTkFont(size=24, weight="bold"), text_color="#0B1A33")
        title_label.pack(side="left")

        add_btn = ctk.CTkButton(header_frame, text="+ Añadir Nuevo Paciente",
                                fg_color="#1E3A5F", text_color="white", corner_radius=8, width=200,
                                command=lambda: self.mostrar_formulario(None))
        add_btn.pack(side="right")

    def crear_contenido_principal(self):
        self.content_frame = ctk.CTkFrame(self, fg_color="#F5F6FA")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.mostrar_tabla()

    # ------------------- HELPERS -------------------
    def mostrar_alerta(self, mensaje: str, es_error: bool):
        if mensaje is None:
            return
        if es_error:
            messagebox.showerror("Aviso", mensaje)
        else:
            messagebox.showinfo("Aviso", mensaje)

    def obtener_paciente_seleccionado(self):
        if self.tree is None:
            return None
        seleccion = self.tree.selection()
        if not seleccion:
            self.mostrar_alerta("SELECCIONA UN PACIENTE DE LA TABLA PRIMERO.❎", es_error=True)
            return None
        paciente_id = int(seleccion[0])
        return next((p for p in self.pacientes_cargados if p.id == paciente_id), None)

    # ------------------- TABLA CON ESTILOS MEJORADOS -------------------
    def mostrar_tabla(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        pacientes, mensaje = self.p_controller.mostrar_pacientes()

        if not pacientes:
            self.pacientes_cargados = []
            self.mostrar_alerta(mensaje, es_error=True)
            no_data_label = ctk.CTkLabel(self.content_frame, text="No hay pacientes registrados",
                                         font=ctk.CTkFont(size=18, weight="bold"),
                                         text_color="red")
            no_data_label.pack(pady=50)
            return

        self.pacientes_cargados = pacientes

        table_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=10)
        table_frame.pack(fill="both", expand=True)

        # ===================== ESTILOS PERSONALIZADOS =====================
        style = ttk.Style()
        style.theme_use("clam")  # 'clam' permite personalizar colores de fondo

        # Estilo para el encabezado (fondo #0D223B, texto blanco, fuente más grande)
        style.configure(
            "Pacientes.Treeview.Heading",
            font=("Roboto", 13, "bold"),
            background="#0D223B",
            foreground="white",
            fieldbackground="#0D223B",
            borderwidth=0
        )

        # Estilo para las filas (fuente más grande, altura mayor)
        style.configure(
            "Pacientes.Treeview",
            font=("Roboto", 12),
            rowheight=32,
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground="#1A2530"
        )

        # Color al seleccionar una fila
        style.map(
            "Pacientes.Treeview",
            background=[("selected", "#2B71B9")],
            foreground=[("selected", "white")]
        )

        columns = ("ID", "Nombre Completo", "Edad", "Ciudad", "Sangre")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10,
            style="Pacientes.Treeview"  # Aplica el estilo personalizado
        )

        # Configurar columnas (ancho ajustado)
        self.tree.column("ID", anchor="center", width=80)
        self.tree.column("Nombre Completo", anchor="center", width=250)
        self.tree.column("Edad", anchor="center", width=100)
        self.tree.column("Ciudad", anchor="center", width=150)
        self.tree.column("Sangre", anchor="center", width=100)

        for col in columns:
            self.tree.heading(col, text=col)

        for paciente in pacientes:
            self.tree.insert("", "end", iid=str(paciente.id),
                        values=(paciente.id, paciente.nombre, paciente.edad,
                                paciente.ciudad, paciente.sangre))

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones de acción (sin cambios)
        action_frame = ctk.CTkFrame(self.content_frame, fg_color="#F5F6FA")
        action_frame.pack(pady=10)

        def eliminar_paciente():
            paciente = self.obtener_paciente_seleccionado()
            if paciente is None:
                return

            confirmado = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Seguro que deseas eliminar al paciente '{paciente.nombre}'?"
            )
            if not confirmado:
                return

            resultado, mensaje = self.p_controller.eliminar_paciente(paciente.id)
            self.mostrar_alerta(mensaje, es_error=not resultado)

            if resultado:
                self.mostrar_tabla()

        def actualizar_paciente():
            paciente = self.obtener_paciente_seleccionado()
            if paciente is None:
                return
            self.mostrar_formulario(paciente)

        eliminar_btn = ctk.CTkButton(action_frame, text="🗑️ Eliminar", fg_color="red",
                                     text_color="white", corner_radius=8,
                                     command=eliminar_paciente)
        eliminar_btn.pack(side="left", padx=10)

        actualizar_btn = ctk.CTkButton(action_frame, text="✏️ Actualizar", fg_color="#1E3A5F",
                                       text_color="white", corner_radius=8,
                                       command=actualizar_paciente)
        actualizar_btn.pack(side="left", padx=10)

    # ------------------- FORMULARIO (sin cambios) -------------------
    def mostrar_formulario(self, paciente=None):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        modo_edicion = paciente is not None

        form_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        titulo = "Actualizar Paciente" if modo_edicion else "Registrar Nuevo Paciente"
        ctk.CTkLabel(form_frame, text=titulo,
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        nombre_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Nombre Completo")
        nombre_entry.pack(pady=10)
        edad_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Edad")
        edad_entry.pack(pady=10)
        ciudad_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Ciudad")
        ciudad_entry.pack(pady=10)
        sangre_combo = ctk.CTkComboBox(form_frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        sangre_combo.pack(pady=10)

        if modo_edicion:
            nombre_entry.insert(0, paciente.nombre)
            edad_entry.insert(0, str(paciente.edad))
            ciudad_entry.insert(0, paciente.ciudad)
            sangre_combo.set(paciente.sangre)
        else:
            sangre_combo.set("A+")

        button_frame = ctk.CTkFrame(form_frame, fg_color="#FFFFFF")
        button_frame.pack(pady=20)

        def guardar_paciente():
            datos = {
                "nombre": nombre_entry.get(),
                "edad": edad_entry.get(),
                "ciudad": ciudad_entry.get(),
                "sangre": sangre_combo.get()
            }

            if modo_edicion:
                datos["id"] = paciente.id
                resultado, mensaje = self.p_controller.actualizar_paciente(datos)
            else:
                resultado, mensaje = self.p_controller.registrar_paciente(datos)

            es_error = resultado is None
            self.mostrar_alerta(mensaje, es_error=es_error)

            if not es_error:
                self.mostrar_tabla()

        guardar_btn = ctk.CTkButton(button_frame, text="Guardar", fg_color="#1E3A5F",
                                    text_color="white", corner_radius=8,
                                    command=guardar_paciente)
        guardar_btn.pack(side="left", padx=10)

        cancelar_btn = ctk.CTkButton(button_frame, text="Cancelar", fg_color="gray",
                                     text_color="white", corner_radius=8,
                                     command=self.mostrar_tabla)
        cancelar_btn.pack(side="left", padx=10)