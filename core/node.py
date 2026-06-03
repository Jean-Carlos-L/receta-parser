class Nodo:

    def __init__(self, etiqueta, hijos=None, valor=None):

        self.etiqueta = etiqueta
        self.hijos = hijos if hijos is not None else []
        self.valor = valor
        self.rasgos = {}
