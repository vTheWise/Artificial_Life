from solution import SOLUTION
import constants as c
import copy
import os
import random
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
            filename = 'data/fitnessValuesObstacles{0}_{1}.pkl'.format(str(c.random_seed), str(c.numpy_seed)) \
                if c.generate_stairs \
                else 'data/fitnessValues{0}_{1}.pkl'.format(str(c.random_seed), str(c.numpy_seed))
            with open(filename, 'wb') as f:
                pickle.dump(self.fitnessValues, f)
                f.close()

    def Show_Best(self):
        best_solution = self.parents[0]
        if len(self.parents) > 1:
            for k, v in self.parents.items():
                if self.parents[k].fitness > best_solution.fitness:
                    best_solution = self.parents[k]
        best_solution.Start_Simulation("GUI", bodyCreated=True)
        filename = 'data/fitnessValuesObstacles{0}_{1}_best.pkl'.format(str(c.random_seed), str(c.numpy_seed)) \
            if c.generate_stairs \
            else 'data/fitnessValues{0}_{1}_best.pkl'.format(str(c.random_seed), str(c.numpy_seed))
        with open(filename, 'wb') as f:
            pickle.dump(best_solution, f)
            f.close()
        best_solution.Wait_For_Simulation_To_End()

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


