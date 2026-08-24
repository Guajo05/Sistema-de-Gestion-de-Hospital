import customtkinter as ctk
from tkinter import ttk, messagebox
from app.controllers.consulta_controller import ConsultaController
from app.controllers.medico_controller import MedicoController
from app.controllers.paciente_controller import PacienteController

class VistaConsultas(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#F5F6FA")

        self.controller = ConsultaController()
        self.medico_controller = MedicoController()
        self.paciente_controller = PacienteController()
        self.tree = None
        self.consultas_cargadas = []

        self.crear_encabezado()
        self.crear_contenido_principal()

    def crear_encabezado(self):
        header_frame = ctk.CTkFrame(self, fg_color="#F5F6FA")
        header_frame.pack(fill="x", pady=(20, 10), padx=20)

        title_label = ctk.CTkLabel(header_frame, text="Gestión de Consultas",
                                   font=ctk.CTkFont(size=24, weight="bold"), text_color="#0B1A33")
        title_label.pack(side="left")

        subtitle_label = ctk.CTkLabel(header_frame, text="Buscar, visualizar o registrar consultas",
                                      font=ctk.CTkFont(size=14), text_color="#6B7280")
        subtitle_label.pack(side="left", padx=(10, 0))

        add_btn = ctk.CTkButton(header_frame, text="+ Registrar Nueva Consulta",
                                fg_color="#1E3A5F", text_color="white", corner_radius=8, width=220,
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

    def es_mensaje_error(self, mensaje: str) -> bool:
        return mensaje is not None and "❎" in mensaje

    def pintar_consultas(self, consultas):
        self.consultas_cargadas = consultas
        self.tree.delete(*self.tree.get_children())
        for consulta in consultas:
            self.tree.insert("", "end", iid=str(consulta.id),
                        values=(consulta.id, consulta.paciente, consulta.medico,
                                f"${consulta.costo}", consulta.fecha))

    # ------------------- TABLA CON ESTILOS MEJORADOS -------------------
    def mostrar_tabla(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Barra de búsqueda (sin cambios)
        search_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=10)
        search_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(search_frame, text="Fecha Inicio (AAAA-MM-DD)").pack(side="left", padx=10, pady=10)
        self.fecha_inicio = ctk.CTkEntry(search_frame, width=150, placeholder_text="2023-10-01")
        self.fecha_inicio.pack(side="left", padx=5)

        ctk.CTkLabel(search_frame, text="Fecha Fin (AAAA-MM-DD)").pack(side="left", padx=10, pady=10)
        self.fecha_fin = ctk.CTkEntry(search_frame, width=150, placeholder_text="2023-10-31")
        self.fecha_fin.pack(side="left", padx=5)

        def buscar_por_fecha():
            fechas = {"inicio": self.fecha_inicio.get().strip(), "final": self.fecha_fin.get().strip()}

            if not fechas["inicio"] or not fechas["final"]:
                self.mostrar_alerta("DEBES INGRESAR AMBAS FECHAS.❎", es_error=True)
                return

            consultas, mensaje = self.controller.buscar_consultas(fechas)

            if consultas is None:
                self.mostrar_alerta(mensaje, es_error=True)
                self.tree.delete(*self.tree.get_children())
                return

            self.pintar_consultas(consultas)

        buscar_btn = ctk.CTkButton(search_frame, text="🔍 Buscar Consultas",
                                   fg_color="#1E3A5F", text_color="white", corner_radius=8, width=200,
                                   command=buscar_por_fecha)
        buscar_btn.pack(side="right", padx=20)

        # ---- Tabla con estilos ----
        table_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=10)
        table_frame.pack(fill="both", expand=True)

        # ===================== ESTILOS PERSONALIZADOS =====================
        style = ttk.Style()
        style.theme_use("clam")

        # Encabezado: fondo #0D223B, texto blanco, fuente más grande
        style.configure(
            "Consultas.Treeview.Heading",
            font=("Roboto", 13, "bold"),
            background="#0D223B",
            foreground="white",
            fieldbackground="#0D223B",
            borderwidth=0
        )

        # Filas: fuente más grande y mayor altura
        style.configure(
            "Consultas.Treeview",
            font=("Roboto", 12),
            rowheight=32,
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground="#1A2530"
        )

        # Selección de fila
        style.map(
            "Consultas.Treeview",
            background=[("selected", "#2B71B9")],
            foreground=[("selected", "white")]
        )

        columns = ("ID Consulta", "Paciente", "Médico", "Costo", "Fecha")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10,
            style="Consultas.Treeview"
        )

        # Anchos de columna ajustados
        self.tree.column("ID Consulta", anchor="center", width=120)
        self.tree.column("Paciente", anchor="center", width=200)
        self.tree.column("Médico", anchor="center", width=200)
        self.tree.column("Costo", anchor="center", width=120)
        self.tree.column("Fecha", anchor="center", width=150)

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_consultas()

    def cargar_consultas(self):
        consultas, mensaje = self.controller.mostrar_consultas()

        self.tree.delete(*self.tree.get_children())

        if consultas is None:
            self.mostrar_alerta(mensaje, es_error=True)
            return

        self.pintar_consultas(consultas)

    # ------------------- FORMULARIO (sin cambios) -------------------
    def mostrar_formulario(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        form_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(form_frame, text="Registrar Nueva Consulta",
            font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        pacientes, mensaje_pacientes = self.paciente_controller.mostrar_pacientes()
        medicos, mensaje_medicos = self.medico_controller.mostrar_medicos()

        if not pacientes:
            self.mostrar_alerta(mensaje_pacientes or "NO HAY PACIENTES REGISTRADOS.❎", es_error=True)
            self.mostrar_tabla()
            return

        if not medicos:
            self.mostrar_alerta(mensaje_medicos or "NO HAY MEDICOS REGISTRADOS.❎", es_error=True)
            self.mostrar_tabla()
            return

        pacientes_map = {f"{p.id} - {p.nombre}": p.id for p in pacientes}
        medicos_map = {f"{m.id} - {m.nombre}": m.id for m in medicos}

        # --- Frame para los combos en paralelo ---
        combos_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        combos_frame.pack(pady=10, fill="x")

        # Columna izquierda: Paciente
        paciente_frame = ctk.CTkFrame(combos_frame, fg_color="transparent")
        paciente_frame.pack(side="left", padx=10, expand=True, fill="x")

        ctk.CTkLabel(paciente_frame, text="Paciente", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        paciente_combo = ctk.CTkComboBox(paciente_frame, values=list(pacientes_map.keys()), width=300)
        paciente_combo.pack(pady=5, fill="x")

        # Columna derecha: Médico
        medico_frame = ctk.CTkFrame(combos_frame, fg_color="transparent")
        medico_frame.pack(side="left", padx=10, expand=True, fill="x")

        ctk.CTkLabel(medico_frame, text="Médico", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        medico_combo = ctk.CTkComboBox(medico_frame, values=list(medicos_map.keys()), width=300)
        medico_combo.pack(pady=5, fill="x")

        # --- Resto de campos (fecha, diagnóstico, costo) en columna central ---
        campos_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        campos_frame.pack(pady=10, fill="x")

        fecha_entry = ctk.CTkEntry(campos_frame, width=400, placeholder_text="Fecha (AAAA-MM-DD)")
        fecha_entry.pack(pady=5, anchor="center")

        diagnostico_entry = ctk.CTkEntry(campos_frame, width=400, placeholder_text="Diagnóstico")
        diagnostico_entry.pack(pady=5, anchor="center")

        costo_entry = ctk.CTkEntry(campos_frame, width=400, placeholder_text="Costo")
        costo_entry.pack(pady=5, anchor="center")

        # --- Botones ---
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=30)

        def guardar_consulta():
            paciente_sel = paciente_combo.get()
            medico_sel = medico_combo.get()
            fecha = fecha_entry.get().strip()
            diagnostico = diagnostico_entry.get().strip()
            costo_texto = costo_entry.get().strip()

            if not paciente_sel or not medico_sel or not fecha or not diagnostico or not costo_texto:
                self.mostrar_alerta("TODOS LOS CAMPOS SON OBLIGATORIOS.❎", es_error=True)
                return

            try:
                costo = float(costo_texto)
            except ValueError:
                self.mostrar_alerta("EL COSTO DEBE SER UN NÚMERO.❎", es_error=True)
                return

            datos = {
                "paciente": pacientes_map[paciente_sel],
                "medico": medicos_map[medico_sel],
                "fecha": fecha,
                "diagnostico": diagnostico,
                "costo": costo,}

            resultado, mensaje = self.controller.registrar_consulta(datos)
            error = self.es_mensaje_error(mensaje)
            self.mostrar_alerta(mensaje, es_error=error)

            if not error:
                self.mostrar_tabla()

        guardar_btn = ctk.CTkButton(button_frame, text="Guardar Consulta", fg_color="#1E3A5F",
                                text_color="white", corner_radius=8, width=150,
                                command=guardar_consulta)
        guardar_btn.pack(side="left", padx=10)

        cancelar_btn = ctk.CTkButton(button_frame, text="Cancelar", fg_color="gray",
                                 text_color="white", corner_radius=8, width=150,
                                 command=self.mostrar_tabla)
        cancelar_btn.pack(side="left", padx=10)