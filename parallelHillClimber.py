from solution import SOLUTION
import constants as c
import copy
import os
import matplotlib.pyplot as plt
import random
from matplotlib import ticker
import numpy as np
import statistics
from itertools import chain
import pickle


random.seed(c.random_seed)

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        for file in os.listdir("./data"):
            if file.startswith("fitness") or file.startswith("brain") or (file.startswith("body")):
                os.system("rm ./data/{0}".format(file))

        self.parents = dict()
        self.nextAvailableID = 0
        for p_size in range(c.populationSize):
            self.parents[p_size] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        self.fitnessValues = []

    def Evolve(self):
        self.Evaluate(self.parents, 'parents')
        for currentGeneration in range(c.numberOfGenerations):
            print('currentGeneration:::', currentGeneration)
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
            self.children[k].parentID = self.parents[k].myID
            self.children[k].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1


    def Mutate(self):
        for k, v in self.children.items():
            self.children[k].Mutate()

    def Select(self):
        for k, v in self.parents.items():
            if self.parents[k].fitness < self.children[k].fitness:
                self.parents[k] = self.children[k]

    def Print(self):
        for k, v in self.parents.items():
            print('\nparent fitness::', self.parents[k].fitness, 'child fitness::', self.children[k].fitness)


    def Plot_Fitness(self):
        if self.fitnessValues:
            with open('data/fitnessValues{0}_{1}.pkl'.format(str(c.random_seed), str(c.numpy_seed)), 'wb') as f:
                pickle.dump(self.fitnessValues, f)
                f.close()

            # generations = [i for i in range(c.numberOfGenerations)]
            # fig, ax = plt.subplots(1, 1)
            # fig.set_size_inches(20, 10)
            # fitness_for_generation = []
            # best_fitness_values = []
            # avg_fitness_values = []
            # population = 0
            # for idx in range (len(self.fitnessValues)):
            #     fitness_for_generation.append(self.fitnessValues[idx])
            #     population += 1
            #     if population == c.populationSize:
            #         best_fitness_values.append(max(fitness_for_generation))
            #         avg_fitness_values.append(statistics.fmean(fitness_for_generation))
            #         population = 0
            #
            # ax.plot(generations, best_fitness_values[:c.numberOfGenerations], 'go-', label='Best fitness values')
            # ax.plot(generations, avg_fitness_values[:c.numberOfGenerations], 'ro-', label='Average fitness values')
            # ax.set_title('Fitness Curve (Fitness: {0})'.format(c.fitnessFunction))
            # ax.legend(loc='upper left')
            # ax.set_xlabel("Generations")
            # ax.set_ylabel("Fitness Values")
            # plt.suptitle('random.seed = {0}\nnumpy.random.seed = {1}'.format(c.random_seed, c.numpy_seed))
            # plt.ylim(min(chain(best_fitness_values[:c.numberOfGenerations], avg_fitness_values[:c.numberOfGenerations]))-1,
            #              max(chain(best_fitness_values[:c.numberOfGenerations], avg_fitness_values[:c.numberOfGenerations]))+1)
            # plt.yticks(np.arange(min(chain(best_fitness_values[:c.numberOfGenerations], avg_fitness_values[:c.numberOfGenerations]))-1.0,
            #                      max(chain(best_fitness_values[:c.numberOfGenerations], avg_fitness_values[:c.numberOfGenerations]))+1.0, 0.5))
            # ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))
            # plt.show()
            # plt.savefig('fitnessCurve.png')
            # plt.close(fig)

    def Show_Best(self):
        best_solution = self.parents[0]
        if len(self.parents) > 1:
            for k, v in self.parents.items():
                if self.parents[k].fitness > best_solution.fitness:
                    best_solution = self.parents[k]
        best_solution.Start_Simulation("GUI", bodyCreated=True)
        with open('data/fitnessValues{0}_{1}_best.pkl'.format(str(c.random_seed), str(c.numpy_seed)), 'wb') as f:
            pickle.dump(best_solution, f)
            f.close()

    def Evaluate(self, solutions, generation):
        display_idx = random.choices(range(c.populationSize), k=c.num_simulation_initial_popluation)
        for p_size in range(c.populationSize):
            if generation == 'parents' and p_size in display_idx:
                solutions[p_size].Start_Simulation("GUI")
            elif generation == 'children':
                solutions[p_size].Start_Simulation("DIRECT", bodyCreated=True)
            else:
                solutions[p_size].Start_Simulation("DIRECT")
        for p_size in range(c.populationSize):
            self.fitnessValues.append(solutions[p_size].Wait_For_Simulation_To_End())


