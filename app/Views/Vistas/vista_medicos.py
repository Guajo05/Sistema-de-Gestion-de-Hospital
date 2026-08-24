import customtkinter as ctk
from tkinter import ttk, messagebox
from app.controllers.medico_controller import MedicoController

class VistaMedicos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#F5F6FA")

        self.controller = MedicoController()
        self.tree = None
        self.medicos_cargados = []

        self.crear_encabezado()
        self.crear_contenido_principal()

    def crear_encabezado(self):
        header_frame = ctk.CTkFrame(self, fg_color="#F5F6FA")
        header_frame.pack(fill="x", pady=(20, 10), padx=20)

        title_label = ctk.CTkLabel(header_frame, text="Gestión de Médicos",
                                   font=ctk.CTkFont(size=24, weight="bold"), text_color="#0B1A33")
        title_label.pack(side="left")

        subtitle_label = ctk.CTkLabel(header_frame, text="Buscar, editar o registrar médicos",
                                      font=ctk.CTkFont(size=14), text_color="#6B7280")
        subtitle_label.pack(side="left", padx=(10, 0))

        add_btn = ctk.CTkButton(header_frame, text="+ Registrar Nuevo Médico",
                                fg_color="#1E3A5F", text_color="white", corner_radius=8, width=220,
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

    def obtener_medico_seleccionado(self):
        if self.tree is None:
            return None
        seleccion = self.tree.selection()
        if not seleccion:
            self.mostrar_alerta("SELECCIONA UN MÉDICO DE LA TABLA PRIMERO.❎", es_error=True)
            return None
        medico_id = int(seleccion[0])
        return next((m for m in self.medicos_cargados if m.id == medico_id), None)

    # ------------------- TABLA -------------------
    def mostrar_tabla(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        table_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=10)
        table_frame.pack(fill="both", expand=True)

        # ===================== ESTILOS PERSONALIZADOS =====================
        style = ttk.Style()
        style.theme_use("clam")

        # Encabezado: fondo #0D223B, texto blanco, fuente más grande
        style.configure(
            "Medicos.Treeview.Heading",
            font=("Roboto", 13, "bold"),
            background="#0D223B",
            foreground="white",
            fieldbackground="#0D223B",
            borderwidth=0
        )

        # Filas: fuente más grande y mayor altura
        style.configure(
            "Medicos.Treeview",
            font=("Roboto", 12),
            rowheight=32,
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground="#1A2530"
        )

        # Selección de fila
        style.map(
            "Medicos.Treeview",
            background=[("selected", "#2B71B9")],
            foreground=[("selected", "white")]
        )

        # Columnas: eliminamos "Acciones"
        columns = ("ID", "Nombre", "Especialidad", "Salario", "Turno")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10,
            style="Medicos.Treeview"
        )

        # Anchos de columna ajustados
        self.tree.column("ID", anchor="center", width=80)
        self.tree.column("Nombre", anchor="center", width=200)
        self.tree.column("Especialidad", anchor="center", width=180)
        self.tree.column("Salario", anchor="center", width=150)
        self.tree.column("Turno", anchor="center", width=120)

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones de acción (debajo de la tabla)
        action_frame = ctk.CTkFrame(self.content_frame, fg_color="#F5F6FA")
        action_frame.pack(pady=10)

        def eliminar_medico():
            medico = self.obtener_medico_seleccionado()
            if medico is None:
                return

            confirmado = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Seguro que deseas eliminar al médico '{medico.nombre}'?"
            )
            if not confirmado:
                return

            exito, mensaje = self.controller.eliminar_medico(medico.id)
            self.mostrar_alerta(mensaje, es_error=not exito)

            if exito:
                self.mostrar_tabla()

        def actualizar_medico():
            medico = self.obtener_medico_seleccionado()
            if medico is None:
                return
            self.mostrar_formulario(medico)

        eliminar_btn = ctk.CTkButton(action_frame, text="🗑️ Eliminar", fg_color="red",
                                     text_color="white", corner_radius=8,
                                     command=eliminar_medico)
        eliminar_btn.pack(side="left", padx=10)

        actualizar_btn = ctk.CTkButton(action_frame, text="✏️ Actualizar", fg_color="#1E3A5F",
                                       text_color="white", corner_radius=8,
                                       command=actualizar_medico)
        actualizar_btn.pack(side="left", padx=10)

        self.cargar_medicos()

    def cargar_medicos(self):
        medicos, mensaje = self.controller.mostrar_medicos()

        self.tree.delete(*self.tree.get_children())

        if medicos is None:
            self.medicos_cargados = []
            self.mostrar_alerta(mensaje, es_error=True)
            return

        self.medicos_cargados = medicos
        for medico in medicos:
            self.tree.insert("", "end", iid=str(medico.id),
                        values=(medico.id, medico.nombre, medico.especialidad,
                                medico.salario, medico.turno))

    # ------------------- FORMULARIO (sin cambios) -------------------
    def mostrar_formulario(self, medico=None):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        modo_edicion = medico is not None

        form_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        titulo = "Editar Médico" if modo_edicion else "Registrar Nuevo Médico"
        ctk.CTkLabel(form_frame, text=titulo,
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        nombre_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Nombre Completo")
        nombre_entry.pack(pady=10)

        especialidad_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Especialidad")
        especialidad_entry.pack(pady=10)

        salario_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Salario")
        salario_entry.pack(pady=10)

        turno_combo = ctk.CTkComboBox(form_frame, values=["Mañana", "Tarde", "Noche"])
        turno_combo.pack(pady=10)

        if modo_edicion:
            nombre_entry.insert(0, medico.nombre)
            especialidad_entry.insert(0, medico.especialidad)
            salario_entry.insert(0, str(medico.salario))
            turno_combo.set(medico.turno)
        else:
            turno_combo.set("Mañana")

        button_frame = ctk.CTkFrame(form_frame, fg_color="#FFFFFF")
        button_frame.pack(pady=20)

        def guardar_medico():
            datos = {
                "nombre": nombre_entry.get(),
                "especialidad": especialidad_entry.get(),
                "salario": salario_entry.get(),
                "turno": turno_combo.get(),
            }

            if modo_edicion:
                datos["id"] = medico.id
                resultado, mensaje = self.controller.actualizar_medico(datos)
            else:
                resultado, mensaje = self.controller.registrar_medico(datos)

            es_error = resultado is None
            self.mostrar_alerta(mensaje, es_error=es_error)

            if resultado is not None:
                self.mostrar_tabla()

        guardar_btn = ctk.CTkButton(button_frame, text="Guardar Cambios" if modo_edicion else "Guardar Médico",
                                    fg_color="#1E3A5F", text_color="white", corner_radius=8,
                                    command=guardar_medico)
        guardar_btn.pack(side="left", padx=10)

        cancelar_btn = ctk.CTkButton(button_frame, text="Cancelar", fg_color="gray",
                                     text_color="white", corner_radius=8,
                                     command=self.mostrar_tabla)
        cancelar_btn.pack(side="left", padx=10)