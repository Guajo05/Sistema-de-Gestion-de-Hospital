import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class ChartBuilder:
    @staticmethod
    def grafica_pastel(datos: dict, titulo: str = '') -> Figure:
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.pie(
            datos['valores'],
            labels=datos['etiquetas'],
            autopct='%1.1f%%',
            startangle=90
        )
        ax.set_title(titulo)
        ax.axis('equal')

        return fig

    @staticmethod
    def grafica_barras(datos: dict, titulo: str = '', color: str = '#4C72B0') -> Figure:
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.bar(datos['etiquetas'], datos['valores'], color=color)
        ax.set_title(titulo)
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()

        return fig