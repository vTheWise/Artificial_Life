# Artificial Life

## Background

"Progress in physics comes by taking things apart; in computation by putting things together. We might have had an analytic science of computation, but
as it worked out, we learned more from putting together thermostats and computers than we did from taking apart monkey brains and frog eyes." I love this quote by Danny Hillis. It highlights the importance of "learning through examples". During the first weeks of our class [COMP_SCI 396: Artificial Life](https://www.mccormick.northwestern.edu/computer-science/academics/courses/descriptions/396-2.html), we discussed a quote found on [Richard Feynman's](https://en.wikipedia.org/wiki/Richard_Feynman) blackboard at the time of his death: "What I cannot create, I do not understand." This has been the philosophy of my life from at least the last decade or so. Like many thinkers before me, I have been bewildered by some of the very basic questions of life and existence, but I couldn't find any reasoanble approach to seeking answers for those questions - until, I stumbled upon an incredible book written by Steven Levy on "Artificial Life". 

Christopher Langton defines artificial life as 'The study of natural life, where "nature" is understood to include, rather than to exclude, human beings and their artifacts.' There are two tracks of artificial life. The more ambitious goal is the creation of living systems - the equivalent of biological alchemy. The other quest, closer to hand, is the simulation — in some cases the duplication — of life’s unique processes, in order to heighten our understanding of natural life and of possible alternative forms of life. This is my first simulation project in artificial life. In the different branches of this repository, you'll find the bits and pieces that led me to this final project.

## Motivation

One biological theorem, postulated by R. A. Fisher, conjectured that evolution proceeded by steady improvements in fitness. This is an equivalent to the so-called hill climbing technique used by certain computer optimization procedures, such as learning in neural network simulations. Because each generation was supposedly slightly fitter than the previous one, a graph illustrating this progress would show line angling upward, as though the fitness of the species were engaged in scaling a peak. 

![Evolutionary Hill Climbing](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/hill_climbing.png?raw=true)


Biologists studying the problem had created a more complicated, multidimensional map of the way that a species might evolve. This “adaptive landscape,”’ first postulated by Sewall Wright, represented the space of all possible genetic combinations. It was filled with bumps, peaks, valleys, and spikes. The gene pool of an entire population resided at a single area on this landscape. The higher the ground, the fitter the population would be if it found its way there. When the terrain was fairly level, a population theoretically engaged in a “random walk,”’ with the effects of crossover and mutation moving its genetic composition to different places, until it found an ascending plane. From that point, the more fit individuals within the population would push fitness higher, and the rest of the population would follow. 

But, if hill climbing was indeed the method nature used to achieve higher fitness, the discovery of the highest ground could not always be assumed. Once the population scaled a medium-size peak, it tended to get stuck. This was due to the built-in reluctance of a population to decrease its fitness, which would be necessary in order to search the landscape for an even higher peak. The population would remain fat and happy on its hill but miss out on the mountains that lay somewhere else on the chart. The population was then “stuck on a local maximum” with no incentive to make the giant evolutionary leaps that push life toward more complexity.

“If evolution is a hill-climbing technique, why doesn’t it seem to have problems that we know hill-climbing techniques suffer from?” ‘‘Why is evolution so much more powerful than any other hill-climbing technique? Why is it able to evolve much more complicated things?”

One possible explanation can be given in terms of ‘‘evolutionary arms races" -  a situation where two populations of differing species were set against each other, in predator-prey or host-parasite relationships. If a host population Evolved strategic traits to foil the parasite, the parasite would in turn evolve a strategy to compensate and the cycle would continue causing continuous improvements (i.e., evolution!). William Hamilton, among others, had suggested that the presence of parasites might have been integral in accelerating the pace of evolution to a rate capable of yielding its present diversity and complexity.


![Coevolution](https://github.com/vTheWise/Artificial_Life/blob/finalProject/Diagrams/coevolution.jpg?raw=true)

**This chain of thoughts led me to question the role of environmental hardships in shaping the path of evolution. I wondered if the creatures who have to face harsh environmental conditions evolve better than those who do not.**




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
4. Here's an awesome book by Steven Levy: ["Artificial Life: A Report from the Frontier Where Computers Meet Biology"](https://www.goodreads.com/book/show/737831.Artificial_Life).
5. If you're still wondering what Artificial Life is, here's a perfect read for you: [A New Definition of Artificial Life](https://www.fisica.unam.mx/personales/mir/langton.pdf)

