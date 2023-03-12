# Artificial_Life -> roboBall

In this version, I have created a blue-green biped creature using pybullet and pyrosim. The blue color indicates the links without any sensor and the green color indicates the links with a touch sensor. Additionally, there is a spherical ball in this environment too.
The creature is evolved to get closer to the ball, using its distance from the ball as the fitness criterion.
To calculate this distance, I have first fetched the position of the robot and ball using pybullet's *getBasePositionAndOrientation* function. This function returns a tuple of tuple, in which the first tuple contains the xyz-coordinates of the corresponding object. 
Let's say the position of robot is pos1: [x1, y1, z1] and the position of ball is pos2: [x2, y2, z2], then the distance between the two can be calculated using Euclidean method: (I've ignored the z-axis since it was not relevant for our creature's movement)

```
numpy.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
```

I've ran the program for 20 generations and each generation contained 20 creatures (population size). These parameters can be modified in **constants.py** by updating *numberOfGenerations* or *populationSize* variables, respectively.

## [Link to Youtube Video](https://www.youtube.com/watch?v=KXEfp0kZ43k&list=PLgzW_9Hyu07Gi0BDSIlZUJI9elMqb2wzR&index=13)
When the program is run, a simulation window will pop-up showing the fifth creature from the first generation. After that all the generations will be evolved in the background and the fitness of parents and children can be seen on the terminal. At last, the simulation window will pop-up again to show the best creature.

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
> pip install matplotlib (optional)
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

