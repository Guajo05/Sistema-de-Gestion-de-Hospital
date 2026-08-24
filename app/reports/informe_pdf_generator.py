from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

class InformePDFGenerator:
    """
    Se encarga únicamente de tomar una lista de figuras de matplotlib
    y empaquetarlas en un solo archivo PDF.
    """

    @staticmethod
    def generar(figuras: list, ruta_destino: str, titulo: str = "Informe Estadístico") -> tuple[bool, str]:
        """
        Genera un PDF con una figura por página.

        Args:
            figuras: lista de objetos matplotlib.figure.Figure
            ruta_destino: ruta completa donde se guardará el .pdf
            titulo: texto de portada (opcional)

        Returns:
            (exito: bool, mensaje: str)
        """
        try:
            with PdfPages(ruta_destino) as pdf:
                for figura in figuras:
                    if figura is not None:
                        pdf.savefig(figura, bbox_inches="tight")

                # Metadata del PDF
                d = pdf.infodict()
                d['Title'] = titulo
                d['Author'] = 'Modern Care Clinic - Sistema de Gestión Hospitalaria'
                d['CreationDate'] = datetime.now()

            return True, f"Informe guardado exitosamente en:\n{ruta_destino}"

        except Exception as e:
            return False, f"Error al generar el informe: {str(e)}"