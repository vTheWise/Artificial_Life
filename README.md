# Artificial Life

## Teaser (10 sec, GIF)

## Summary (2 mins, video)

## B-Roll (Extra Footage of Random and Evolved Creatures)

## Background

"Progress in physics comes by taking things apart; in computation by putting things together. We might have had an analytic science of computation, but
as it worked out, we learned more from putting together thermostats and computers than we did from taking apart monkey brains and frog eyes." I love this quote by Danny Hillis. It highlights the importance of "learning through examples". During the first weeks of our class [COMP_SCI 396: Artificial Life](https://www.mccormick.northwestern.edu/computer-science/academics/courses/descriptions/396-2.html), we discussed a quote found on [Richard Feynman's](https://en.wikipedia.org/wiki/Richard_Feynman) blackboard at the time of his death: "What I cannot create, I do not understand." This has been the philosophy of my life from at least the last decade or so. Like many thinkers before me, I have been bewildered by some of the very basic questions of life and existence, but I couldn't find any reasoanble approach to seeking answers for those questions - until, I stumbled upon an incredible book written by Steven Levy on "Artificial Life". 

Christopher Langton defines artificial life as 'The study of natural life, where "nature" is understood to include, rather than to exclude, human beings and their artifacts.' There are two tracks of artificial life. The more ambitious goal is the creation of living systems - the equivalent of biological alchemy. The other quest, closer to hand, is the simulation — in some cases the duplication — of life’s unique processes, in order to heighten our understanding of natural life and of possible alternative forms of life. This is my first simulation project in artificial life. In the different branches of this repository, you'll find the bits and pieces that led me to this final project.

## Motivation

One biological theorem, postulated by R. A. Fisher, conjectured that evolution proceeded by steady improvements in fitness. This is an equivalent to the so-called hill climbing technique used by certain computer optimization procedures, such as learning in neural network simulations. Because each generation was supposedly slightly fitter than the previous one, a graph illustrating this progress would show line angling upward, as though the fitness of the species were engaged in scaling a peak. 

![Evolutionary Hill Climbing](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/hill_climbing.png?raw=true)


Biologists studying the problem had created a more complicated, multidimensional map of the way that a species might evolve. This “adaptive landscape,”’ first postulated by Sewall Wright, represented the space of all possible genetic combinations. It was filled with bumps, peaks, valleys, and spikes. The gene pool of an entire population resided at a single area on this landscape. The higher the ground, the fitter the population would be if it found its way there. When the terrain was fairly level, a population theoretically engaged in a “random walk,”’ with the effects of crossover and mutation moving its genetic composition to different places, until it found an ascending plane. From that point, the more fit individuals within the population would push fitness higher, and the rest of the population would follow. 

But, if hill climbing was indeed the method nature used to achieve higher fitness, the discovery of the highest ground could not always be assumed. Once the population scaled a medium-size peak, it tended to get stuck. This was due to the built-in reluctance of a population to decrease its fitness, which would be necessary in order to search the landscape for an even higher peak. The population would remain fat and happy on its hill but miss out on the mountains that lay somewhere else on the chart. The population was then “stuck on a local maximum” with no incentive to make the giant evolutionary leaps that push life toward more complexity.

![Local Maxima](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/local_optima.png?raw=true)

“If evolution is a hill-climbing technique, why doesn’t it seem to have problems that we know hill-climbing techniques suffer from?” ‘‘Why is evolution so much more powerful than any other hill-climbing technique? Why is it able to evolve much more complicated things?”

One possible explanation can be given in terms of ‘‘evolutionary arms races" -  a situation where two populations of differing species were set against each other, in predator-prey or host-parasite relationships. If a host population Evolved strategic traits to foil the parasite, the parasite would in turn evolve a strategy to compensate and the cycle would continue causing continuous improvements (i.e., evolution!). William Hamilton, among others, had suggested that the presence of parasites might have been integral in accelerating the pace of evolution to a rate capable of yielding its present diversity and complexity.


![Coevolution](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/coevolution.jpg?raw=true)

**This chain of thoughts led me to question the role of environmental hardships in shaping the path of evolution. I wondered if the creatures who have to face harsh environmental conditions evolve better than those who do not.**


## Hypothesis

### Null Hypothesis

```
H0: Harsh environmental conditions do not have any positive impact on the evolutionary process.
```

### Alternative Hypothesis

```
H': Harsh environmental conditions do have positive impact on the evolutionary process.
```

## Method 

In order to test my hypothesis, I followed a controlled testing set-up. I first ran an evolutionary search (PHC - details are mentioned below) for 500 generations with a population size of 10. The environment was plain and simple without any obstacles. The fitness objective for the creatures was to go as close to the balls as possible. I ran this evolutionary process 5 times using a different random seed each time. I saved the best creatures from every run (the corresponding pickle files are available in the **saved_creatures** folder. Next, keeping everything exactly the same, I ran the evolutionary process for another set of 5 times (the random seeds were the same that I used for the previous 5 runs). The only difference this time was that there was an obstacle in the shape of staircases between the creatures and the balls. This can. be seen as a control-group for testing my hypothesis. The creatures were supposed to learn how to reach to the balls avoiding/climbing the obstacle. Again I saved the best creatures from each run. Finally, I created a new world/environment with different kinds of obstacles in it and tested the saved best creatures from the original experiment as well as the control-group experiment for the distance that they traveled in the new world. The results are presented below followed by a short discussion. 

![Method](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/method.jpg?raw=true)

## An Introduction to Our Simulated World and its Creatures

### World/Environment

The world contains some spherical balls on a 3D plane. The world also contains a gravitational force. In the normal setting, there is no other object in the world. In the "harsh environment" setting, there is a staircase structure present between the creature and the balls. The creature is supposed to either climb the staircases and move towards the balls or learn how to avoid the staircases while moving towards the balls. In the final settings, a different kind of "harsh environment" is introduced. Basically, there are cubes with different masses on the plane, some of them can be moved away, rest of them cannot. Creatures are supposed to either move the cubes away from their path or learn how to avoid them while moving towards the balls.


### Creature - Body

Our creatures are made up of cubes of different sizes. Here's the body plan used for generating a typical creature:

![Body Plan](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/Body_Plan.png?raw=true)

It's difficult to imagine all types of possible creature bodies, since our program randomly generates the morphologies. However, the following diagram captures the essence of the genotype of our creatures:

![Body](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/body.jpg?raw=true)


### Sensor Placements

The creatures in our random 3D world currently have touch sensors. Whether a link will have a sensor is defined with the help of a random choice function with a probability of 0.5.


### Motor Placements

Motors are placed on the joints of the creatures.

### Creature - Brain

Our creatures contain a brain-like structure consisting of a neural network with sensor and motor neurons.  Here's an illustration of how the brain and body of the creatures interact with each other:

![Brain-Body Control System](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/Control_System.jpg?raw=true)

In this network, every sensor neuron is connected with every motor neuron with a synapse having a random weight. Since, we are using a dense/fully-connected layer of neurons, the sensor on one part of the body will also affect the motors on other parts of the body.

![neural network](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/Brain.jpg?raw=true)


### Creature - Movement

Our creatures possess hinge joints of "revolute" type, each of which allows for free movement in 2 axes. The placement of joints can be better understood with the help of the following diagram: [source](https://docs.google.com/presentation/d/1zvZzFyTf8PBNjzQZx_gZk84aUntZo2bUKhpe78yT4OY/edit#slide=id.g10dad2fba23_2_428)

![Joints Placement](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/Joints%20Position.png?raw=true)

If the link is generated alongside z-axis (direction: [0, 0, 1] or [0, 0, -1]), then the joints on this link can move along the x-y plane. Similarly, if the link is generated alongside y-axis, the movement is allowed along the x-z plane. And, for the links generated alongside x-axis, free movement is allowed along the y-z plane.


### Evolution (Parallel Hill Climbing)

he objective of the fitness function is to evolve locomotive capabilities in the creature in a manner that they try to chase some balls present in the 3D world. Creatures try to obtain this objective by minimizing the Euclidean distance between the ball and themselves. Let's say the position of a creature is pos1: [x1, y1, z1] and the position of the ball is pos2: [x2, y2, z2], then the distance between the two can be calculated using Euclidean method:

```
numpy.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2)
```

The best creatures in the population are searched with the help of parallel hill climbing method. These new creatures also contain a random number of randomly shaped links with random sensor placement along the links and random motor placement along the joints. The blue color indicates the links without any sensor and the green color indicates the links with a touch sensor.

Here's a flow diagram depicting different stages:

![PHC](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/phc.jpg?raw=true)

Initailly, a population of random creatures is generated. The number of creatures in the population is defined in constants.py as **populationSize**. A parallel hill climbing algorithm is used for evolving the creatures through multiple generations. The number of generations is defined in constants.py as **numberOfGenerations**. The creatures undergo a series of spawning, mutation, evaluation, and selection processes and the best creatures in each generation are selected as parents for reproducing in the next generation. During each generation, creatures are selected by a direct comparison with their respective parent. Other creatures in the population do not affect the selection process directly. The selection process can be understood with the help of the following diagram:

![Selection](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/selection.jpg?raw=true)


 Here's an illustration demonstrating the types of mutations that our creatures can undergo in each generation:

![Mutations](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/Mutation.jpg?raw=true)


Here's an illustration of how the evolved creatures differ from the random ones:

![Evolution](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/Evolution.jpg?raw=true)



## Results

### Plots

Best fitness in each generation:

![best fitness](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/fitness_curve_best.png?raw=true)

Average fitness in each generation:

![avg fitness](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/fitness_curve_avg.png?raw=true)


## Discussion



## Conclusion


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

**To Generate the Graphs**

```
python plot_graphs.py
```

**To Simulate the new World**

```
python new_world_evaluation.py
```

## Important Notes
```
* For reproducing the selected results, I have added seed values for both the numpy and random modules that I've been using in the program. These seeds are defined in **constant.py** as numpy_seed and random_seed, respectively. They can be changed before running the program.

* If you want to generate staircase obstacles, you need to set generate_stairs in constants.py to True. 
```


## References:
1. This implementation is done as an assignment for the following MSAI course (Winter 2023): [Northwestern University - COMP_SCI 396: Artificial Life](https://www.mccormick.northwestern.edu/computer-science/academics/courses/descriptions/396-2.html). The instructor for this course is: [Dr. Sam Kriegman](https://skriegman.github.io/).
2. This assignment is built on top of the fundamental components developed as a part of an awesome course designed by [Prof. Josh Bongard](https://jbongard.github.io/). The course can be found on reddit: [Education in Evolutionary Robotics](https://www.reddit.com/r/ludobots/wiki/). 
3. This repository has forked and modded a version of [Pyrosim](https://github.com/jbongard/pyrosim.git). Pyrosim allows us to more easily send information to pybullet, and get information back from it.
4. Here's an awesome book by Steven Levy: ["Artificial Life: A Report from the Frontier Where Computers Meet Biology"](https://www.goodreads.com/book/show/737831.Artificial_Life).
5. If you're still wondering what Artificial Life is, here's a perfect read for you: [A New Definition of Artificial Life](https://www.fisica.unam.mx/personales/mir/langton.pdf)

