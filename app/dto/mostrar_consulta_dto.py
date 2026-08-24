class MostrarConsultaDto:
    def __init__(self, id, costo, fecha, diagnostico=None, paciente=None, medico=None):
        self.id = id
        self.costo = costo
        self.fecha = fecha
        self.diagnostico = diagnostico
        self.paciente = paciente
        self.medico = medico