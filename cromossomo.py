class Cromossomo:
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        chromosomes = ''
        for i in range(len(self.valor)):
            chromosomes += str(self.valor[i]) + " "
        return chromosomes
