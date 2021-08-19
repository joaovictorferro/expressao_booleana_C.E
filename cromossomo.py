class Cromossomo:
    def __init__(self, individuo):
        self.individuo = individuo

    def __str__(self):
        chromosomes = ''
        for i in range(len(self.individuo)):
            chromosomes += str(self.individuo[i]) + " "
        return chromosomes
