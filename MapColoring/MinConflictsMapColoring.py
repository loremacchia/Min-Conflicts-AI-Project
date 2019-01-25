import bisect
import csv
import math
import random
from timeit import default_timer as timer


class Region:

    def __init__(self, x, y, name, color=-1):
        self.x = x
        self.y = y
        self.color = color
        self.arcs = []
        self.name = name


class Solver:

    def __init__(self, list, n, k):
        self.variables = list
        self.inConflict = []
        self.randomRestarts = 0
        self.localMinimaIndex = 0
        self.plateauxIndex = 0
        self.n = n
        self.k = k

    def minConflict(self, maxSteps):
        start = timer()
        self.initSolution()
        for i in range(maxSteps):
            if (self.checkSolution()):
                stop = timer()
                return [self.variables, self.randomRestarts, stop - start]
            variable = self.inConflict[random.randint(0, len(self.inConflict) - 1)]  # variable è una regione
            value = self.getMinConflicting(variable)  # value è il colore che minimizza
            if (self.restartCondition()):
                self.randomRestart()
            self.updateValue(variable, value)
        stop = timer()
        return [[], self.randomRestarts, stop - start]

    def initSolution(self):
        for i in range(len(self.variables)):
            self.updateValue(self.variables[i], random.randint(1, self.k))

    def checkSolution(self):
        if (len(self.inConflict) == 0):
            return True
        return False

    def getMinConflicting(self, region):
        initialConflicts = 0
        for j in range(len(region.arcs)):
            if (region.arcs[j].color == region.color):
                initialConflicts += 1
        minColor = -1
        minConflicts = len(region.arcs)
        for color in range(1, self.k):
            if (color != region.color):
                currentConflicts = 0
                for j in range(len(region.arcs)):
                    if (region.arcs[j].color == color): # rappresentazione della violazione del vincolo
                        currentConflicts += 1
                if (currentConflicts < minConflicts):
                    minConflicts = currentConflicts
                    minColor = color
        if (initialConflicts < minConflicts):
            self.localMinimaIndex += 1
        elif (initialConflicts == minConflicts):
            self.plateauxIndex += 1
        return minColor

    def updateValue(self, region, color):  # region appartiene ad inConflict
        region.color = color
        noConflicts = True
        for i in range(len(region.arcs)):
            if (color == region.arcs[i].color):
                if (region.arcs[i] not in self.inConflict):
                    self.inConflict.append(region.arcs[i])
                noConflicts = False
        if (noConflicts and region in self.inConflict):
            self.inConflict.remove(region)

    def restartCondition(self):
        return self.localMinimaIndex == 1 or self.plateauxIndex == 1

    def randomRestart(self):
        self.inConflict = []
        self.initSolution()
        self.randomRestarts += 1
        self.localMinimaIndex = 0
        self.plateauxIndex = 0


class MapGenerator:

    def __init__(self, n):
        self.regions = []
        self.arcs = []
        self.n = n

    # dim è la dimensione della matrice, n è il numeto di regioni, k è il numero di colori. Dati questi input la
    # funzione genera n regioni e le collega con il massimo numero di archi fra 0 e k-1
    def generateMap(self, dim):
        created = []  # lista che tiene conto di quali punti (x,y) sono stati creati
        for i in range(self.n):  # ciclo che genera le regioni
            done = False
            while (not done):
                x = random.randint(0, dim - 1)
                y = random.randint(0, dim - 1)
                if ((x, y) not in created):
                    created.append((x, y))
                    self.regions.append(Region(x, y, i))
                    done = True
        self.regionConnection()
        return self.regions, self.arcs

    # funzione che connette le regioni con le regioni più vicine
    def regionConnection(self):

        def intersect(p1, p2, p3, p4):
            d1 = direction(p3, p4, p1)
            d2 = direction(p3, p4, p2)
            d3 = direction(p1, p2, p3)
            d4 = direction(p1, p2, p4)

            if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
                return True

            elif d1 == 0 and onSegment(p3, p4, p1):
                return True
            elif d2 == 0 and onSegment(p3, p4, p2):
                return True
            elif d3 == 0 and onSegment(p1, p2, p3):
                return True
            elif d4 == 0 and onSegment(p1, p2, p4):
                return True
            else:
                return False

        def direction(p1, p2, p3):
            return (p3.y - p1.y) * (p2.x - p1.x) - (p3.x - p1.x) * (p2.y - p1.y)

        def onSegment(p1, p2, p):
            return min(p1.x, p2.x) < p.x < max(p1.x, p2.x) and min(p1.y, p2.y) < p.y < max(p1.y, p2.y)

        # funzione che calcola la distanza fra due regioni
        def distance(A, B):  # dato che mi serve il minimo non importa che faccia la radice
            return math.pow((A.x - B.x), 2) + math.pow((A.y - B.y), 2)

        available = self.regions.copy()  # le regioni che possono avere ancora un arco
        while (len(available) > 0):
            region = available.pop(random.randint(0, len(available) - 1))  # prendo una regione a caso dalle disponibili
            i = region.name
            dist = [] # vettore ordinato in cui sono messe le distanze minime dal nodo ad altri nodi ammissibili
            momentaryArcs = [] # vettore ordinato in base a dist in cui sono inseriti i possibili archi
            # preso l'arco (i,j) guarda se è ammissibile e se interseca un arco già presente
            for j in range(len(self.regions)):
                if (j != i and (self.regions[i], self.regions[j]) not in self.arcs
                        and (self.regions[j], self.regions[i]) not in self.arcs):
                    isIntersected = False
                    w = 0
                    # il ciclo non termina fino a quando o non trova un'intersezione o ha controllato tutti gli archi
                    while (not isIntersected and w < len(self.arcs) and len(self.arcs) > 0):
                        if (intersect(self.regions[i], self.regions[j], self.arcs[w][0], self.arcs[w][1])):
                            isIntersected = True
                        w += 1
                    d = distance(self.regions[i], self.regions[j])
                    if (not isIntersected):
                        index = bisect.bisect(dist, d) # con il metodo della bisezione trovo l'indice in cui inserire d
                        dist.insert(index, d) # la distanza fra i due nodi viene inserita nel vettore ordinato
                        momentaryArcs.insert(index, (self.regions[i], self.regions[j])) # viene inserito nella posizione
                                                                                        # giusta anche l'arco
            if (len(dist) > 0): # controllo che mostra se non ci sono ancora archi ammessi
                current = momentaryArcs.pop(0)
                self.arcs.append(current)
                current[0].arcs.append(current[1])
                current[1].arcs.append(current[0])
                available.append(region)


def main():
    for k in [3, 4, 5]: # k è il numero di colori
        for n in range(4, 40): # n è il numero di Regioni da creare
            print(n)
            for i in range(10): # vengono svolte 10 prove per ogni n
                generator = MapGenerator(n)
                regions, arcs = generator.generateMap(n)
                solver = Solver(regions, n, k)
                queens, randomRestarts, runTime = solver.minConflict(10000)
                with open('randomRestartsMap.csv', mode='a') as statistic:
                    writer = csv.writer(statistic, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    if (len(queens) == 0):
                        writer.writerow([n, k, randomRestarts, "Error"])
                    else:
                        writer.writerow([n, k, randomRestarts])
                with open('runningTimeMap.csv', mode='a') as time:
                    writer = csv.writer(time, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    if (len(queens) == 0):
                        writer.writerow([n, k, runTime, "Error"])
                    else:
                        writer.writerow([n, k, runTime])
                with open('arcsInMap.csv', mode='a') as arcNumber:
                    writer = csv.writer(arcNumber, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([n, len(arcs)])

if __name__ == '__main__':
    main()