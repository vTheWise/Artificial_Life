import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")
length = 1
width = 1
height = 1
x1 = 0.5
y1= 0.5
z1 = 0.5

x2 = 1
y2 = y1
z2 = 1.5
#pyrosim.Send_Cube(name="Box", pos=[x1, y1, z1] , size=[length,width,height])
#pyrosim.Send_Cube(name="Box2", pos=[x2, y2, z2] , size=[length,width,height])

for k in range(5):
    li = length
    wi = width
    hi = height
    for j in range(5):
        li = length
        wi = width
        hi = height
        for i in range(10):
            pyrosim.Send_Cube(name="Box", pos=[x1, y1, z1], size=[li, wi, hi])
            z1 += hi
            li *= 0.9
            wi *= 0.9
            hi *= 0.9
        x1 += 1
        z1 = 0.5
    y1 += 1
    x1 = 0.5
    z1 = 0.5

pyrosim.End()