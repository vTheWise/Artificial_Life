# Artificial_Life -> randomEvolution

In this version, I've changed the morphospace of the creatures that I created in the branch **random3D**. Additionally, the new creatures are now powered by an evolutionary algorithm that is fueled by a fitness function. The objective of the fitness function is to evolve locomotive capabilities in the creature in a manner that they try to chase a ball present in the 3D world. Creatures try to obtain this objective by minimizing the Euclidean distance between the ball and themselves. Let's say the position of a creature is pos1: [x1, y1, z1] and the position of the ball is pos2: [x2, y2, z2], then the distance between the two can be calculated using Euclidean method: (I've ignored the z-axis since it was not relevant for our creature's movement)

```
numpy.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
```

The best creatures in the population are searched with the help of parallel hill climbing method.

These new creatures also contain a random number of randomly shaped links with random sensor placement along the links and random motor placement along the joints. The blue color indicates the links without any sensor and the green color indicates the links with a touch sensor.

For reproducing the selected results, I have added seed values for both the numpy and random modules that I've been using in the program. These seeds are defined in **constant.py** as numpy_seed and random_seed, respectively. They can be changed before running the program.


## Morphospace


### Creature - Body

The creatures in our random 3D world are created using cuboids of random dimensions. Here's the body plan for our creatures:

![Body Plan](https://github.com/vTheWise/Artificial_Life/blob/randomEvolution/Diagrams/Body_Plan.jpg?raw=true)

Here's a sneak peek into the Create_Body() function used for generating creatures's bodies:

![Body Plan](https://github.com/vTheWise/Artificial_Life/blob/randomEvolution/Diagrams/Body_Creation_Plan.png?raw=true)


### Sensor Placements

The creatures in our random 3D world currently have touch sensors. Whether a link will have a sensor is defined with the help of a random choice function with a probability of 0.5. 


### Motor Placements

Motors are placed on the joints of the creatures.


### World

The world contains a spherical ball on a 3D plane. The world also contains a gravitational force.


### Creature - Brain

Our creatures contain a brain-like structure consisting of a neural network with sensor and motor neurons. Here's an illustration of how the brain and body of the creatures interact with each other:


![Brain-Body Control System](https://github.com/vTheWise/Artificial_Life/blob/randomEvolution/Diagrams/Control_System.jpg?raw=true)


In this network, every sensor neuron is connected with every motor neuron with a synapse having a random weight. Since, we are using a dense/fully-connected layer of neurons, the sensor on one part of the body will also affect the motors on other parts of the body.

![neural network](https://github.com/vTheWise/Artificial_Life/blob/randomEvolution/Diagrams/Brain.jpg?raw=true)


### Creature - Movement

Our creatures possess hinge joints of "revolution" type, each of which allows for free movement in 2 axes. The placement of joints can be better understood with the help of the following diagram: [source](https://docs.google.com/presentation/d/1zvZzFyTf8PBNjzQZx_gZk84aUntZo2bUKhpe78yT4OY/edit#slide=id.g10dad2fba23_2_428)

![Joints Placement](https://github.com/vTheWise/Artificial_Life/blob/randomEvolution/Diagrams/Joints%20Position.png?raw=true)

If the link is generated alongside z-axis (direction: [0, 0, 1] or [0, 0, -1]), then the joints on this link can move along the x-y plane. Similarly, if the link is generated alongside y-axis, the movement is allowed along the x-z plane. And, for the links generated alongside x-axis, free movement is allowed along the y-z plane.

In the code, I have randomly picked if our creature should be inspired by reptile designs or mammal designs, based on that the creature's link joints can move either in x-y or x-z plane, respectively. Similarly, a creature with spider legs can move in y-z plane, whereas creatures with quadruped legs can move in x-z plane. This distinction is shown in the body creation plan above.


# Evolution

Our creatures are evolved for chasing a ball in the 3D world. Here's an illustration of how the evolved creatures differ from the random ones:

![Evolution](https://github.com/vTheWise/Artificial_Life/blob/randomEvolution/Diagrams/Evolution.jpg?raw=true)

Initailly, a population of random creatures is generated. The number of creatures in the population is defined in constants.py as **populationSize**. A parallel hill climbing algorithm is used for evolving the creatures through multiple generations. The number of generations is defined in constants.py as **numberOfGenerations**. The creatures undergo a series of spawning, mutation, evaluation, and selection processes and the best creatures in each generation are selected as parents for reproducing in the next generation. Here's an illustration demonstrating the types of mutations that our creatures can undergo in each generation:


![Evolution](https://github.com/vTheWise/Artificial_Life/blob/randomEvolution/Diagrams/Mutation.jpg?raw=true)


## Demo
[Link to Youtube Video](https://youtube.com)

## To run the code:

**Dependencies**
```
> Python (version 3.x)
> Tested on MacBook Pro (14 inch, 2021) with MacOS Monterey Version 12.5
```

**Libraries**
```
> pip install pybullet
> pip install numpy
> pip install hide_warnings
> pip install matplotlib 
```

**Steps**
```
1. Clone this branch or download the code (zip file)
2. Unzip the file and navigate to the folder: 'Artificial_Life'
3. Either run "search.py" directly using any IDE or run the following command on your terminal:
```

```
python search.py
```

OR 

```
python3 search.py
```


## References:
1. This implementation is done as an assignment for the following MSAI course (Winter 2023): [Northwestern University - COMP_SCI 396: Artificial Life](https://www.mccormick.northwestern.edu/computer-science/academics/courses/descriptions/396-2.html). The instructor for this course is: [Dr. Sam Kriegman](https://skriegman.github.io/).
2. This assignment is built on top of the fundamental components developed as a part of an awesome course designed by [Prof. Josh Bongard](https://jbongard.github.io/). The course can be found on reddit: [Education in Evolutionary Robotics](https://www.reddit.com/r/ludobots/wiki/). 
3. This repository has forked and modded a version of [Pyrosim](https://github.com/jbongard/pyrosim.git). Pyrosim allows us to more easily send information to pybullet, and get information back from it.

