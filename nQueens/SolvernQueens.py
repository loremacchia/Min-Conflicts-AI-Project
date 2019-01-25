import csv
import random
from timeit import default_timer as timer


class Queen:

    def __init__(self, row, column):
        self.row = row
        self.column = column


class Solver:

    def __init__(self, n):
        self.currentConflicts = []
        self.inConflict = []
        self.variables = []
        self.n = n
        self.randomRestarts = 0
        self.localMinimaIndex = 0
        self.plateauxIndex = 0

    def minConflict(self, maxSteps):
        start = timer()
        self.initSolution()
        for i in range(maxSteps):
            if (self.checkSolution()):
                stop = timer()
                # self.printTable() # Se si vuole vedere la stampa a video del risultato togliere il # di commento
                return [self.variables, self.randomRestarts, stop - start]
            variable = self.inConflict[random.randint(0, len(self.inConflict) - 1)]  # è una regina
            value = self.getMinConflicting(variable)  # è la nuova posizione della regina
            if (self.restartCondition()):
                self.randomRestart()
            self.updateConflicts(variable, value)
        stop = timer()
        return [[], self.randomRestarts, stop - start]

    def initSolution(self):
        self.currentConflicts = [[0 for i in range(self.n)] for j in range(self.n)]
        self.variables = [Queen(random.randint(1, self.n - 1), k) for k in range(self.n)]
        self.calculateConflicts()

    # calcola il numero di conflitti per ogni cella per ogni regina
    def calculateConflicts(self):
        for column in range(len(self.variables)):
            self.addConflict(self.variables[column].row, column, self.n)
        for column in range(len(self.variables)):
            row = self.variables[column].row
            if (self.currentConflicts[row][column] > 0):
                self.inConflict.append(self.variables[column])

    def addConflict(self, row, column, n):
        k = 1
        while (k <= n):
            if (row + k < n and column + k < n):
                self.currentConflicts[row + k][column + k] += 1
            if (0 <= row - k < n and column + k < n):
                self.currentConflicts[row - k][column + k] += 1
            if (row + k < n and 0 <= column - k < n):
                self.currentConflicts[row + k][column - k] += 1
            if (0 <= row - k < n and 0 <= column - k < n):
                self.currentConflicts[row - k][column - k] += 1
            if (k - 1 != column):
                self.currentConflicts[row][k - 1] += 1
            k += 1

    def removeConflict(self, row, column, n):
        k = 1
        while (k <= n):
            if (row + k < n and column + k < n):
                self.currentConflicts[row + k][column + k] -= 1
            if (0 <= row - k < n and column + k < n):
                self.currentConflicts[row - k][column + k] -= 1
            if (row + k < n and 0 <= column - k < n):
                self.currentConflicts[row + k][column - k] -= 1
            if (0 <= row - k < n and 0 <= column - k < n):
                self.currentConflicts[row - k][column - k] -= 1
            if (k - 1 != column):
                self.currentConflicts[row][k - 1] -= 1
            k += 1

    def checkSolution(self):
        if (len(self.inConflict) == 0):
            return True
        return False

    def getMinConflicting(self, queen):
        min = [0, self.n]
        for row in range(self.n):
            if (row != queen.row):
                if (self.currentConflicts[row][queen.column] < min[1]):
                    min = [row, self.currentConflicts[row][queen.column]]
        return min[0]

    def updateConflicts(self, queen, newRow):
        oldRow = queen.row
        column = queen.column
        if (self.currentConflicts[oldRow][column] == self.currentConflicts[newRow][column]):
            self.plateauxIndex += 1
        elif (self.currentConflicts[oldRow][column] < self.currentConflicts[newRow][column]):
            self.localMinimaIndex += 1
        queen.row = newRow
        self.removeConflict(oldRow, column, self.n)
        self.addConflict(newRow, column, self.n)
        self.checkQueens()

    def checkQueens(self):
        for i in range(len(self.variables)):
            if (self.currentConflicts[self.variables[i].row][i] > 0 and self.variables[i] not in self.inConflict):
                self.inConflict.append(self.variables[i])
            if (self.currentConflicts[self.variables[i].row][i] == 0 and self.variables[i] in self.inConflict):
                self.inConflict.remove(self.variables[i])

    def restartCondition(self):
        return self.localMinimaIndex == 1 or self.plateauxIndex == 120

    def randomRestart(self):
        self.inConflict = []
        self.initSolution()
        self.randomRestarts += 1
        self.localMinimaIndex = 0
        self.plateauxIndex = 0

    def printTable(self): # funzione che serve a stampare la scacchiera attuale
        print()
        for row in range(self.n):
            for col in range(self.n):
                if (row == self.variables[col].row):
                    print("{:>6}".format(" Q"), end=" ")
                else:
                    print("{:>6}".format(" x"), end=" ")
            print()
        print()


def main():
    for n in range(1, 120):
        n *= 5
        print(n)
        for i in range(10):
            solver = Solver(n)
            queens, randomRestarts, runningTime = solver.minConflict(10000)
            # while(len(queens) == 0): # togliere i commenti se si vogliono ottenere tutte soluzioni valide
            #     solver = Solver(n)
            #     queens,randomRestarts = solver.minConflictnQueens(1000)
            with open('randomRestartsQueen.csv', mode='a') as statistic:
                writer = csv.writer(statistic, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                if (len(queens) == 0):
                    writer.writerow([n, randomRestarts, "Error"])
                else:
                    writer.writerow([n, randomRestarts])
            with open('runningTimeQueen.csv', mode='a') as time:
                writer = csv.writer(time, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                if (len(queens) == 0):
                    writer.writerow([n, runningTime, "Error"])
                else:
                    writer.writerow([n, runningTime])


if __name__ == '__main__':
    main()
