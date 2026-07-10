class Consulta:
    def __init__(self, fecha,
                 diagnostico, costo, paciente, medico, id = None):
        self.id = id
        self.fecha = fecha
        self.diagnostico = diagnostico
        self.costo = costo
        self.paciente = paciente
        self.medico = medico