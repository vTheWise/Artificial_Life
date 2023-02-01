from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        for file in os.listdir("./data"):
            if file.startswith("fitness") or file.startswith("brain"):
                os.system("rm ./data/{0}".format(file))

        self.parents = dict()
        self.nextAvailableID = 0
        for p_size in range(c.populationSize):
            self.parents[p_size] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()

        self.Mutate()

        self.Evaluate(self.children)

        self.Print()

        self.Select()

    def Spawn(self):
        self.children = dict()
        for k, v in self.parents.items():
            self.children[k] = copy.deepcopy(self.parents[k])
            self.children[k].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1


    def Mutate(self):
        for k, v in self.children.items():
            self.children[k].Mutate()

    def Select(self):
        for k, v in self.parents.items():
            if self.parents[k].fitness > self.children[k].fitness:
                self.parents[k] = self.children[k]

    def Print(self):
        for k, v in self.parents.items():
            print('\nparent fitness::', self.parents[k].fitness, 'child fitness::', self.children[k].fitness)

    def Show_Best(self):
        lowest_fitness = 0
        best_solution = self.parents[list(self.parents.keys())[0]]
        for k, v in self.parents.items():
            if self.parents[k].fitness < lowest_fitness:
                lowest_fitness = self.parents[k].fitness
                best_solution = self.parents[k]
        best_solution.Start_Simulation("GUI")

    def Evaluate(self, solutions):
        for p_size in range(c.populationSize):
            solutions[p_size].Start_Simulation("DIRECT")
        for p_size in range(c.populationSize):
            solutions[p_size].Wait_For_Simulation_To_End()


