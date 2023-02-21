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
1. [Northwestern University - COMP_SCI 396: Artificial Life](https://www.mccormick.northwestern.edu/computer-science/academics/courses/descriptions/396-2.html). 
2. [Education in Evolutionary Robotics](https://www.reddit.com/r/ludobots/wiki/). 
3. [Pyrosim](https://github.com/jbongard/pyrosim.git) (allows us to more easily send information to pybullet, and get information back from it)

