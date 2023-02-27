from solution import SOLUTION
import constants as c
import copy
import os
import matplotlib.pyplot as plt

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
            generations = [i for i in range(c.numberOfGenerations)]
            fig, ax = plt.subplots(1, 1)
            fig.set_size_inches(20, 10)
            fitness_for_generation = []
            best_fitness_values = []
            population = 0
            for idx in range (len(self.fitnessValues)):
                fitness_for_generation.append(self.fitnessValues[idx])
                population += 1
                if population == c.populationSize:
                    best_fitness_values.append(max(fitness_for_generation))
                    population = 0
            ax.plot(generations, best_fitness_values[:c.numberOfGenerations], 'go-', label='Training Accuracy (LSTM)')
            ax.set_title('Fitness Curve')
            ax.legend()
            ax.set_xlabel("Generations")
            ax.set_ylabel("Best Fitness Value")
            plt.yscale('symlog')
            plt.show()
            plt.savefig('fitnessCurve.png')
            plt.close(fig)

    def Show_Best(self):
        best_solution = self.parents[0]
        if len(self.parents) > 1:
            for k, v in self.parents.items():
                if self.parents[k].fitness > best_solution.fitness:
                    best_solution = self.parents[k]
        best_solution.Start_Simulation("GUI")

    def Evaluate(self, solutions, generation):
        for p_size in range(c.populationSize):
            if generation == 'parents' and self.nextAvailableID == c.populationSize:
                solutions[p_size].Start_Simulation("GUI")
            elif generation == 'children':
                solutions[p_size].Start_Simulation("DIRECT", isMutation=True)
            else:
                solutions[p_size].Start_Simulation("DIRECT")
        for p_size in range(c.populationSize):
            self.fitnessValues.append(solutions[p_size].Wait_For_Simulation_To_End())


