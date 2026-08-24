import customtkinter as ctk
from datetime import datetime
from PIL import Image
import os

# Importar todas las vistas
from app.Views.Vistas.vista_pacientes import VistaPacientes
from app.Views.Vistas.vista_consultas import VistaConsultas
from app.Views.Vistas.vista_medicos import VistaMedicos
from app.Views.Vistas.vista_medicamentos import VistaMedicamentos
from app.Views.Vistas.vista_recetas import VistaRecetas
from app.Views.Vistas.vista_informes import VistaInformes
from app.Views.Vistas.vista_inicio import VistaInicio

# ==========================================
# CONFIGURACIÓN GENERAL Y COLORES
# ==========================================
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

BG_COLOR = "#F4F6F9"
SIDEBAR_COLOR = "#0D223B"
CARD_BG = "#FFFFFF"
TEXT_DARK = "#1A2530"
TEXT_LIGHT = "#8A94A6"
ACCENT_BLUE = "#2B71B9"
ACCENT_GREEN = "#28A745"
SHADOW_COLOR = "#D1D5DB"


class ModernCareApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestión Hospitalaria - Modern Care")
        self.geometry("1150x700")
        self.configure(fg_color=BG_COLOR)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Cargar imágenes
        self.base_dir = os.getcwd()
        self.assets_dir = os.path.join(self.base_dir, "app", "assets")
        self.icons = self.cargar_iconos()
        self.logo_img = self.cargar_logo()

        # Para controlar el botón activo en el menú
        self.boton_activo = None

        self.crear_menu_lateral()
        self.crear_contenido_principal()

        # Cargar la vista por defecto
        self.cargar_vista("inicio")

    # ------------------------------------------------------------
    # CARGA DE IMÁGENES
    # ------------------------------------------------------------
    def cargar_imagen(self, ruta_relativa, tamaño=(24, 24)):
        ruta = os.path.join(self.assets_dir, ruta_relativa)
        if not os.path.exists(ruta):
            return None
        try:
            img = Image.open(ruta)
            img = img.resize(tamaño, Image.LANCZOS)
            return ctk.CTkImage(light_image=img, dark_image=img, size=tamaño)
        except Exception:
            return None

    def cargar_iconos(self):
        nombres = [
            ("inicio", "icons/Icono Inicio.png"),
            ("pacientes", "icons/Icono Paciente.png"),
            ("consultas", "icons/Icono Consulta.png"),
            ("medicos", "icons/Icono Medico.png"),
            ("informes", "icons/Icono Informe.png"),
            ("medicamentos", "icons/Icono Medicamento.png"),
            ("recetas", "icons/Icono Receta.png"),
            ("cerrar", "icons/Icono Cerrar Sesion.png")
        ]
        iconos = {}
        for key, ruta_rel in nombres:
            img = self.cargar_imagen(ruta_rel, tamaño=(20, 20))
            iconos[key] = img if img else None
        return iconos

    def cargar_logo(self):
        return self.cargar_imagen("Logo Principal.jpeg", tamaño=(100, 100))

    # ------------------------------------------------------------
    # MENÚ LATERAL
    # ------------------------------------------------------------
    def crear_menu_lateral(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=SIDEBAR_COLOR, corner_radius=0, width=220)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)

        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        logo_frame.grid_columnconfigure(0, weight=1)

        if self.logo_img:
            lbl_logo = ctk.CTkLabel(logo_frame, image=self.logo_img, text="")
            lbl_logo.grid(row=0, column=0)
        else:
            lbl_logo = ctk.CTkLabel(logo_frame, text="🏥", font=ctk.CTkFont(size=50))
            lbl_logo.grid(row=0, column=0)

        # Diccionario para guardar referencias a los botones del menú
        self.menu_botones = {}

        menu_opciones = [
            ("inicio", "Panel Principal"),
            ("pacientes", "Pacientes"),
            ("consultas", "Consultas"),
            ("medicos", "Médicos"),
            ("informes", "Informes"),
            ("medicamentos", "Medicamentos"),
            ("recetas", "Recetas")
        ]

        for i, (key, texto) in enumerate(menu_opciones):
            icon = self.icons.get(key)
            btn = ctk.CTkButton(
                self.sidebar,
                text=texto,
                image=icon if icon else None,
                compound="left",
                anchor="w",
                fg_color="transparent",
                hover_color="#1F3653",
                text_color="white",
                font=ctk.CTkFont(family="Roboto", size=14),
                corner_radius=8,
                height=40,
                command=lambda k=key: self.cargar_vista(k)
            )
            btn.grid(row=i+1, column=0, padx=15, pady=5, sticky="ew")
            self.menu_botones[key] = btn

        # Cerrar sesión (cierra la aplicación)
        icon_cerrar = self.icons.get("cerrar")
        btn_cerrar = ctk.CTkButton(
            self.sidebar,
            text="Cerrar Sesión",
            image=icon_cerrar if icon_cerrar else None,
            compound="left",
            anchor="w",
            fg_color="transparent",
            hover_color="#B33939",
            text_color="white",
            font=ctk.CTkFont(family="Roboto", size=14),
            height=40,
            command=self.cerrar_sesion
        )
        btn_cerrar.grid(row=9, column=0, padx=15, pady=(10, 30), sticky="ew")

    def cerrar_sesion(self):
        """Cierra la aplicación completamente."""
        self.destroy()

    # ------------------------------------------------------------
    # CONTENIDO PRINCIPAL
    # ------------------------------------------------------------
    def crear_contenido_principal(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        self.main_frame.grid_rowconfigure(0, weight=0)   # encabezado común
        self.main_frame.grid_rowconfigure(1, weight=1)   # contenedor de vistas
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.crear_encabezado_comun()

        self.contenedor_vistas = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.contenedor_vistas.grid(row=1, column=0, sticky="nsew")
        self.contenedor_vistas.grid_rowconfigure(0, weight=1)
        self.contenedor_vistas.grid_columnconfigure(0, weight=1)

    def crear_encabezado_comun(self):
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        lbl_bienvenida = ctk.CTkLabel(
            header_frame,
            text="Bienvenidos/a a Modern Care Clinic",
            font=ctk.CTkFont(family=("Inter", "Roboto", "Arial"), size=24, weight="bold"),
            text_color=SIDEBAR_COLOR
        )
        lbl_bienvenida.pack(anchor="w")

        fecha_actual = datetime.now().strftime("Resumen Diario - %A, %d de %B de %Y | %I:%M %p")
        lbl_fecha = ctk.CTkLabel(
            header_frame,
            text=fecha_actual.title(),
            font=ctk.CTkFont(family="Roboto", size=15),
            text_color=TEXT_LIGHT
        )
        lbl_fecha.pack(anchor="w")

    # ------------------------------------------------------------
    # CARGA DE VISTAS DINÁMICAS (con resaltado de menú)
    # ------------------------------------------------------------
    def cargar_vista(self, nombre_vista):
        # Limpiar el contenedor
        for widget in self.contenedor_vistas.winfo_children():
            widget.destroy()

        # Resaltar el botón del menú correspondiente
        for key, btn in self.menu_botones.items():
            if key == nombre_vista:
                btn.configure(fg_color="#1F3653")  # color activo
            else:
                btn.configure(fg_color="transparent")  # color inactivo

        # Fábrica de vistas
        factories = {
            "inicio": self.crear_vista_inicio,
            "pacientes": self.crear_vista_pacientes,
            "consultas": self.crear_vista_consultas,
            "medicos": self.crear_vista_medicos,
            "informes": self.crear_vista_informes,
            "medicamentos": self.crear_vista_medicamentos,
            "recetas": self.crear_vista_recetas,
        }

        factory = factories.get(nombre_vista)
        if factory:
            vista = factory()
            vista.pack(fill="both", expand=True)
        else:
            lbl_error = ctk.CTkLabel(
                self.contenedor_vistas,
                text=f"Módulo '{nombre_vista}' no implementado",
                font=ctk.CTkFont(size=16),
                text_color="red"
            )
            lbl_error.pack(pady=50)

    # -------------------- Fábricas de vistas --------------------
    def crear_vista_inicio(self):
        return VistaInicio(self.contenedor_vistas)

    def crear_vista_pacientes(self):
        return VistaPacientes(self.contenedor_vistas)

    def crear_vista_consultas(self):
        return VistaConsultas(self.contenedor_vistas)

    def crear_vista_medicos(self):
        return VistaMedicos(self.contenedor_vistas)

    def crear_vista_medicamentos(self):
        return VistaMedicamentos(self.contenedor_vistas)

    def crear_vista_recetas(self):
        return VistaRecetas(self.contenedor_vistas)

    def crear_vista_informes(self):
        return VistaInformes(self.contenedor_vistas)


if __name__ == "__main__":
    app = ModernCareApp()
    app.mainloop()