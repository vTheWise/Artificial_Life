class JOINT:
    def __init__(self, jointName, jointPos, jointAxis):
        self.jointName = jointName
        self.parentLink = jointName.split('_')[0]
        self.childLink = jointName.split('_')[1]
        self.jointPos = jointPos
        self.jointGlobalPos = [0, 0, 0]
        self.type = "revolute"
        self.jointAxis = jointAxis
