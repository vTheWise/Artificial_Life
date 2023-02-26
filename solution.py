#region Imports
import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import random
import os
import time
#endregion Imports

#region File Attributes
random.seed(42)
np.random.seed(42)
#endregion File Attributes

class SOLUTION:

    def __init__(self, id):
        #region Class Variables
        self.myID = id
        if self.myID == 0:
            self.Create_World()

    def Start_Simulation(self, directOrGUI):
        links, joints = self.Create_Body()
        self.links, self.link_num = links, len(links)
        self.joints, self.joint_num = joints, len(joints)
        self.sensor_num, self.motor_num = sum([l['sensor_tag'] for l in links]), len(joints)
        self.weights = np.random.rand(self.sensor_num, self.motor_num)
        self.weights = 2 * self.weights - 1
        self.Create_Brain()
        os.system("python3 simulate.py {0} {1} 2&>runLogs.txt &".format(directOrGUI, str(self.myID)))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("data/fitness{0}.txt".format(str(self.myID))):
            time.sleep(0.01)
        f = open("data/fitness{0}.txt".format(str(self.myID)), "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm ./data/fitness{0}.txt".format(str(self.myID)))
        return self.fitness

    def Create_World(self):
        # empty world
        pyrosim.Start_SDF("data/world.sdf")
        pyrosim.End()

    def Transform_Link(self, name, size, pos):
        sensor_tag = random.sample([True, False], k=1)[0]
        color_name = 'green' if sensor_tag else 'blue'
        link_color = "0 1.0 0 1.0" if sensor_tag else "0 0 1.0 1.0"
        link_dict = {
            "name": name,
            "size": size,
            "pos": pos,
            'sensor_tag': sensor_tag, 'color': link_color, 'color_name': color_name,
        }
        return link_dict

    def get_size(self, leg_type, link_width_range, link_length_rage, leg_width_range, leg_length_range):

        body_size_x, upper_leg_size_x, lower_leg_size_x = -1, 0, 0
        while (body_size_x < upper_leg_size_x) or (body_size_x < lower_leg_size_x):
            body_size_x, body_size_y, body_size_z = random.uniform(*link_length_rage), random.uniform(
                *link_width_range), random.uniform(*link_width_range)
            if leg_type == "spider":
                upper_leg_size_x = random.uniform(*leg_width_range)
                upper_leg_size_y = random.uniform(*leg_length_range)
                upper_leg_size_z = random.uniform(*leg_width_range)
            elif leg_type == "qudrapedal":
                upper_leg_size_x = random.uniform(*leg_width_range)
                upper_leg_size_y = random.uniform(*leg_width_range)
                upper_leg_size_z = random.uniform(*leg_length_range)
            lower_leg_size_x = random.uniform(*leg_width_range)
            lower_leg_size_y = random.uniform(*leg_width_range)
            lower_leg_size_z = random.uniform(*leg_length_range)
        return (body_size_x, body_size_y, body_size_z), (upper_leg_size_x, upper_leg_size_y, upper_leg_size_z), (
        lower_leg_size_x, lower_leg_size_y, lower_leg_size_z)

    def Create_Body(self):
        # shape is good at climbing the steps
        links, joints = {}, {}

        # number of section, for each section, (body szie, leg type, leg size)
        num_sec = random.randint(2, 5)
        sec_width_range, sec_length_rage = (0.1, 0.5), (0.1, 0.5)
        sec_connection_type = random.sample(["snake", "horse", ], k=1)[0]
        leg_type = random.sample(["spider", "qudrapedal", ], k=1)[0]
        leg_width_range, leg_length_range = (0.1, 0.3), (0.2, 0.6)

        # size
        (body_size_x, body_size_y, body_size_z), \
        (upper_leg_size_x, upper_leg_size_y, upper_leg_size_z), \
        (lower_leg_size_x, lower_leg_size_y, lower_leg_size_z) \
            = self.get_size(leg_type, sec_width_range, sec_length_rage, leg_width_range, leg_length_range)

        for i in range(num_sec):
            if i == 0:
                body_pos_x, body_pos_y, body_pos_z = body_size_x / 2.0, 0, upper_leg_size_z + lower_leg_size_z
            else:
                body_pos_x, body_pos_y, body_pos_z = body_size_x / 2.0, 0, 0
            link_dict = self.Transform_Link(f"body{i}", [body_size_x, body_size_y, body_size_z],
                                       [body_pos_x, body_pos_y, body_pos_z])
            links[f"body{i}"] = link_dict
            # right leg
            right_upper_pos_x, right_upper_pos_y, right_upper_pos_z = 0, -upper_leg_size_y / 2.0, -upper_leg_size_z / 2.0
            left_upper_pos_x, left_upper_pos_y, left_upper_pos_z = 0, upper_leg_size_y / 2.0, -upper_leg_size_z / 2.0
            if leg_type == "spider":
                right_lower_pos_x, right_lower_pos_y, right_lower_pos_z = 0, -lower_leg_size_y / 2.0, -lower_leg_size_z / 2.0
                left_lower_pos_x, left_lower_pos_y, left_lower_pos_z = 0, lower_leg_size_y / 2.0, -lower_leg_size_z / 2.0
            elif leg_type == "qudrapedal":
                right_lower_pos_x, right_lower_pos_y, right_lower_pos_z = 0, 0, -lower_leg_size_z / 2.0
                left_lower_pos_x, left_lower_pos_y, left_lower_pos_z = 0, 0, -lower_leg_size_z / 2.0
            link_dict = self.Transform_Link(f"RightUpperLeg{i}", [upper_leg_size_x, upper_leg_size_y, upper_leg_size_z], \
                                       [right_upper_pos_x, right_upper_pos_y, right_upper_pos_z])
            links[f"RightUpperLeg{i}"] = link_dict
            link_dict = self.Transform_Link(f"LeftUpperLeg{i}", [upper_leg_size_x, upper_leg_size_y, upper_leg_size_z], \
                                       [left_upper_pos_x, left_upper_pos_y, left_upper_pos_z])
            links[f"LeftUpperLeg{i}"] = link_dict
            link_dict = self.Transform_Link(f"RightLowerLeg{i}", [lower_leg_size_x, lower_leg_size_y, lower_leg_size_z], \
                                       [right_lower_pos_x, right_lower_pos_y, right_lower_pos_z])
            links[f"RightLowerLeg{i}"] = link_dict
            link_dict = self.Transform_Link(f"LeftLowerLeg{i}", [lower_leg_size_x, lower_leg_size_y, lower_leg_size_z], \
                                       [left_lower_pos_x, left_lower_pos_y, left_lower_pos_z])
            links[f"LeftLowerLeg{i}"] = link_dict

        # generate sec joint
        for i in range(num_sec):
            # body joint
            if i < num_sec - 1:
                parent, child = f"body{i}", f"body{i + 1}"
                joint_name = f"{parent}_{child}"
                if i == 0:
                    pos_x, pos_y, pos_z = links[parent]["size"][0], 0, links[parent]["pos"][2]
                else:
                    pos_x, pos_y, pos_z = links[parent]["size"][0], 0, 0
                if sec_connection_type == "snake":
                    joint_axis = "0 0 1"
                elif sec_connection_type == "horse":
                    joint_axis = "0 1 0"
                joint_dict = {
                    'name': joint_name,
                    'parent': parent, 'child': child,
                    'position': [pos_x, pos_y, pos_z], 'jointAxis': joint_axis,
                }
                joints[joint_name] = joint_dict
            # right upper
            parent, child = f"body{i}", f"RightUpperLeg{i}"
            joint_name = f"{parent}_{child}"
            if i == 0:
                pos_x, pos_y, pos_z = links[parent]["size"][0] / 2.0, -links[parent]["size"][1] / 2.0, \
                                      links[parent]["pos"][2]
            else:
                pos_x, pos_y, pos_z = links[parent]["size"][0] / 2.0, -links[parent]["size"][1] / 2.0, 0
            if leg_type == "spider":
                joint_axis = "1 0 0 "
            elif leg_type == "qudrapedal":
                joint_axis = "0 1 0"
            joint_dict = {'name': joint_name, 'parent': parent, 'child': child, 'position': [pos_x, pos_y, pos_z],
                          'jointAxis': joint_axis, }
            joints[joint_name] = joint_dict
            # left upper
            parent, child = f"body{i}", f"LeftUpperLeg{i}"
            joint_name = f"{parent}_{child}"
            if i == 0:
                pos_x, pos_y, pos_z = links[parent]["size"][0] / 2.0, links[parent]["size"][1] / 2.0, \
                                      links[parent]["pos"][2]
            else:
                pos_x, pos_y, pos_z = links[parent]["size"][0] / 2.0, links[parent]["size"][1] / 2.0, 0
            if leg_type == "spider":
                joint_axis = "1 0 0 "
            elif leg_type == "qudrapedal":
                joint_axis = "0 1 0"
            joint_dict = {'name': joint_name, 'parent': parent, 'child': child, 'position': [pos_x, pos_y, pos_z],
                          'jointAxis': joint_axis, }
            joints[joint_name] = joint_dict
            # right_lower
            parent, child = f"RightUpperLeg{i}", f"RightLowerLeg{i}"
            joint_name = f"{parent}_{child}"
            if leg_type == "spider":
                joint_axis = "1 0 0 "
                pos_x, pos_y, pos_z = 0, -links[parent]["size"][1], -links[parent]["size"][2]
            elif leg_type == "qudrapedal":
                joint_axis = "0 1 0"
                pos_x, pos_y, pos_z = 0, -links[parent]["size"][1] / 2.0, -links[parent]["size"][2]
            joint_dict = {'name': joint_name, 'parent': parent, 'child': child, 'position': [pos_x, pos_y, pos_z],
                          'jointAxis': joint_axis, }
            joints[joint_name] = joint_dict
            # left lower
            parent, child = f"LeftUpperLeg{i}", f"LeftLowerLeg{i}"
            joint_name = f"{parent}_{child}"
            if leg_type == "spider":
                joint_axis = "1 0 0 "
                pos_x, pos_y, pos_z = 0, links[parent]["size"][1], -links[parent]["size"][2]
            elif leg_type == "qudrapedal":
                joint_axis = "0 1 0"
                pos_x, pos_y, pos_z = 0, links[parent]["size"][1] / 2.0, -links[parent]["size"][2]
            joint_dict = {'name': joint_name, 'parent': parent, 'child': child, 'position': [pos_x, pos_y, pos_z],
                          'jointAxis': joint_axis, }
            joints[joint_name] = joint_dict

        # generate urdf file
        pyrosim.Start_URDF("data/body{0}.urdf".format(self.myID))
        for link_dict in links.values():
            pyrosim.Send_Cube(name=link_dict['name'], pos=link_dict['pos'], size=link_dict['size'],
                              rgba=link_dict['color'], color=link_dict['color_name'])
        for joint_dict in joints.values():
            pyrosim.Send_Joint(name=joint_dict['name'], parent=joint_dict['parent'], child=joint_dict['child'], \
                               type="revolute", position=joint_dict['position'], jointAxis=joint_dict['jointAxis'])
        pyrosim.End()
        return list(links.values()), list(joints.values())

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("data/brain{0}.nndf".format(self.myID))

        # sensor neurons
        neuron_id = 0
        for i in range(self.link_num):
            if self.links[i]['sensor_tag']:
                pyrosim.Send_Sensor_Neuron(name=neuron_id, linkName=self.links[i]['name'])
                neuron_id += 1

        # motor neurons
        for i in range(self.motor_num):
            pyrosim.Send_Motor_Neuron(name=neuron_id, jointName=self.joints[i]['name'])
            neuron_id += 1

        for currentRow in range(self.sensor_num):
            for currentColumn in range(self.motor_num):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn + self.sensor_num,
                                     weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        # mutation_possibilities = ['Mutate_Body', 'Mutate_weight', 'Mutate_Weight_And_Body']
        # mutation_type = random.choice(mutation_possibilities)
        randomRow = random.randint(0, self.sensor_num - 1)
        randomColumn = random.randint(0, self.motor_num - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID







