import pyrosim.pyrosim as pyrosim
import random

length = 1
width = 1
height = 1
x1 = 0
y1 = 0
z1 = 0.5

def Generate_World():
    pyrosim.Start_SDF("data/world.sdf")

    pyrosim.Send_Cube(name="Box", pos=[x1-2, y1+2, z1] , size=[length,width,height])

    pyrosim.End()

def Generate_Body():
    pyrosim.Start_URDF("data/body.urdf")

    pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[1, 0, 1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2, 0, 1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[length, width, height])

    pyrosim.End()

def Generate_Brain():
    pyrosim.Start_NeuralNetwork("data/brain.nndf")

    #Sensor Neurons
    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")


    #Motor Neurons
    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

    # #Synapses and Synaptic Weights
    # pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=3, weight=0.0)
    # pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=3, weight=0.0)
    #
    # pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=4, weight=-1.0)
    # pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=4, weight=-1.0)

    for s_neuron in range(3):
        for m_neuron in range(3, 5):
            pyrosim.Send_Synapse(sourceNeuronName=s_neuron, targetNeuronName=m_neuron, weight=random.uniform(-1, 1))

    pyrosim.End()

Generate_World()

Generate_Body()

Generate_Brain()
