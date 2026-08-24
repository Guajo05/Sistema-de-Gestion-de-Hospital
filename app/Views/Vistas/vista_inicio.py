import customtkinter as ctk
from datetime import datetime
from app.controllers.estadistica_controller import EstadisticasController
from app.helpers.chart_embedder import ChartEmbedder
from tkinter import filedialog, messagebox

# ==========================================
# COLORES (reutilizamos los mismos de la vista base)
# ==========================================
BG_COLOR = "#F4F6F9"
CARD_BG = "#FFFFFF"
TEXT_DARK = "#1A2530"
TEXT_LIGHT = "#8A94A6"
ACCENT_BLUE = "#2B71B9"
ACCENT_GREEN = "#28A745"
SHADOW_COLOR = "#D1D5DB"


class VistaInicio(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")

        # Controlador de estadísticas
        self.stats_controller = EstadisticasController()

        # Obtener KPIs y gráficas
        self.kpis = self.stats_controller.obtener_kpis()
        self.figura_evolucion, error1 = self.stats_controller.grafica_barras_consultas_por_mes()
        self.figura_activos, error2 = self.stats_controller.grafica_pastel_activos_inactivos()

        self.crear_contenido()

    def crear_contenido(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        # 3:2 -> el panel derecho gana ancho sin robarle demasiado al izquierdo
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2, minsize=280)

        self.crear_tarjetas_kpi()
        self.crear_seccion_graficas()
        self.crear_panel_derecho()

    # ------------------------------------------------------------
    # TARJETAS KPI
    # ------------------------------------------------------------
    def crear_tarjetas_kpi(self):
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.grid(row=0, column=0, sticky="ew", padx=(0, 15), pady=(0, 10))

        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1, uniform="kpi")

        CARD_SIZE = 140

        datos_tarjetas = [
            ("Citas Hoy", str(self.kpis.get('citas_hoy', 0)), ACCENT_BLUE, 0.7),
            ("Total Pacientes", str(self.kpis.get('total_pacientes', 0)), ACCENT_GREEN, 0.4),
            ("Médicos Activos", str(self.kpis.get('medicos_activos', 0)), ACCENT_BLUE, 0.85),
            ("Ingresos del Día", f"${self.kpis.get('ingresos_dia', 0):,.2f}", ACCENT_GREEN, 0.6)
        ]

        for i, (titulo, valor, color, progreso) in enumerate(datos_tarjetas):
            contenedor = ctk.CTkFrame(
                cards_frame,
                fg_color=SHADOW_COLOR,
                corner_radius=0,
                height=CARD_SIZE
            )
            contenedor.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            contenedor.grid_propagate(False)

            card = ctk.CTkFrame(
                contenedor,
                fg_color=CARD_BG,
                corner_radius=0,
                border_width=1,
                border_color="#E5E8EB"
            )
            card.pack(padx=(0, 5), pady=(0, 5), fill="both", expand=True)

            lbl_icono = ctk.CTkLabel(card, text="●", font=ctk.CTkFont(size=20), text_color=color)
            lbl_icono.pack(pady=(5, 0))

            lbl_titulo = ctk.CTkLabel(
                card, text=titulo,
                font=ctk.CTkFont(family="Roboto", size=12), text_color=TEXT_LIGHT
            )
            lbl_titulo.pack()

            lbl_valor = ctk.CTkLabel(
                card, text=valor,
                font=ctk.CTkFont(family="Roboto", size=20, weight="bold"), text_color=TEXT_DARK
            )
            lbl_valor.pack(pady=(2, 5))

            barra = ctk.CTkProgressBar(card, progress_color=color, fg_color="#E5E8EB", height=4)
            barra.pack(fill="x", padx=15, pady=(0, 8))
            barra.set(progreso)

    # ------------------------------------------------------------
    # GRÁFICAS
    # ------------------------------------------------------------
    def crear_seccion_graficas(self):
        graficas_frame = ctk.CTkFrame(self, fg_color="transparent")
        graficas_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 15), pady=(5, 0))
        graficas_frame.grid_propagate(False)
        graficas_frame.configure(height=230)

        graficas_frame.grid_rowconfigure(0, weight=1)
        graficas_frame.grid_columnconfigure(0, weight=1, uniform="graf")
        graficas_frame.grid_columnconfigure(1, weight=1, uniform="graf")

        if self.figura_evolucion is not None:
            ChartEmbedder.embed_chart(graficas_frame, self.figura_evolucion,
                                       row=0, column=0, sticky="nsew", padx=4, pady=4)
        else:
            ctk.CTkLabel(
                graficas_frame, text="Sin datos de consultas",
                font=ctk.CTkFont(size=12), text_color=TEXT_LIGHT
            ).grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

        if self.figura_activos is not None:
            ChartEmbedder.embed_chart(graficas_frame, self.figura_activos,
                                       row=0, column=1, sticky="nsew", padx=4, pady=4)
        else:
            ctk.CTkLabel(
                graficas_frame, text="Sin datos de pacientes",
                font=ctk.CTkFont(size=12), text_color=TEXT_LIGHT
            ).grid(row=0, column=1, padx=4, pady=4, sticky="nsew")

    # ------------------------------------------------------------
    # ACCIONES DE LOS BOTONES (Acciones Rápidas)
    # ------------------------------------------------------------
    def _obtener_app(self):
        """
        Devuelve la instancia de ModernCareApp (la ventana raíz).
        winfo_toplevel() siempre retorna la ventana CTk de más alto nivel,
        sin importar cuántos frames haya anidados entre VistaInicio y ella.
        Esto evita tener que pasar la referencia de la app manualmente
        por el constructor de cada vista.
        """
        return self.winfo_toplevel()

    def nueva_consulta(self):
        """
        Navega a la vista de Consultas, reutilizando el mismo mecanismo
        que usan los botones del menú lateral (self.cargar_vista).
        """
        app = self._obtener_app()
        if hasattr(app, "cargar_vista"):
            app.cargar_vista("consultas")
        else:
            messagebox.showwarning(
                "Aviso",
                "No se pudo acceder a la ventana principal para cambiar de vista."
            )

    def registro_paciente(self):
        """
        Navega a la vista de Pacientes. Ahí es donde debería vivir el
        formulario de registro (según tu estructura, VistaPacientes ya
        maneja alta/edición de pacientes).
        """
        app = self._obtener_app()
        if hasattr(app, "cargar_vista"):
            app.cargar_vista("pacientes")
        else:
            messagebox.showwarning(
                "Aviso",
                "No se pudo acceder a la ventana principal para cambiar de vista."
            )

    def generar_informe(self):
        # Le pide al usuario dónde guardar (cualquier carpeta de su compu)
        ruta_destino = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivo PDF", "*.pdf")],
            initialfile="Informe_ModernCareClinic.pdf",
            title="Guardar informe como..."
        )

        if not ruta_destino:  # el usuario canceló el diálogo
            return

        exito, mensaje = self.stats_controller.generar_informe_pdf(ruta_destino)

        if exito:
            messagebox.showinfo("Informe generado", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

    # ------------------------------------------------------------
    # PANEL DERECHO (Citas y Acciones Rápidas)
    # ------------------------------------------------------------
    def crear_panel_derecho(self):
        right_panel = ctk.CTkFrame(self, fg_color="transparent")
        right_panel.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(0, 0), pady=(0, 0))

        # Obtener citas reales
        citas = self.stats_controller.obtener_proximas_citas(limite=4)

        # --- Próximas Citas ---
        citas_frame = ctk.CTkFrame(
            right_panel,
            fg_color=CARD_BG,
            corner_radius=10,
            border_width=1,
            border_color="#E5E8EB"
        )
        citas_frame.pack(fill="both", expand=True, pady=(0, 8))

        lbl_citas_titulo = ctk.CTkLabel(
            citas_frame,
            text="Próximas Citas",
            font=ctk.CTkFont(family="Roboto", size=13, weight="bold"),
            text_color="white",
            fg_color="#0D223B",
            corner_radius=6,
            width=70
        )
        lbl_citas_titulo.pack(fill="x", ipady=4, padx=0, pady=0)

        if not citas:
            lbl_sin_citas = ctk.CTkLabel(
                citas_frame,
                text="No hay citas programadas",
                font=ctk.CTkFont(family="Roboto", size=11),
                text_color=TEXT_LIGHT
            )
            lbl_sin_citas.pack(pady=12)
        else:
            for cita in citas:
                fila = ctk.CTkFrame(citas_frame, fg_color="transparent")
                fila.pack(fill="x", padx=8, pady=4)

                ctk.CTkLabel(
                    fila,
                    text=cita['hora'],
                    font=ctk.CTkFont(family="Roboto", size=10, weight="bold"),
                    text_color=TEXT_DARK,
                    width=45
                ).pack(side="left")

                info_frame = ctk.CTkFrame(fila, fg_color="transparent")
                info_frame.pack(side="left", padx=4)
                ctk.CTkLabel(
                    info_frame,
                    text=cita['paciente'],
                    font=ctk.CTkFont(family="Roboto", size=11, weight="bold"),
                    text_color=TEXT_DARK
                ).pack(anchor="w")
                ctk.CTkLabel(
                    info_frame,
                    text=cita['medico'],
                    font=ctk.CTkFont(family="Roboto", size=9),
                    text_color=TEXT_LIGHT
                ).pack(anchor="w")

                estado_lbl = ctk.CTkLabel(
                    fila,
                    text=cita['estado'],
                    font=ctk.CTkFont(family="Roboto", size=9),
                    fg_color=cita['bg_color'],
                    text_color=cita['text_color'],
                    corner_radius=6,
                    width=55,
                    height=18
                )
                estado_lbl.pack(side="right")

                ctk.CTkFrame(citas_frame, height=1, fg_color="#E5E8EB").pack(fill="x", padx=8)

        # --- Acciones Rápidas ---
        acciones_frame = ctk.CTkFrame(
            right_panel,
            fg_color=CARD_BG,
            corner_radius=10,
            border_width=1,
            border_color="#E5E8EB"
        )
        acciones_frame.pack(fill="both", expand=True, pady=(0, 0))

        ctk.CTkLabel(
            acciones_frame,
            text="Acciones Rápidas",
            font=ctk.CTkFont(family="Roboto", size=13, weight="bold"),
            text_color=TEXT_DARK
        ).pack(anchor="w", padx=12, pady=(6, 4))

        # Diccionario: texto del botón -> método que se ejecuta al hacer click.
        # Para agregar una acción nueva en el futuro, solo agregas una línea aquí.
        botones_acciones = {
            "+ Nueva Consulta": self.nueva_consulta,
            "👤 Registro Paciente": self.registro_paciente,
            "📄 Generar Informe": self.generar_informe,
        }

        for btn_text, funcion in botones_acciones.items():
            btn = ctk.CTkButton(
                acciones_frame,
                text=btn_text,
                anchor="w",
                fg_color="#0D223B",
                hover_color=ACCENT_BLUE,
                font=ctk.CTkFont(family="Roboto", size=10),
                corner_radius=5,
                height=26,
                command=funcion
            )
            btn.pack(fill="x", padx=12, pady=2)