import random
import math

class Bee:
    def __init__(self):
    
        ### Control Parameters of ABC Algorithm
        self.NP = 20    # The number of colony size (employed bees + onlooker bees)
        self.foodNumber = int(self.NP/2)    # The number of food sources equals the half of the colony size
        self.limit = 100    # A food source which could not be improved through "limit" is abandoned by its employed bee
        self.maxCycle = 2500     # The number of cycles for foraging (a stopping criteria)
        
        ### Problem specific variables
        self.d = 100    # The number of parameters of the problem to be optimized
        self.lb = -5.12    # lower bound of the parameters
        self.ub = 5.12      # upper bound of the parameters
        self.r = None       # a random number in range[0,1)
        self.runtime = 5    # Algorithm can be run many times in order to see its robustness (saglamlik)
        self.objValSol = None   # Objective function value of new solution
        self.fitnessSol = None      # Fitness value of new solution
        self.param2chance = None     ## param2change corrresponds to j,
        self.neighbour = None       ## neighbour corresponds to k in equation v_{ij}=x_{ij}+\phi_{ij}*(x_{kj}-x_{ij})
        self.globalMin = None       #Optimum solution obtained by ABC algorithm
        self.foods = [[0 for x in range(self.d)] for y in range(self.foodNumber)]
        self.f = [0 for x in range(self.foodNumber)]
        self.fitness = [0 for x in range(self.foodNumber)]
        self.solution = [0 for x in range(self.d)]
        self.trial = [0 for x in range(self.foodNumber)]
        self.prob = [0 for x in range(self.foodNumber)]
        self.globalParams = [0 for x in range(self.d)]
        self.globalMins = [0 for x in range(self.runtime)]


    def CalculateFitness(self,param):
        sonuc = 0
        if(param>=0):
            sonuc = 1/(param+1)
        else:
            sonuc = 1 + abs(param)
        return sonuc

    def MemorizeBestSource(self):
        for i in range(0, self.foodNumber):
            if(self.f[i]<self.globalMin):
                self.globalMin = self.f[i]
                for j in range(0,self.d):
                    self.globalParams[j] = self.foods[i][j]

    def init(self, index):
        for k in range(0,self.d):
            self.r = random.uniform(0,1)*32767 / (32767 + 1)
            self.foods[index][k] = self.r*(self.ub-self.lb)+ self.lb
            self.solution[k] = self.foods[index][k]

        self.f[index] = self.CalculateFunction(self.solution)
        self.fitness[index] = self.CalculateFitness(self.f[index])
        self.trial[index] = 0

    def initialize(self):
        for i in range(0, self.foodNumber):
            self.init(i)
        self.globalMin = self.f[0]
        for j in range(0, self.d):
            self.globalParams[j] = self.foods[0][1]

    def SendEmployeBees(self):
        for i in range(0, self.foodNumber):
            self.r = random.uniform(0,1) * 32767 / (32767 + 1)
            self.param2chance = int(self.r * self.d)
            self.r = random.uniform(0,1) * 32767 / (32767 + 1)
            self.neighbour = int(self.r * self.foodNumber)

            for j in range(0, self.d):
                self.solution[j] = self.foods[i][j]
            self.r = random.uniform(0,1) * 32767 / (32767 + 1)
            self.solution[self.param2chance] = self.foods[i][self.param2chance]+(self.foods[i][self.param2chance] - self.foods[self.neighbour][self.param2chance])*(self.r - 0.5)*2

            if(self.solution[self.param2chance] < self.lb):
                self.solution[self.param2chance] = self.lb

            if(self.solution[self.param2chance] > self.ub):
                self.solution[self.param2chance] = self.ub

            self.objValSol = self.CalculateFunction(self.solution)
            self.fitnessSol = self.CalculateFitness(self.objValSol)

            if(self.fitnessSol > self.fitness[i]):
                self.trial[i] = 0
                for k in range(0, self.d):
                    self.foods[i][k] = self.solution[k]
                self.f[i] = self.objValSol
                self.fitness[i] = self.fitnessSol
            else:
                self.trial[i] = self.trial[i]+1

    def CalculateProbabilities(self):
        maxfit = self.fitness[0]
        for i in range(0,self.foodNumber):
            if(self.fitness[i] > maxfit):
                maxfit = self.fitness[i]
        for j in range(0, self.foodNumber):
            self.prob[i] = (0.9 * (self.fitness[i]/maxfit))+0.1

    def SendOnLookerBees(self):
        t = 0
        i = 0
        while(t<self.foodNumber):
            self.r = random.uniform(0,1) * 32767 / (32767 + 1)
            if(self.r<self.prob[i]):
                t+=1
                self.r = random.uniform(0,1) * 32767 / (32767 + 1)
                self.param2chance = int(self.r * self.d)
                self.r = random.uniform(0,1) * 32767 / (32767 + 1)
                self.neighbour = int(self.r * self.foodNumber)
                while(self.neighbour == i):
                    self.r = random.uniform(0,1) * 32767 / (32767 + 1)
                    self.neighbour = int(self.r * self.foodNumber)
                for j in range(0, self.d):
                    self.solution[j] = self.foods[i][j]
                self.r = random.uniform(0,1) * 32767 / (32767 + 1)
                self.solution[self.param2chance] = self.foods[i][self.param2chance] + (self.foods[i][self.param2chance]
                                                                                       -self.foods[self.neighbour][self.param2chance])*\
                                                                                      (self.r-0.5)*2
                if(self.solution[self.param2chance] < self.lb):
                    self.solution[self.param2chance] = self.lb
                if(self.solution[self.param2chance] > self.ub):
                    self.solution[self.param2chance] = self.ub
                self.objValSol = self.CalculateFunction(self.solution)
                self.fitnessSol = self.CalculateFitness(self.objValSol)
                if(self.fitnessSol > self.fitness[i]):
                    self.trial[i] = 0
                    for k in range(0, self.d):
                        self.foods[i][k] = self.solution[k]
                    self.f[i] = self.objValSol
                    self.fitness[i] = self.fitnessSol
                else:
                    self.trial[i] = self.trial[i]+1
            i+=1
            if(i == self.foodNumber):
                i = 0

    def SendScoutBees(self):
        maxtrialindex = 0
        for i in range(0, self.foodNumber):
            if(self.trial[i] > self.trial[maxtrialindex]):
                maxtrialindex = i
        if(self.trial[maxtrialindex] >= self.limit):
            self.init(maxtrialindex)

    def CalculateFunction(self, sol):
        return self.Rastgrin(sol)

    def myFunction(self,sol):   ## You can write your own function
        return sol
    def sphere(self, sol):
        top = 0
        for j in range(0, self.d):
            top = top + sol[j]*sol[j]
        return top
    def Rosenbrok(self, sol):
        top = 0
        for j in range(0, (self.d-1)):
            top = top + 100 * math.pow(sol[j + 1] - math.pow(sol[j], 2), 2) + math.pow(sol[j] - 1, 2)
        return top

    def Griewank(self, sol):
        top1 = 0
        top2 = 1
        for j in range(0, self.d):
            top1 = top1 + math.pow(sol[j],2)
            top2 = top2 * math.cos(((sol[j] / math.sqrt(j + 1) * math.pi)) / 180)
        top = (1/4000) * top1 - top2 + 1
        return top

    def Rastgrin(self, sol):
        top = 0
        for j in range(0, self.d):
            top = top + (math.pow(sol[j], 2) - (10 * math.cos(2 * math.pi * sol[j])) + 10)
        return top


if __name__ == '__main__':
    aj = Bee()
    iter = 0
    run = 0
    mean = 0.00000000
    for run in range(aj.runtime):
        aj.initialize()
        aj.MemorizeBestSource()
        for iter in range(aj.maxCycle):
            aj.SendEmployeBees()
            aj.CalculateProbabilities()
            aj.SendOnLookerBees()
            aj.MemorizeBestSource()
            aj.SendScoutBees()
        for k in range(0, aj.d):
            print("Global Params ["+str(k+1)+"] : "+str(aj.globalParams[k]))
        print(str(run+1)+".run : "+str(aj.globalMin))
        aj.globalMins[run] = aj.globalMin
        mean = mean + aj.globalMin
    mean = mean/aj.runtime
    print("Means of "+ str(aj.runtime)+" runs: "+str(mean))
