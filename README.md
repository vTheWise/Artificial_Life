# Artificial_Life -> kinematicSnakes

In this version, I am generating a kinematic chain (jointed snake) with a random number of randomly shaped links with random sensor placement along the chain. The blue color indicates the links without any sensor and the green color indicates the links with a touch sensor. The number of randomly generated snakes is defined in **constants.py** as 50, and it can be changed before running the program. The number of links to be generated is defined as a random function between the given range in the constructor of **solution.py** as self.numLinks. This range can also be updated before running the program.


## [Link to Youtube Video](https://youtube.com/shorts/AInUh_sMSmk?feature=share)


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

