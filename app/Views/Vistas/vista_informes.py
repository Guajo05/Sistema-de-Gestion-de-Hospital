import customtkinter as ctk
from tkinter import messagebox
from app.controllers.estadistica_controller import EstadisticasController
from app.helpers.chart_embedder import ChartEmbedder

class VistaInformes(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#F5F6FA")

        self.controller = EstadisticasController()

        self.crear_encabezado()
        self.crear_contenido_principal()

    def crear_encabezado(self):
        header_frame = ctk.CTkFrame(self, fg_color="#F5F6FA")
        header_frame.pack(fill="x", pady=(20, 10), padx=20)

        title_label = ctk.CTkLabel(header_frame, text="Informes Estadísticos",
                                   font=ctk.CTkFont(size=24, weight="bold"), text_color="#0B1A33")
        title_label.pack(side="left")

        subtitle_label = ctk.CTkLabel(header_frame, text="Visualización de datos y métricas del sistema",
                                      font=ctk.CTkFont(size=14), text_color="#6B7280")
        subtitle_label.pack(side="left", padx=(10, 0))

    def crear_contenido_principal(self):
        # Scrollable: si las 3 filas de gráficas no caben en la pantalla,
        # el usuario puede bajar con scroll en vez de que se corten.
        self.graficas_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#F5F6FA",
            scrollbar_button_color="#C7CBD1",
            scrollbar_button_hover_color="#9CA3AF"
        )
        self.graficas_frame.pack(fill="both", expand=True, padx=20, pady=10)

        for j in range(2):
            self.graficas_frame.grid_columnconfigure(j, weight=1, uniform="col")

        self.cargar_graficas()

    def cargar_graficas(self):
        ALTO_CARD = 300  # sube o baja este número para hacer las gráficas más grandes/chicas

        graficas_config = [
            ("Evolución de Consultas", self.controller.grafica_barras_consultas_por_mes, 0, 0),
            ("Pacientes Activos vs Inactivos", self.controller.grafica_pastel_activos_inactivos, 0, 1),
            ("Pacientes por Ciudad", self.controller.grafica_pastel_ciudad, 1, 0),
            ("Pacientes por Tipo de Sangre", self.controller.grafica_barras_tipo_sangre, 1, 1),
            ("Pacientes con vs sin Consultas", self.controller.grafica_pastel_con_sin_consultas, 2, 0),
            ("Top 5 Medicamentos", self.controller.grafica_barras_top_medicamentos, 2, 1),
        ]

        for titulo, metodo, fila, columna in graficas_config:
            card = ctk.CTkFrame(
                self.graficas_frame,
                fg_color="#FFFFFF",
                corner_radius=10,
                border_width=1,
                border_color="#E5E8EB",
                height=ALTO_CARD
            )
            card.grid(row=fila, column=columna, padx=8, pady=8, sticky="nsew")
            card.grid_propagate(False)

            # CLAVE: sin esto, el sticky="nsew" del canvas dentro de la card
            # no tiene efecto porque la card no tiene fila/columna elástica
            # a la cual estirarse. Esto es lo que causaba el corte.
            card.grid_rowconfigure(0, weight=1)
            card.grid_columnconfigure(0, weight=1)

            figura, error = metodo()

            if figura is not None and error is None:
                # Tamaño inicial razonable acorde a la card; luego el canvas
                # se estira solo gracias al weight configurado arriba.
                try:
                    figura.set_size_inches(4.0, 2.6)
                    figura.tight_layout(pad=1.0)
                except Exception:
                    pass

                # embed_chart usa grid(row=0, column=0) por defecto,
                # que es justo donde va dentro de card.
                ChartEmbedder.embed_chart(card, figura, sticky="nsew", padx=8, pady=8)
            else:
                lbl_error = ctk.CTkLabel(
                    card,
                    text=error or f"No hay datos para {titulo}",
                    font=ctk.CTkFont(size=12),
                    text_color="#6B7280"
                )
                lbl_error.grid(row=0, column=0, sticky="nsew", pady=20)