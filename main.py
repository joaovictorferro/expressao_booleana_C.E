import numpy as np
from cromossomo import Cromossomo
from tree import Node
from copy import deepcopy

solucao = [[1,1,1,0],
         [1,1,0,0],
         [1,0,1,1],
         [1,0,0,0],
         [0,1,1,1],
         [0,1,0,0],
         [0,0,1,1],
         [0,0,0,0]]

dicionario = {0: "and", 1: "or"}
populacao = []
novaPopulacao = []
listaFant = []
nodes_to_remove = []
global index
index = 0

def selection():
    qualquerLista = populacao + novaPopulacao
    qualquerLista = sorted(qualquerLista, key=lambda ind: abs(ind.score), reverse=True)
    selected_population = []
    for i in range(20):
        selected_population.append(qualquerLista[i])
    return selected_population

def change_subtree(node):
    if node == None:
        return
    if node.left == nodes_to_remove[0]:
        node.left = deepcopy(nodes_to_remove[1])
        return
    if node.right == nodes_to_remove[0]:
        node.right = deepcopy(nodes_to_remove[1])
        return
    if node.left == nodes_to_remove[1]:
        node.left = deepcopy(nodes_to_remove[0])
        return
    if node.right == nodes_to_remove[1]:
        node.right = deepcopy(nodes_to_remove[0])
        return
    change_subtree(node.left)
    change_subtree(node.right)

def search_subtree(root):
    if root == None:
        return False
    if root.data == "or" or root.data == "and":
        return True
    return search_subtree(root.left) or search_subtree(root.right)

def search(node):
    if node == None:
        return
    if node.data == "or" or node.data == "and":
        flag_left = search_subtree(node.left)
        flag_right = search_subtree(node.right)
        if not flag_left and not flag_right:
            nodes_to_remove.append(node)
            return
    search(node.left)
    search(node.right)

def mutate_node(node, possibilities, change_to=""):
    if node == None:
        return
    if node.left != None and len(possibilities) == 2:
        if node.left.data in possibilities:
            if node.left.left == None:
                node.left = node.left.right
            else:
                node.left = node.left.left
            return
    if node.right != None and len(possibilities) == 2:
        if node.right.data in possibilities:
            if node.right.right == None:
                node.right = node.right.left
            else:
                node.right = node.right.right
            return
    if node.data in possibilities:
        if node.data == "or" or node.data == "and":
            node.data = change_to
            return

def mutation(population):
    for ind in population:
        chance = np.random.randint(0, 100)
        if chance <= 3:
            chance = np.random.randint(1, 3)
            if chance == 2:
                mutate_node(ind, ["and"], "or")
            else:
                mutate_node(ind, ["or"], "and")

def cross_over(population):
    new_population = []
    for father in population:
        for mother in population:
            if father != mother:
                chance = np.random.randint(0, 100)
                if chance <= 70:
                    first_son = deepcopy(father)
                    second_son = deepcopy(mother)
                    search(first_son)
                    search(second_son)
                    change_subtree(first_son)
                    change_subtree(second_son)
                    new_population.append(first_son)
                    new_population.append(second_son)
            nodes_to_remove.clear()
    return new_population

def score(ScorePopulacao):
    for ind in ScorePopulacao:
        lista = []
        listaFant.clear()
        in_order(ind)
        listaFant.reverse()
        indScore = 0
        for solu in solucao:
            lista = listaFant.copy()
            cont = 0

            while len(lista) != 0:
                var1 = lista.pop()
                if len(lista) == 0:
                    cont += 1
                    if var1 == solu[cont]:
                        indScore += 1
                    break

                if type(var1) is int:
                    var2 = lista.pop()
                    if var2 == '\\!':
                        if var1 == 0:
                            lista.insert(len(lista), 1)
                        else:
                            lista.insert(len(lista), 0)
                    if var2 == 'or':
                        cont += 1
                        var3 = lista.pop()
                        var3 = solu[cont]
                        if len(lista) != 0:
                            var4 = lista.pop()
                            if var4 == '!':
                                if var3 == 0:
                                    var3 = 1
                                else:
                                    var3 = 0
                            elif var4 == '\\!':
                                lista.insert(len(lista), '\\!')
                            else:
                                lista.insert(len(lista),var4)
                        resolu = var1 or var3
                        lista.insert(len(lista), resolu)

                    if var2 == 'and':
                        cont += 1
                        var3 = lista.pop()
                        var3 = solu[cont]
                        if len(lista) != 0:
                            var4 = lista.pop()
                            if var4 == '!':
                                if var3 == 0:
                                    var3 = 1
                                else:
                                    var3 = 0
                            elif var4 == '\\!':
                                lista.insert(len(lista), '\\!')
                            else:
                                lista.insert(len(lista),var4)
                        resolu = var1 and var3
                        lista.insert(len(lista), resolu)

                if var1 == 'q':
                    var2 = lista.pop()
                    if var2 == '!':
                        var3 = solu[cont]
                        if var3 == 0:
                            lista.insert(len(lista),1)
                        else:
                            lista.insert(len(lista), 0)
                    else:
                        lista.insert(len(lista),var2)
                        lista.insert(len(lista),solu[cont])

        ind.score = indScore

def print_tree(no):
    if no == None:
        return
    print(no.data)
    print_tree(no.left)
    print_tree(no.right)

def in_order(no):
    if no == None:
        return
    in_order(no.left)
    listaFant.append(no.data)
    in_order(no.right)

def construirArvore(cromossomo,no):
    global index
    if index< len(cromossomo) and cromossomo[index] == "\!":
        no = Node("\!")
        index += 1
        no.left = construirArvore(cromossomo,no)
        return no
    if index< len(cromossomo) and cromossomo[index] == "!":
        no = Node("!")
        index += 1
        no.left = construirArvore(cromossomo,no)
        return no

    if index<len(cromossomo) and cromossomo[index]=="(":
        no= Node('')
        index += 1
        no.left = construirArvore(cromossomo,no)

    if index < len(cromossomo) and (cromossomo[index] == 'and' or cromossomo[index] == 'or'):
        if cromossomo[index] == 'and':
            no.data = 'and'
        else:
            no.data = 'or'
        index += 1
        no.right = construirArvore(cromossomo, no)

    if index<len(cromossomo) and cromossomo[index] =='q':
        no = Node('q')
        index += 1

        if index < len(cromossomo) and cromossomo[index] == ')':
            index += 1
        return no
    return no

def init_populacao():
    global index
    for i in range(2):
        cromossomo = []
        aleatorio = np.random.randint(0, 2)
        if aleatorio == 1:
            cromossomo.append('\!')
        cromossomo.append('(')
        aleatorio = np.random.randint(0, 2)
        if aleatorio == 1:
            cromossomo.append('\!')
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

        # cromossomo.append('\!')
        # cromossomo.append('(')
        # cromossomo.append('\!')
        # cromossomo.append('(')
        # cromossomo.append('!')
        # cromossomo.append('q')
        # cromossomo.append('or')
        # cromossomo.append('!')
        # cromossomo.append('q')
        # cromossomo.append(')')
        # cromossomo.append('or')
        # cromossomo.append('!')
        # cromossomo.append('q')
        # cromossomo.append(')')
        no = Node('')
        no = construirArvore(cromossomo, no)
        #in_order(no)
        populacao.append(no)
        index = 0
        # cromossomo = populacao[l]

if __name__ == '__main__':
    init_populacao()
    score(populacao)
    new_population = cross_over(populacao)
    mutation(populacao)