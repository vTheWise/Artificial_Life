import constants as c
import matplotlib.pyplot as plt
import pickle
import statistics
from matplotlib import ticker
import os
from operator import itemgetter

def main():
    directory_normal = "saved_fitness/normal/"
    directory_obstacles = "saved_fitness/obstacles/"
    normal_files, obstacle_files = get_KV_pairs()
    normal_fitness = []
    obstacle_fitness = []
    for file in normal_files:
        with (open("{0}{1}".format(directory_normal, file["filename"]), "rb")) as openfile:
            while True:
                try:
                    fitnessValues = pickle.load(openfile)
                    normal_fitness.append({"filename": file["filename"], "random_seed": file["random_seed"],
                                           "numpy_seed": file["numpy_seed"],
                                           "fitnessValues": fitnessValues[:c.numberOfGenerations*c.populationSize]})
                except EOFError:
                    break
        openfile.close()
    for file in obstacle_files:
        with (open("{0}{1}".format(directory_obstacles, file["filename"]), "rb")) as openfile:
            while True:
                try:
                    fitnessValues = pickle.load(openfile)
                    obstacle_fitness.append({"filename": file["filename"], "random_seed": file["random_seed"],
                                           "numpy_seed": file["numpy_seed"],
                                             "fitnessValues": fitnessValues[:c.numberOfGenerations*c.populationSize]})
                except EOFError:
                    break
        openfile.close()
    generate_plot(normal_fitness, obstacle_fitness)
    new_world()

def get_KV_pairs():
    normal_files =  [
        {"filename": "fitnessValues10_7.pkl", "random_seed": 10, "numpy_seed": 7},
        {"filename": "fitnessValues54_42.pkl", "random_seed": 54, "numpy_seed": 42},
        {"filename": "fitnessValues125_75.pkl", "random_seed": 125, "numpy_seed": 75},
        {"filename": "fitnessValues287_275.pkl", "random_seed": 287, "numpy_seed": 275},
        {"filename": "fitnessValues334_371.pkl", "random_seed": 334, "numpy_seed": 371}
    ]

    obstacle_files = [
        {"filename": "fitnessValuesObstacles10_7.pkl", "random_seed": 10, "numpy_seed": 7},
        {"filename": "fitnessValuesObstacles54_42.pkl", "random_seed": 54, "numpy_seed": 42},
        {"filename": "fitnessValuesObstacles125_75.pkl", "random_seed": 125, "numpy_seed": 75},
        {"filename": "fitnessValuesObstacles287_275.pkl", "random_seed": 287, "numpy_seed": 275},
        {"filename": "fitnessValuesObstacles334_371.pkl", "random_seed": 334, "numpy_seed": 371}
    ]
    return normal_files, obstacle_files

def generate_plot(normal_fitness, obstacle_fitness):
    generations = [i for i in range(c.numberOfGenerations)]
    fitness_for_population = []
    best_fitness_gen_normal = []
    avg_fitness_gen_normal = []
    best_fitness_values_normal = []
    avg_fitness_values_normal = []
    best_fitness_gen_obstacle = []
    avg_fitness_gen_obstacle = []
    best_fitness_values_obstacle = []
    avg_fitness_values_obstacle = []
    population = 0

    for fitness in normal_fitness:
        for idx in range(len(fitness["fitnessValues"])):
            fitness_for_population.append(fitness["fitnessValues"][idx])
            population += 1
            if population == c.populationSize:
                best_fitness_gen_normal.append(max(fitness_for_population))
                avg_fitness_gen_normal.append(statistics.fmean(fitness_for_population))
                population = 0
        best_fitness_values_normal.append({"filename": fitness["filename"], "fitness": best_fitness_gen_normal,
                                           "random_seed": fitness["random_seed"],
                                           "numpy_seed": fitness["numpy_seed"]})
        avg_fitness_values_normal.append({"filename": fitness["filename"], "fitness": avg_fitness_gen_normal,
                                          "random_seed": fitness["random_seed"],
                                          "numpy_seed": fitness["numpy_seed"]})
        fitness_for_population = []
        best_fitness_gen_normal = []
        avg_fitness_gen_normal = []

    for fitness in obstacle_fitness:
        for idx in range(len(fitness["fitnessValues"])):
            fitness_for_population.append(fitness["fitnessValues"][idx])
            population += 1
            if population == c.populationSize:
                best_fitness_gen_obstacle.append(max(fitness_for_population))
                avg_fitness_gen_obstacle.append(statistics.fmean(fitness_for_population))
                population = 0
        best_fitness_values_obstacle.append({"filename": fitness["filename"], "fitness": best_fitness_gen_obstacle,
                                           "random_seed": fitness["random_seed"],
                                           "numpy_seed": fitness["numpy_seed"]})
        avg_fitness_values_obstacle.append({"filename": fitness["filename"], "fitness": avg_fitness_gen_obstacle,
                                          "random_seed": fitness["random_seed"],
                                          "numpy_seed": fitness["numpy_seed"]})
        fitness_for_population = []
        best_fitness_gen_obstacle = []
        avg_fitness_gen_obstacle = []

    plot_best_fitness(best_fitness_values_normal, best_fitness_values_obstacle, generations)
    plot_avg_fitness(avg_fitness_values_normal, avg_fitness_values_obstacle, generations)

def plot_best_fitness(best_fitness_values_normal, best_fitness_values_obstacle, generations):
    fig, (ax1, ax2) = plt.subplots(2)
    fig.set_size_inches(15, 10)
    fig.subplots_adjust(hspace=0.5)
    plot_num = 1
    for best_normal_fitness in best_fitness_values_normal:
        style = get_plot_style(plot_num)
        ax1.plot(generations, best_normal_fitness["fitness"], style,
                 label='random seed: {0}\nnumpy_seed: {1}'.format(best_normal_fitness["random_seed"],
                                                                  best_normal_fitness["numpy_seed"]))
        plot_num += 1

    plot_num = 1
    for best_obstacle_fitness in best_fitness_values_obstacle:
        style = get_plot_style(plot_num)
        ax2.plot(generations, best_obstacle_fitness["fitness"], style,
                 label='random seed: {0}\nnumpy_seed: {1}'.format(best_obstacle_fitness["random_seed"],
                                                                  best_obstacle_fitness["numpy_seed"]))
        plot_num += 1

    ax1.set_title('Fitness Curve (Fitness: {0})\nNormal Environment'.format(c.fitnessFunction))
    ax2.set_title('Fitness Curve (Fitness: {0})\nEnvironment with Obstacle'.format(c.fitnessFunction))

    ax1.legend(loc='upper right', bbox_to_anchor=(1.125, 1.2), fancybox=True, shadow=True)
    ax2.legend(loc='upper right', bbox_to_anchor=(1.125, 1.2), fancybox=True, shadow=True)

    ax1.set_xlabel("Generations")
    ax2.set_xlabel("Generations")

    ax1.set_ylabel("Best Fitness Values")
    ax2.set_ylabel("Best Fitness Values")

    ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))
    ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))

    ax1.relim()
    ax2.relim()

    ax1.autoscale()
    ax2.autoscale()

    plt.savefig('Diagrams/fitness_curve_best.png')
    plt.show()

def plot_avg_fitness(avg_fitness_values_normal, avg_fitness_values_obstacle, generations):
    fig, (ax1, ax2) = plt.subplots(2)
    fig.set_size_inches(15, 10)
    fig.subplots_adjust(hspace=0.5)
    plot_num = 1
    for avg_normal_fitness in avg_fitness_values_normal:
        style = get_plot_style(plot_num)
        ax1.plot(generations, avg_normal_fitness["fitness"], style,
                 label='random seed: {0}\nnumpy_seed: {1}'.format(avg_normal_fitness["random_seed"],
                                                                  avg_normal_fitness["numpy_seed"]))
        plot_num += 1

    plot_num = 1
    for avg_obstacle_fitness in avg_fitness_values_obstacle:
        style = get_plot_style(plot_num)
        ax2.plot(generations, avg_obstacle_fitness["fitness"], style,
                 label='random seed: {0}\nnumpy_seed: {1}'.format(avg_obstacle_fitness["random_seed"],
                                                                  avg_obstacle_fitness["numpy_seed"]))
        plot_num += 1

    ax1.set_title('Fitness Curve (Fitness: {0})\nNormal Environment'.format(c.fitnessFunction))
    ax2.set_title('Fitness Curve (Fitness: {0})\nEnvironment with Obstacle'.format(c.fitnessFunction))

    ax1.legend(loc='upper right', bbox_to_anchor=(1.125, 1.2), fancybox=True, shadow=True)
    ax2.legend(loc='upper right', bbox_to_anchor=(1.125, 1.2), fancybox=True, shadow=True)

    ax1.set_xlabel("Generations")
    ax2.set_xlabel("Generations")

    ax1.set_ylabel("Average Fitness Values")
    ax2.set_ylabel("Average Fitness Values")

    ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))
    ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))

    ax1.relim()
    ax2.relim()

    ax1.autoscale()
    ax2.autoscale()

    plt.savefig('Diagrams/fitness_curve_avg.png')
    plt.show()


def get_plot_style(plot_num):
    plot_style = 'b.-'
    if plot_num == 1:
        plot_style = 'g.-'
    elif plot_num == 2:
        plot_style = 'r.-'
    elif plot_num == 3:
        plot_style = 'c.-'
    elif plot_num == 4:
        plot_style = 'm.-'
    elif plot_num == 5:
        plot_style = 'b.-'
    return plot_style

def new_world():
    directory_normal = "new_world/normal/"
    directory_obstacles = "new_world/obstacles/"
    normal_fitness = []
    obstacle_fitness = []
    for root, dirs, files in os.walk(directory_normal):
        for file_ in files:
            if '.pkl' in file_:
                with (open(os.path.join(root, file_), "rb")) as openfile:
                    while True:
                        try:
                            fitness = pickle.load(openfile)
                            normal_fitness.append({"file": file_, "fitness": fitness})
                        except EOFError:
                            break
                openfile.close()

    for root, dirs, files in os.walk(directory_obstacles):
        for file_ in files:
            if '.pkl' in file_:
                with (open(os.path.join(root, file_), "rb")) as openfile:
                    while True:
                        try:
                            fitness = pickle.load(openfile)
                            obstacle_fitness.append({"file": file_, "fitness": fitness})
                        except EOFError:
                            break
                openfile.close()

    sorted_normal_fitness = sorted(normal_fitness, key=itemgetter('file'))
    sorted_obstacle_fitness = sorted(obstacle_fitness, key=itemgetter('file'))
    x = []
    y1 = []
    y2 = []
    for idx, snf in enumerate(sorted_normal_fitness):
        x.append('Creature{0}'.format(str(idx+1)))
        y1.append(snf['fitness'])
    for sof in sorted_obstacle_fitness:
        y2.append(sof['fitness'])
    fig = plt.figure(facecolor='white')
    fig.set_size_inches(10, 8.5)
    ax = fig.add_subplot()
    plt.rcParams["font.weight"] = "bold"
    ax.bar(x, y1, color='r')
    ax.bar(x, y2, bottom=y1, color='b')
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", label_type='center', color='white', fontsize=10)
    plt.xlabel("Creatures")
    plt.ylabel("Fitness in New World")
    plt.legend(["Creature Evolved without Obstacles", "Creature Evolved with Obstacles"], loc='upper left',
               bbox_to_anchor=(0, 1), fancybox=True, shadow=True)
    plt.title('Fitness Curve (Fitness: {0})\nNew World'.format(c.fitness_new_world))
    plt.savefig('Diagrams/new_world_evaluate')
    plt.show()

if __name__ == "__main__":
    main()
