import numpy as np
from cromossomo import  Cromossomo
from tree import Node
solucao = [[1,1,1,0],
         [1,1,0,0],
         [1,0,1,0],
         [1,0,0,1],
         [0,1,1,0],
         [0,1,0,0],
         [0,0,1,0],
         [0,0,0,0]]

dicionario = {0: "and", 1: "or"}
arvore = [[]] #lista de adjacencia
populacao = []
global index
index = 0

def print_tree(no):
    if no == None:
        return
    print(no.data)
    print_tree(no.left)
    print_tree(no.right)

def construirArvore(cromossomo,no):
    global index
   # print(index)
    #print("no da arvore: " + cromossomo[index])
    no_novo = Node('')
    if index< len(cromossomo) and  cromossomo[index] == "!":
        no = Node("!")
        index += 1
        no.left = construirArvore(cromossomo,no_novo)
    if index< len(cromossomo) and cromossomo[index] == '(':
        no = Node("")
        index += 1
        no.left = construirArvore(cromossomo,no_novo)
       #print("Cromossomo index: " + cromossomo[index])
    if index< len(cromossomo) and (cromossomo[index] == 'and' or cromossomo[index] == 'or'):
        if cromossomo[index] == 'and':
            no.data = 'and'
        else:
            no.data = 'or'
        index += 1
        no.right = construirArvore(cromossomo,no_novo)

    if index< len(cromossomo) and cromossomo[index] == 'q':
        no_novo = Node('q')
        index += 1
        if index< len(cromossomo) and cromossomo[index] ==')':
            index += 1
        return no_novo
    return no

def init_populacao():
    for i in range(1):
        cromossomo = []
        # for i in range(10):
        aleatorio = np.random.randint(0, 2)
        if aleatorio == 1:
            cromossomo.append('!')
        cromossomo.append('(')
        aleatorio = np.random.randint(0, 2)
        if aleatorio == 1:
            cromossomo.append('!')
        cromossomo.append('(')
        cromossomo.append('q')
        aleatorio = np.random.randint(0, 2)
        if aleatorio == 0:
            cromossomo.append('and')
        else:
            cromossomo.append('or')
        aleatorio = np.random.randint(0, 2)
        if aleatorio == 1:
            cromossomo.append('!')
        cromossomo.append('q')
        cromossomo.append(')')
        aleatorio = np.random.randint(0, 2)
        if aleatorio == 0:
            cromossomo.append('and')
        else:
            cromossomo.append('or')
        aleatorio = np.random.randint(0, 2)
        if aleatorio == 1:
            cromossomo.append('!')
        cromossomo.append('q')
        cromossomo.append(')')

        populacao.append(Cromossomo(cromossomo))
        for l in range (len(populacao)):
            print(populacao[l])
        no = Node('')
        index = 0
        no = construirArvore(cromossomo,no)
        print_tree(no)

if __name__ == '__main__':
    init_populacao()
