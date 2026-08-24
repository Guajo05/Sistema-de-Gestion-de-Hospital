import customtkinter as ctk
from tkinter import ttk, messagebox
from app.controllers.medicamento_controller import MedicamentoController

class VistaMedicamentos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#F5F6FA")

        self.controller = MedicamentoController()
        self.tree = None
        self.medicamentos_cargados = []

        self.crear_encabezado()
        self.crear_contenido_principal()

    def crear_encabezado(self):
        header_frame = ctk.CTkFrame(self, fg_color="#F5F6FA")
        header_frame.pack(fill="x", pady=(20, 10), padx=20)

        title_label = ctk.CTkLabel(header_frame, text="Gestión de Medicamentos",
                                   font=ctk.CTkFont(size=24, weight="bold"), text_color="#0B1A33")
        title_label.pack(side="left")

        add_btn = ctk.CTkButton(header_frame, text="+ Registrar Nuevo Medicamento",
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

    def obtener_medicamento_seleccionado(self):
        if self.tree is None:
            return None
        seleccion = self.tree.selection()
        if not seleccion:
            self.mostrar_alerta("SELECCIONA UN MEDICAMENTO DE LA TABLA PRIMERO.❎", es_error=True)
            return None
        medicamento_id = int(seleccion[0])
        return next((m for m in self.medicamentos_cargados if m.id == medicamento_id), None)

    # ------------------- TABLA CON ESTILOS -------------------
    def mostrar_tabla(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        medicamentos, mensaje = self.controller.mostrar_medicamentos()

        if not medicamentos:
            self.medicamentos_cargados = []
            self.mostrar_alerta(mensaje, es_error=True)
            no_data_label = ctk.CTkLabel(self.content_frame, text="No hay medicamentos registrados",
                                         font=ctk.CTkFont(size=18, weight="bold"),
                                         text_color="red")
            no_data_label.pack(pady=50)
            return

        self.medicamentos_cargados = medicamentos

        table_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=10)
        table_frame.pack(fill="both", expand=True)

        # Estilos
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Medicamentos.Treeview.Heading",
            font=("Roboto", 13, "bold"),
            background="#0D223B",
            foreground="white",
            fieldbackground="#0D223B",
            borderwidth=0
        )
        style.configure(
            "Medicamentos.Treeview",
            font=("Roboto", 12),
            rowheight=32,
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground="#1A2530"
        )
        style.map(
            "Medicamentos.Treeview",
            background=[("selected", "#2B71B9")],
            foreground=[("selected", "white")]
        )

        columns = ("ID", "Nombre", "Laboratorio", "Precio", "Stock")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10,
            style="Medicamentos.Treeview"
        )

        self.tree.column("ID", anchor="center", width=80)
        self.tree.column("Nombre", anchor="center", width=250)
        self.tree.column("Laboratorio", anchor="center", width=200)
        self.tree.column("Precio", anchor="center", width=120)
        self.tree.column("Stock", anchor="center", width=120)

        for col in columns:
            self.tree.heading(col, text=col)

        for medicamento in medicamentos:
            self.tree.insert("", "end", iid=str(medicamento.id),
                        values=(medicamento.id, medicamento.nombre, medicamento.laboratorio,
                                medicamento.precio, medicamento.stock))

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones de acción
        action_frame = ctk.CTkFrame(self.content_frame, fg_color="#F5F6FA")
        action_frame.pack(pady=10)

        def eliminar_medicamento():
            medicamento = self.obtener_medicamento_seleccionado()
            if medicamento is None:
                return

            confirmado = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Seguro que deseas eliminar el medicamento '{medicamento.nombre}'?"
            )
            if not confirmado:
                return

            exito, mensaje = self.controller.eliminar_medicamento(medicamento.id)
            self.mostrar_alerta(mensaje, es_error=not exito)

            if exito:
                self.mostrar_tabla()

        def actualizar_medicamento():
            medicamento = self.obtener_medicamento_seleccionado()
            if medicamento is None:
                return
            self.mostrar_formulario(medicamento)

        eliminar_btn = ctk.CTkButton(action_frame, text="🗑️ Eliminar", fg_color="red",
                                     text_color="white", corner_radius=8,
                                     command=eliminar_medicamento)
        eliminar_btn.pack(side="left", padx=10)

        actualizar_btn = ctk.CTkButton(action_frame, text="✏️ Actualizar", fg_color="#1E3A5F",
                                       text_color="white", corner_radius=8,
                                       command=actualizar_medicamento)
        actualizar_btn.pack(side="left", padx=10)

    # ------------------- FORMULARIO -------------------
    def mostrar_formulario(self, medicamento=None):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        modo_edicion = medicamento is not None

        form_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF", corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        titulo = "Editar Medicamento" if modo_edicion else "Registrar Nuevo Medicamento"
        ctk.CTkLabel(form_frame, text=titulo,
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        nombre_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Nombre Medicamento")
        nombre_entry.pack(pady=10)

        laboratorio_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Laboratorio")
        laboratorio_entry.pack(pady=10)

        precio_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Precio")
        precio_entry.pack(pady=10)

        stock_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Stock disponible")
        stock_entry.pack(pady=10)

        if modo_edicion:
            nombre_entry.insert(0, medicamento.nombre)
            laboratorio_entry.insert(0, medicamento.laboratorio)
            precio_entry.insert(0, str(medicamento.precio))
            stock_entry.insert(0, str(medicamento.stock))

        button_frame = ctk.CTkFrame(form_frame, fg_color="#FFFFFF")
        button_frame.pack(pady=20)

        def guardar_medicamento():
            datos = {
                "nombre": nombre_entry.get(),
                "laboratorio": laboratorio_entry.get(),
                "precio": precio_entry.get(),
                "cantidad": stock_entry.get(),
            }

            if modo_edicion:
                datos["id"] = medicamento.id
                resultado, mensaje = self.controller.actualizar_medicamento(datos)
            else:
                resultado, mensaje = self.controller.registrar_medicamento(datos)

            es_error = resultado is None
            self.mostrar_alerta(mensaje, es_error=es_error)

            if resultado is not None:
                self.mostrar_tabla()

        guardar_btn = ctk.CTkButton(button_frame, text="Guardar Cambios" if modo_edicion else "Guardar Medicamento",
                                    fg_color="#1E3A5F", text_color="white", corner_radius=8,
                                    command=guardar_medicamento)
        guardar_btn.pack(side="left", padx=10)

        cancelar_btn = ctk.CTkButton(button_frame, text="Cancelar", fg_color="gray",
                                     text_color="white", corner_radius=8,
                                     command=self.mostrar_tabla)
        cancelar_btn.pack(side="left", padx=10)