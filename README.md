# Artificial_Life -> random3D

In this version, I've expanded the design space ("morphospace") of the kinematic chain that I created in the branch **kinematicSnakes** by allowing the chain to branch in 3D. These new creatures also contain a random number of randomly shaped links with random sensor placement along the links and random motor placement along the joints. The blue color indicates the links without any sensor and the green color indicates the links with a touch sensor. The number of randomly generated creatures is defined in **constants.py** as 100, and it can be changed before running the program. The number of links to be generated is defined as a random function between the given range in the constructor of **solution.py** as self.maxNumLinks. This range can also be updated before running the program.

## Sensor Placements

The creatures in our random3D world currently have touch sensors. Whether a link will have a sensor is defined with the help of a probabilty threshold and a random number generating function withing the range: [0, 1). After each link is created, the random function is called and if the generated number is **less than** the threshold defined in the constructor of Solution.py as "self.probSensor = 0.5", then the corresponding link will have a sensor. Therefore, the probability of each link having a sensor is roughly 0.5 (or 50%). Practically, it is a little bit higher than 0.5, since the range of the random number generating function is inclusive of the lower bound 0 and exclusive of the upper bond 1, hence it is a bit left-skewed. In other words, [0.0,0.5) is a bigger infinite set of numbers than (0.5,1.0), because the 0.0 is included and the 1.0 is excluded.

## Motor Placements

Similar to sensors, placement of the motors is also decided with the help of a random number generating function and a probability threshold defined as " self.probMotor = 0.7" in Solution.py.

## Morphospace

### World

The world is currently empty with no objects present in it except for a 3D plane. The world does contain a gravitational force.

### Creature - Body

The creatures in our random3D world are created using cuboids of random dimensions. 

![Cuboid faces and the corresponding direction vectors](https://github.com/vTheWise/Artificial_Life/blob/random3D/Cube_Faces.jpg?raw=true)

The limbs of the creatures are added randomly with the help of a couple of probability thresholds and random number generating functions.
The variable **self.probExtend** in Solution.py acts as a probability threshold to determine whether the next link will be created on the same face. Similarly another variable **self.probSwitchFace** in the same class works as a probability threshold to determine whether the next link will be created in a different face. A dictionary **self.probNextFace** is defined with the directions (such as, [1,0,0] for front face, [0,-1,0] for left face, etc.) as the keys and a list of self.probExtend and self.probSwitchFace variables as values. The probability of extending in the opposite face is 0. So, if the current link is generated on the front face, the next link cannot be generated in the back face. Similarly, if the current link was generated on the left face, the next link cannot be generated on the right face. This rule preserves the natural growth of the creature avoiding link-intersections and link-pooling.

### Creature - Brain

### Creature - Movement

## Demo
[Link to Youtube Video]

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

