import pickle
import constants as c
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import os

random.seed(c.random_seed)


def main():
    directory_normal = "saved_creatures/normal/"
    directory_obstacles = "saved_creatures/obstacles/"
    Create_World()
    for root, dirs, files in os.walk(directory_normal):
        for file_ in files:
            if '.pkl' in file_:
                with (open(os.path.join(root, file_), "rb")) as openfile:
                    while True:
                        try:
                            creature = pickle.load(openfile)
                        except EOFError:
                            break
                openfile.close()
                creature.Start_Simulation("GUI", bodyCreated=True)
                creature.Wait_For_Simulation_To_End()
                with open("new_world/normal/new_world_{0}".format(file_), 'wb') as f:
                    pickle.dump(creature.fitness, f)
                    f.close()

    for root, dirs, files in os.walk(directory_obstacles):
        for file_ in files:
            if '.pkl' in file_:
                with (open(os.path.join(root, file_), "rb")) as openfile:
                    while True:
                        try:
                            creature = pickle.load(openfile)
                        except EOFError:
                            break
                openfile.close()
                creature.Start_Simulation("GUI", bodyCreated=True, new_world=True)
                creature.Wait_For_Simulation_To_End()
                with open("new_world/obstacles/new_world_{0}".format(file_), 'wb') as f:
                    pickle.dump(creature.fitness, f)
                    f.close()

def Create_World():
    pyrosim.Start_SDF("data/world.sdf")

    if c.generate_obstacles:
        pos = c.block_pos
        for n_block in range(c.num_blocks):
            mass = random.uniform(0.2, 20)
            offset = random.choices([5, 6, 8, 10])[0]
            pyrosim.Send_Cube(name="Box{0}".format(str(n_block)), pos=pos, size=[4, 4, 4], mass=mass)
            pos = np.add(pos, [offset, offset, 0])

    pyrosim.End()


if __name__ == "__main__":
    main()