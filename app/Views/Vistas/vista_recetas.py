import customtkinter as ctk
from tkinter import ttk, messagebox
from app.controllers.receta_controller import RecetaController
from app.controllers.consulta_controller import ConsultaController
from app.controllers.medicamento_controller import MedicamentoController

class VistaRecetas(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#F5F6FA")

        self.controller = RecetaController()
        self.consulta_controller = ConsultaController()
        self.medicamento_controller = MedicamentoController()
        self.tree = None
        self.recetas_cargadas = []

        self.crear_encabezado()
        self.crear_contenido_principal()

    def crear_encabezado(self):
        header_frame = ctk.CTkFrame(self, fg_color="#F5F6FA")
        header_frame.pack(fill="x", pady=(20, 10), padx=20)

        title_label = ctk.CTkLabel(header_frame, text="Gestión de Recetas",
                                   font=ctk.CTkFont(size=24, weight="bold"), text_color="#0B1A33")
        title_label.pack(side="left")

        subtitle_label = ctk.CTkLabel(header_frame, text="Registrar, actualizar o eliminar recetas",
                                      font=ctk.CTkFont(size=14), text_color="#6B7280")
        subtitle_label.pack(side="left", padx=(10, 0))

        add_btn = ctk.CTkButton(header_frame, text="+ Registrar Nueva Receta",
                                fg_color="#1E3A5F", text_color="white", corner_radius=8, width=250,
                                command=self.mostrar_formulario)
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

    def obtener_receta_seleccionada(self):
        if self.tree is None:
            return None
        seleccion = self.tree.selection()
        if not seleccion:
            self.mostrar_alerta("SELECCIONA UNA RECETA DE LA TABLA PRIMERO.❎", es_error=True)
            return None
        receta_id = int(seleccion[0])
        return next((r for r in self.recetas_cargadas if r.id == receta_id), None)

    # ------------------- TABLA CON ESTILOS -------------------
    def mostrar_tabla(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        recetas, mensaje = self.controller.mostrar_recetas()

        if not recetas:
            self.recetas_cargadas = []
            self.mostrar_alerta(mensaje, es_error=True)
            no_data_label = ctk.CTkLabel(self.content_frame, text=mensaje or "No hay recetas registradas",
                                         font=ctk.CTkFont(size=18, weight="bold"),
                                         text_color="red")
            no_data_label.pack(pady=50)
            return

        self.recetas_cargadas = recetas

        table_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=10)
        table_frame.pack(fill="both", expand=True)

        # Estilos
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Recetas.Treeview.Heading",
            font=("Roboto", 13, "bold"),
            background="#0D223B",
            foreground="white",
            fieldbackground="#0D223B",
            borderwidth=0
        )
        style.configure(
            "Recetas.Treeview",
            font=("Roboto", 12),
            rowheight=32,
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground="#1A2530"
        )
        style.map(
            "Recetas.Treeview",
            background=[("selected", "#2B71B9")],
            foreground=[("selected", "white")]
        )

        columns = ("ID Receta", "Medicamento", "Consulta", "Cantidad", "Dosis", "Días")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10,
            style="Recetas.Treeview"
        )

        self.tree.column("ID Receta", anchor="center", width=100)
        self.tree.column("Medicamento", anchor="center", width=200)
        self.tree.column("Consulta", anchor="center", width=150)
        self.tree.column("Cantidad", anchor="center", width=100)
        self.tree.column("Dosis", anchor="center", width=200)
        self.tree.column("Días", anchor="center", width=100)

        for col in columns:
            self.tree.heading(col, text=col)

        for receta in recetas:
            self.tree.insert("", "end", iid=str(receta.id),
                        values=(receta.id, receta.medicamento.nombre, receta.consulta.id,
                                receta.cantidad, receta.dosis, receta.dias))

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones de acción
        action_frame = ctk.CTkFrame(self.content_frame, fg_color="#F5F6FA")
        action_frame.pack(pady=10)

        def eliminar_receta():
            receta = self.obtener_receta_seleccionada()
            if receta is None:
                return

            confirmado = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Seguro que deseas eliminar la receta #{receta.id}?"
            )
            if not confirmado:
                return

            exito, mensaje = self.controller.eliminar_receta(receta.id)
            self.mostrar_alerta(mensaje, es_error=not exito)

            if exito:
                self.mostrar_tabla()

        def actualizar_receta():
            receta = self.obtener_receta_seleccionada()
            if receta is None:
                return
            self.mostrar_formulario(receta)

        eliminar_btn = ctk.CTkButton(action_frame, text="🗑️ Eliminar", fg_color="red",
                                     text_color="white", corner_radius=8,
                                     command=eliminar_receta)
        eliminar_btn.pack(side="left", padx=10)

        actualizar_btn = ctk.CTkButton(action_frame, text="✏️ Actualizar", fg_color="#1E3A5F",
                                       text_color="white", corner_radius=8,
                                       command=actualizar_receta)
        actualizar_btn.pack(side="left", padx=10)

    # ------------------- FORMULARIO EN PARALELO -------------------
    def mostrar_formulario(self, receta=None):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        modo_edicion = receta is not None

        form_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        titulo = "Editar Receta" if modo_edicion else "Registrar Nueva Receta"
        ctk.CTkLabel(form_frame, text=titulo,
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        # Cargar combos
        medicamentos, mensaje_medicamentos = self.medicamento_controller.mostrar_medicamentos()
        consultas, mensaje_consultas = self.consulta_controller.mostrar_consultas()

        if not medicamentos:
            self.mostrar_alerta(mensaje_medicamentos or "NO HAY MEDICAMENTOS REGISTRADOS.❎", es_error=True)
            self.mostrar_tabla()
            return

        if not consultas:
            self.mostrar_alerta(mensaje_consultas or "NO HAY CONSULTAS REGISTRADAS.❎", es_error=True)
            self.mostrar_tabla()
            return

        medicamentos_map = {f"{m.id} - {m.nombre}": m.id for m in medicamentos}
        consultas_map = {f"{c.id} - {c.paciente}": c.id for c in consultas}

        # ========== FILA 1: Medicamento y Consulta en paralelo ==========
        fila1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        fila1.pack(pady=5, fill="x")

        # Medicamento
        frame_med = ctk.CTkFrame(fila1, fg_color="transparent")
        frame_med.pack(side="left", padx=10, expand=True, fill="x")
        ctk.CTkLabel(frame_med, text="Medicamento:", font=ctk.CTkFont(size=14)).pack(anchor="w")
        medicamento_combo = ctk.CTkComboBox(frame_med, values=list(medicamentos_map.keys()), width=300)
        medicamento_combo.pack(pady=5, fill="x")

        # Consulta
        frame_con = ctk.CTkFrame(fila1, fg_color="transparent")
        frame_con.pack(side="left", padx=10, expand=True, fill="x")
        ctk.CTkLabel(frame_con, text="Consulta:", font=ctk.CTkFont(size=14)).pack(anchor="w")
        consulta_combo = ctk.CTkComboBox(frame_con, values=list(consultas_map.keys()), width=300)
        consulta_combo.pack(pady=5, fill="x")

        # ========== FILA 2: Cantidad, Dosis, Días en paralelo ==========
        fila2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        fila2.pack(pady=5, fill="x")

        # Cantidad
        frame_cant = ctk.CTkFrame(fila2, fg_color="transparent")
        frame_cant.pack(side="left", padx=10, expand=True, fill="x")
        ctk.CTkLabel(frame_cant, text="Cantidad:", font=ctk.CTkFont(size=14)).pack(anchor="w")
        cantidad_entry = ctk.CTkEntry(frame_cant, placeholder_text="Cantidad", width=150)
        cantidad_entry.pack(pady=5, fill="x")

        # Dosis
        frame_dosis = ctk.CTkFrame(fila2, fg_color="transparent")
        frame_dosis.pack(side="left", padx=10, expand=True, fill="x")
        ctk.CTkLabel(frame_dosis, text="Dosis:", font=ctk.CTkFont(size=14)).pack(anchor="w")
        dosis_entry = ctk.CTkEntry(frame_dosis, placeholder_text="Ej: 500 mg cada 8 horas", width=200)
        dosis_entry.pack(pady=5, fill="x")

        # Días
        frame_dias = ctk.CTkFrame(fila2, fg_color="transparent")
        frame_dias.pack(side="left", padx=10, expand=True, fill="x")
        ctk.CTkLabel(frame_dias, text="Días:", font=ctk.CTkFont(size=14)).pack(anchor="w")
        dias_entry = ctk.CTkEntry(frame_dias, placeholder_text="Días de tratamiento", width=100)
        dias_entry.pack(pady=5, fill="x")

        # Si es edición, precargar datos
        if modo_edicion:
            medicamento_combo.set(f"{receta.medicamento.id} - {receta.medicamento.nombre}")
            consulta_combo.set(f"{receta.consulta.id} - {receta.consulta.paciente}")
            cantidad_entry.insert(0, str(receta.cantidad))
            dosis_entry.insert(0, receta.dosis)
            dias_entry.insert(0, str(receta.dias))

        # ========== BOTONES ==========
        button_frame = ctk.CTkFrame(form_frame, fg_color="#FFFFFF")
        button_frame.pack(pady=20)

        def guardar_receta():
            medicamento_sel = medicamento_combo.get()
            consulta_sel = consulta_combo.get()
            cantidad = cantidad_entry.get().strip()
            dosis = dosis_entry.get().strip()
            dias = dias_entry.get().strip()

            if not medicamento_sel or not consulta_sel or not cantidad or not dosis or not dias:
                self.mostrar_alerta("TODOS LOS CAMPOS SON OBLIGATORIOS.❎", es_error=True)
                return

            datos = {
                "medicamento": medicamentos_map[medicamento_sel],
                "consulta": consultas_map[consulta_sel],
                "cantidad": cantidad,
                "dosis": dosis,
                "dias": dias,
            }

            if modo_edicion:
                datos["id"] = receta.id
                resultado, mensaje = self.controller.actualizar_receta(datos)
            else:
                resultado, mensaje = self.controller.registrar_receta(datos)

            es_error = resultado is None
            self.mostrar_alerta(mensaje, es_error=es_error)

            if not es_error:
                self.mostrar_tabla()

        guardar_btn = ctk.CTkButton(button_frame, text="Guardar Cambios" if modo_edicion else "Guardar Receta",
                                    fg_color="#1E3A5F", text_color="white", corner_radius=8,
                                    command=guardar_receta)
        guardar_btn.pack(side="left", padx=10)

        cancelar_btn = ctk.CTkButton(button_frame, text="Cancelar", fg_color="gray",
                                     text_color="white", corner_radius=8,
                                     command=self.mostrar_tabla)
        cancelar_btn.pack(side="left", padx=10)