class Medicamento:
    def __init__(self, nombre, laboratorio, precio, stock, id = None):
        self.id = id
        self.nombre = nombre
        self.laboratorio = laboratorio
        self.precio = precio
        self.stock = stock