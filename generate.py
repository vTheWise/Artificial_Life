import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")
length = 1
width = 1
height = 1
x1 = 0.5
y1= 0.5
z1 = 0.5
x2 = 0.5
y2 = 1.5
z2 = 1.5
#pyrosim.Send_Cube(name="Box2", pos=[x2, y2, z2] , size=[length,width,height])
#pyrosim.Send_Cube(name="Box", pos=[x1, y1, z1] , size=[length,width,height])
for i in range(10):
    pyrosim.Send_Cube(name="Box", pos=[x1, y1, z1], size=[length, width, height])
    z1 += 1.5
    length *= 0.9
    width *= 0.9
    height *= 0.9
    
pyrosim.End()