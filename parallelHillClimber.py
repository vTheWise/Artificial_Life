from solution import SOLUTION
import constants as c
import copy
import os
import random
import math
import numpy as np


class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        for file in os.listdir("./data"):
            if file.startswith("fitness") or file.startswith("brain") or file.startswith("body"):
                os.system("rm ./data/{0}".format(file))

        self.parents = dict()
        self.nextAvailableID = 0
        for p_size in range(c.populationSize):
            self.parents[p_size] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents, 'parents')
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()

        self.Mutate()

        self.Evaluate(self.children, 'children')

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
        parent_fitness = 0
        children_fitness = 0
        for k, v in self.parents.items():
            print('hi::', self.parents[k].fitness)
            for idx in range(c.numRobots):
                parent_fitness += self.parents[k].fitness[idx]
                children_fitness += self.children[k].fitness[idx]
            print('parent_fitness::', parent_fitness)
            print('children_fitness::', children_fitness)
            if parent_fitness > children_fitness:
                self.parents[k] = self.children[k]

    def Print(self):
        for k, v in self.parents.items():
            for idx in range(c.numRobots):
                print('\nrobot::', idx, ' ', 'parent fitness::', self.parents[k].fitness[idx],
                      'child fitness::', self.children[k].fitness[idx])

    def Show_Best(self):
        desired_fitness = 10000
        parent_fitness = 0
        best_solution = self.parents[list(self.parents.keys())[0]]
        for k, v in self.parents.items():
            for idx in range(c.numRobots):
                parent_fitness += self.parents[k].fitness[idx]
            if parent_fitness < desired_fitness:
                desired_fitness = parent_fitness
                best_solution = self.parents[k]
        best_solution.Start_Simulation("GUI")
        best_solution.Wait_For_Simulation_To_End()

    def Evaluate(self, solutions, generation):
        random_index = random.randint(0, math.floor(c.populationSize / 2))
        for p_size in range(c.populationSize):
            if generation == 'parents' and p_size == random_index:
                solutions[p_size].Start_Simulation("GUI")
            else:
                solutions[p_size].Start_Simulation("DIRECT")
        for p_size in range(c.populationSize):
            solutions[p_size].Wait_For_Simulation_To_End()
