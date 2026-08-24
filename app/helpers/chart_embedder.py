import matplotlib
matplotlib.use("TkAgg")  # Necesario para embeber en Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

class ChartEmbedder:
    """
    Helper que convierte una figura de Matplotlib en un widget CTk
    listo para ser colocado en la interfaz.
    """
    @staticmethod
    def embed_chart(master: ctk.CTkFrame, figure, row=0, column=0, sticky="nsew", padx=5, pady=5):
        canvas = FigureCanvasTkAgg(figure, master=master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        return canvas

    @staticmethod
    def embed_chart_pack(master: ctk.CTkFrame, figure, fill="both", expand=True, padx=5, pady=5):
        """
        Versión con pack() en lugar de grid().
        """
        canvas = FigureCanvasTkAgg(figure, master=master)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=fill, expand=expand, padx=padx, pady=pady)
        return canvas