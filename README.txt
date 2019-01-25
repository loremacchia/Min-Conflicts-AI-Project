Nelle due cartelle MapColoring e nQueens troviamo i codici sorgente
e dei file .csv in cui sono riportati i dati ricavati dai test svolti
sull'algoritmo. 

Se si vuole testare nuovamente l'algoritmo generando nuovi dati deve
essere eseguito il codice sorgente del problema scelto. In autonomia
il programma creerà nuovi file .csv o caricherà quelli già esistenti
su cui scriverà i risultati.

Per eseguire i codici sorgente in un sistema operativo Ubuntu è
necessario scrivere nella linea di comando:

python3 nomeFile.py


Per l'implementazione dell'algoritmo Min Conflicts ho seguito lo 
pseudocodice prpresentato nel libro Artificial Intelligence a 
Modern Approach al capitolo 6.4; per la creazione delle mappe 
ho seguito la strategia proposta nell’esercizio 6.10 del libro 
Artificial Intelligence a Modern Approach; per la verifica della
intersezione fra archi ho utilizzato l’algoritmo presentato al 
capitolo 33.1 nel libro Introduction to Algorithms. Ulteriori
dettagli sono forniti nel file "Relazione Macchiarini 6129400.pdf".

Per fornire la possibilità di svolgere tutti i test che ho svolto 
ho inserito nel codice variabili non previste dallo pseudocodice.
La base del codice è generale ed è quella sotto riportata.

    def minConflict(self, maxSteps):
        self.initSolution()
        for i in range(maxSteps):
            if (self.checkSolution()):
                return self.variables
            variable = self.inConflict[random.randint(0, len(self.inConflict) - 1)]
            value = self.getMinConflicting(variable) 
            if (self.restartCondition()):
                self.randomRestart()
            self.updateValue(variable, value)
        return None