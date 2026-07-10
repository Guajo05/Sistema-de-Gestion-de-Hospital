class Receta:
    def __init__(self, dosis, dias, consulta, medicamento, cantidad, id = None):
        self.id = id
        self.dosis = dosis
        self.dias = dias
        self.consulta = consulta
        self.medicamento = medicamento
        self.cantidad = cantidad
