class Medico:
    def __init__(self, nombre, especialidad, salario, turno, estado, id = None):
        self.id = id
        self.nombre = nombre
        self.especialidad = especialidad
        self.salario = salario
        self.turno = turno
        self.estado = estado