class ConsultaMasCaraDto:
    def __init__(self, paciente, medico, diagnostico, costo, fecha):
        self.paciente = paciente
        self.medico = medico
        self.diagnostico = diagnostico
        self.costo = costo
        self.fecha = fecha