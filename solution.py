#region Imports
import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import re
#endregion Imports

#region File Attributes
# set random seeds
random.seed(c.random_seed)
np.random.seed(c.numpy_seed)

# constants
SPIDER_LEG_TYPE = 'spider'
QUADRUPED_LEG_TYPE = 'quadruped'
CREATURE_REPTILE = 'reptile'
CREATURE_MAMMAL = 'mammal'
#endregion File Attributes

class SOLUTION:

    def __init__(self, id):
        self.myID = id
        self.parentID = -1
        if self.myID == 0:
            self.Create_World()

    def Start_Simulation(self, directOrGUI, isMutation=False):
        self.num_limbs = random.randint(2, 8)
        if isMutation:
            self.Create_Child_Body()
        else:
            links, joints = self.Create_Body()
            self.links, self.num_links = links, len(links)
            self.joints, self.num_joints = joints, len(joints)
            self.num_sensors, self.num_motors = sum([l['s_flag'] for l in links]), len(joints)
            self.weights = (2 * np.random.rand(self.num_sensors, self.num_motors)) - 1

        self.Create_Brain()

        os.system("python3 simulate.py {0} {1} 2&>runLogs.txt &".format(directOrGUI, str(self.myID)))

    def Create_Child_Body(self):
        # generate body's urdf file: suffix: myID
        pyrosim.Start_URDF("data/body{0}.urdf".format(self.myID))
        for link_dict in self.links:
            pyrosim.Send_Cube(name=link_dict['name'], pos=link_dict['pos'], size=link_dict['size'],
                              rgba=link_dict['color'], color=link_dict['color_name'],
                              mass=np.prod(link_dict['size']) / 2)
        for joint_dict in self.joints:
            pyrosim.Send_Joint(name=joint_dict['name'], parent=joint_dict['parent'], child=joint_dict['child'], \
                               type="revolute", position=joint_dict['position'], jointAxis=joint_dict['jointAxis'])
        pyrosim.End()

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("data/fitness{0}.txt".format(str(self.myID))):
            time.sleep(0.01)
        f = open("data/fitness{0}.txt".format(str(self.myID)), "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm ./data/fitness{0}.txt".format(str(self.myID)))
        return self.fitness

    def Create_World(self):
        pyrosim.Start_SDF("data/world.sdf")
        pyrosim.Send_Sphere(name="Ball", pos=c.ball_pos, size=[0.75])
        pyrosim.End()

    def Set_Body_Characteristics(self, name, size, pos):
        s_flag = random.choice([True, False])
        color_name = c.color_sensor_link if s_flag else c.color_nosensor_link
        link_color = c.rgba_sensor_link if s_flag else c.rgba_nosensor_link
        link_dict = {
            "name": name,
            "size": size,
            "pos": pos,
            's_flag': s_flag, 'color': link_color, 'color_name': color_name,
        }
        return link_dict

    def Get_Limb_Size(self, leg_type, body_width_range, body_length_rage, leg_width_range, leg_length_range):
        bodyX, upperLegX, lowerLegX = -1, 0, 0
        while (bodyX < upperLegX) or (bodyX < lowerLegX):
            bodyX, bodyY, bodyZ = random.uniform(*body_length_rage), random.uniform(
                *body_width_range), random.uniform(*body_width_range)
            if leg_type == QUADRUPED_LEG_TYPE:
                upperLegX = random.uniform(*leg_width_range)
                upperLegY = random.uniform(*leg_width_range)
                upperLegZ = random.uniform(*leg_length_range)
            elif leg_type == SPIDER_LEG_TYPE:
                upperLegX = random.uniform(*leg_width_range)
                upperLegY = random.uniform(*leg_length_range)
                upperLegZ = random.uniform(*leg_width_range)
            lowerLegX = random.uniform(*leg_width_range)
            lowerLegY = random.uniform(*leg_width_range)
            lowerLegZ = random.uniform(*leg_length_range)
        return (bodyX, bodyY, bodyZ), (upperLegX, upperLegY, upperLegZ), (lowerLegX, lowerLegY, lowerLegZ)

    def Create_Body(self):
        links, joints = {}, {}
        limb_width_range, link_length_rage = (0.1, 0.5), (0.1, 0.5)
        creature_inspired_by = random.choice([CREATURE_REPTILE, CREATURE_MAMMAL])
        leg_type = random.choice([SPIDER_LEG_TYPE, QUADRUPED_LEG_TYPE])
        leg_width_range, leg_length_range = (0.1, 0.3), (0.2, 0.6)

        (bodyX, bodyY, bodyZ), (upperLegX, upperLegY, upperLegZ), (lowerLegX, lowerLegY, lowerLegZ) \
            = self.Get_Limb_Size(leg_type, limb_width_range, link_length_rage, leg_width_range, leg_length_range)

        for i in range(self.num_limbs):
            if i == 0: # root limb with absolute position
                body_pos_x, body_pos_y, body_pos_z = bodyX / 2.0, 0, upperLegZ + lowerLegZ
            else: # subsequent limbs with relative positions
                body_pos_x, body_pos_y, body_pos_z = bodyX / 2.0, 0, 0

            link_dict = self.Set_Body_Characteristics(f"link{i}", [bodyX, bodyY, bodyZ],
                                                      [body_pos_x, body_pos_y, body_pos_z])
            links[f"link{i}"] = link_dict

            # legs
            rightUpper_posX, rightUpper_posY, rightUpper_posZ = 0, -upperLegY / 2.0, -upperLegZ / 2.0
            leftUpper_posX, leftUpper_posY, leftUpper_posZ = 0, upperLegY / 2.0, -upperLegZ / 2.0

            if leg_type == SPIDER_LEG_TYPE:
                rightLower_posX, rightLower_posY, rightLower_posZ = 0, -lowerLegY / 2.0, -lowerLegZ / 2.0
                leftLower_posX, leftLower_posY, leftLower_posZ = 0, lowerLegY / 2.0, -lowerLegZ / 2.0

            elif leg_type == QUADRUPED_LEG_TYPE:
                rightLower_posX, rightLower_posY, rightLower_posZ = 0, 0, -lowerLegZ / 2.0
                leftLower_posX, leftLower_posY, leftLower_posZ = 0, 0, -lowerLegZ / 2.0

            link_dict = self.Set_Body_Characteristics(f"RightUpperLeg{i}", [upperLegX, upperLegY, upperLegZ], \
                                                      [rightUpper_posX, rightUpper_posY, rightUpper_posZ])
            links[f"RightUpperLeg{i}"] = link_dict

            link_dict = self.Set_Body_Characteristics(f"LeftUpperLeg{i}", [upperLegX, upperLegY, upperLegZ], \
                                                      [leftUpper_posX, leftUpper_posY, leftUpper_posZ])
            links[f"LeftUpperLeg{i}"] = link_dict

            link_dict = self.Set_Body_Characteristics(f"RightLowerLeg{i}", [lowerLegX, lowerLegY, lowerLegZ], \
                                                      [rightLower_posX, rightLower_posY, rightLower_posZ])
            links[f"RightLowerLeg{i}"] = link_dict

            link_dict = self.Set_Body_Characteristics(f"LeftLowerLeg{i}", [lowerLegX, lowerLegY, lowerLegZ], \
                                                      [leftLower_posX, leftLower_posY, leftLower_posZ])
            links[f"LeftLowerLeg{i}"] = link_dict

        # link joints
        for i in range(self.num_limbs):
            if i < self.num_limbs - 1:
                parent, child = f"link{i}", f"link{i + 1}"
                joint_name = f"{parent}_{child}"
                if i == 0: # absolute position
                    pos_x, pos_y, pos_z = links[parent]["size"][0], 0, links[parent]["pos"][2]
                else: # relative position
                    pos_x, pos_y, pos_z = links[parent]["size"][0], 0, 0
                if creature_inspired_by == CREATURE_REPTILE:
                    # can move in x-y plane
                    joint_axis = "0 0 1"
                elif creature_inspired_by == CREATURE_MAMMAL:
                    # can move in x-z plane
                    joint_axis = "0 1 0"
                joint_dict = {
                    'name': joint_name,
                    'parent': parent, 'child': child,
                    'position': [pos_x, pos_y, pos_z], 'jointAxis': joint_axis,
                }
                joints[joint_name] = joint_dict

            # right upper leg joints
            parent, child = f"link{i}", f"RightUpperLeg{i}"
            joint_name = f"{parent}_{child}"
            if i == 0:
                pos_x, pos_y, pos_z = links[parent]["size"][0] / 2.0, -links[parent]["size"][1] / 2.0, \
                                      links[parent]["pos"][2]
            else:
                pos_x, pos_y, pos_z = links[parent]["size"][0] / 2.0, -links[parent]["size"][1] / 2.0, 0

            if leg_type == SPIDER_LEG_TYPE:
                joint_axis = "1 0 0 "
            elif leg_type == QUADRUPED_LEG_TYPE:
                joint_axis = "0 1 0"
            joint_dict = {'name': joint_name, 'parent': parent, 'child': child, 'position': [pos_x, pos_y, pos_z],
                          'jointAxis': joint_axis, }
            joints[joint_name] = joint_dict

            # left upper leg joints
            parent, child = f"link{i}", f"LeftUpperLeg{i}"
            joint_name = f"{parent}_{child}"
            if i == 0:
                pos_x, pos_y, pos_z = links[parent]["size"][0] / 2.0, links[parent]["size"][1] / 2.0, \
                                      links[parent]["pos"][2]
            else:
                pos_x, pos_y, pos_z = links[parent]["size"][0] / 2.0, links[parent]["size"][1] / 2.0, 0
            if leg_type == SPIDER_LEG_TYPE:
                joint_axis = "1 0 0 "
            elif leg_type == QUADRUPED_LEG_TYPE:
                joint_axis = "0 1 0"
            joint_dict = {'name': joint_name, 'parent': parent, 'child': child, 'position': [pos_x, pos_y, pos_z],
                          'jointAxis': joint_axis, }
            joints[joint_name] = joint_dict

            # right lower leg joints
            parent, child = f"RightUpperLeg{i}", f"RightLowerLeg{i}"
            joint_name = f"{parent}_{child}"
            if leg_type == SPIDER_LEG_TYPE:
                joint_axis = "1 0 0 "
                pos_x, pos_y, pos_z = 0, -links[parent]["size"][1], -links[parent]["size"][2]
            elif leg_type == QUADRUPED_LEG_TYPE:
                joint_axis = "0 1 0"
                pos_x, pos_y, pos_z = 0, -links[parent]["size"][1] / 2.0, -links[parent]["size"][2]
            joint_dict = {'name': joint_name, 'parent': parent, 'child': child, 'position': [pos_x, pos_y, pos_z],
                          'jointAxis': joint_axis, }
            joints[joint_name] = joint_dict

            # left lower leg joints
            parent, child = f"LeftUpperLeg{i}", f"LeftLowerLeg{i}"
            joint_name = f"{parent}_{child}"
            if leg_type == SPIDER_LEG_TYPE:
                joint_axis = "1 0 0 "
                pos_x, pos_y, pos_z = 0, links[parent]["size"][1], -links[parent]["size"][2]
            elif leg_type == QUADRUPED_LEG_TYPE:
                joint_axis = "0 1 0"
                pos_x, pos_y, pos_z = 0, links[parent]["size"][1] / 2.0, -links[parent]["size"][2]
            joint_dict = {'name': joint_name, 'parent': parent, 'child': child, 'position': [pos_x, pos_y, pos_z],
                          'jointAxis': joint_axis, }
            joints[joint_name] = joint_dict

        # generate body's urdf file: suffix: myID
        pyrosim.Start_URDF("data/body{0}.urdf".format(self.myID))
        for link_dict in links.values():
            pyrosim.Send_Cube(name=link_dict['name'], pos=link_dict['pos'], size=link_dict['size'],
                              rgba=link_dict['color'], color=link_dict['color_name'], mass=np.prod(link_dict['size'])/2)
        for joint_dict in joints.values():
            pyrosim.Send_Joint(name=joint_dict['name'], parent=joint_dict['parent'], child=joint_dict['child'], \
                               type="revolute", position=joint_dict['position'], jointAxis=joint_dict['jointAxis'])
        pyrosim.End()
        return list(links.values()), list(joints.values())

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("data/brain{0}.nndf".format(self.myID))

        # sensor neurons
        neuron_id = 0
        for i in range(self.num_links):
            if self.links[i]['s_flag']:
                pyrosim.Send_Sensor_Neuron(name=neuron_id, linkName=self.links[i]['name'])
                neuron_id += 1

        # motor neurons
        for i in range(self.num_motors):
            pyrosim.Send_Motor_Neuron(name=neuron_id, jointName=self.joints[i]['name'])
            neuron_id += 1


        # synaptic weights
        for currentRow in range(self.num_sensors):
            for currentColumn in range(self.num_motors):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + self.num_sensors,
                                     weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        mutation_possibilities = ['Mutate_Weight', 'Mutate_Brain', 'Mutate_Weight_And_Brain', 'Mutate_Body',
                                  'Mutate_Body_And_Brain']
        mutation_type = random.choice(mutation_possibilities)
        if mutation_type == 'Mutate_Weight':
            self.Mutate_Weight()
        elif mutation_type == 'Mutate_Brain':
            self.Mutate_Brain()
        elif mutation_type == 'Mutate_Weight_And_Brain':
            self.Mutate_Weight_And_Brain()
        elif mutation_type == 'Mutate_Body':
            self.Mutate_Body()
        elif mutation_type == 'Mutate_Body_And_Brain':
            self.Mutate_Body_And_Brain()

    def Mutate_Body_And_Brain(self):
        self.Mutate_Body()
        self.Mutate_Brain()

    def Mutate_Body(self):
        if self.num_links > c.minimumLinks:
            limb_number = 0
            print('Mutate_Body Enter, Num Sensors::', self.num_sensors)
            print('Mutate_Body Enter, Num Links::', self.num_links)
            print('Mutate_Body Enter, Num Joints::', self.num_joints)
            for l in self.links[::-1]:
                if 'UpperLeg' in l['name']:
                    limb_number = re.findall(r'\d+', l['name'])[0]
                    self.links.remove(l)
                    self.num_links -= 1
                    self.num_sensors = self.num_sensors - 1 if l['s_flag'] else self.num_sensors
                    # delete joints
                    for j in self.joints[::-1]:
                        if j['parent'] == l['name'] or j['child'] == l['name']:
                            self.joints.remove(j)
                            self.num_motors -= 1
                            self.num_joints -= 1
                    break
            for l in self.links[::-1]:
                if 'LowerLeg{0}'.format(limb_number) in l['name']:
                    self.links.remove(l)
                    self.num_links -= 1
                    self.num_sensors = self.num_sensors - 1 if l['s_flag'] else self.num_sensors
                    break
        print('Mutate_Body Exit, Num Sensors::', self.num_sensors)
        print('Mutate_Body Exit, Num Links::', self.num_links)
        print('Mutate_Body Exit, Num Joints::', self.num_joints)
    def Mutate_Weight_And_Brain(self):
        self.Mutate_Weight()
        self.Mutate_Brain()

    def Mutate_Brain(self):
        print('Mutate_Brain Enter, Num Sensors::', self.num_sensors)
        print('Mutate_Brain Enter, Num Links::', self.num_links)
        s_flag = []
        while sum(s_flag) != self.num_sensors:
            s_flag = random.choices([True, False], k=self.num_links)
        print('Mutate_Brain, s_flag::', len(s_flag))
        for i in range(self.num_links):
            self.links[i]['s_flag'] = s_flag[i]
            self.links[i]['color_name'] = c.color_sensor_link if s_flag else c.color_nosensor_link
            self.links[i]['color'] = c.rgba_sensor_link if s_flag else c.rgba_nosensor_link
        self.num_sensors = sum([l['s_flag'] for l in self.links])
        print('Mutate_Brain Exit, Num Sensors::', self.num_sensors)
        print('Mutate_Brain Exit, Num Links::', self.num_links)

    def Mutate_Weight(self):
        randomRow = random.randint(0, self.num_sensors - 1)
        randomColumn = random.randint(0, self.num_motors - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID







