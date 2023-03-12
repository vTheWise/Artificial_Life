from pyrosim.commonFunctions import Save_Whitespace

class MASS_URDF: 

    def __init__(self,mass):

        self.string = '<mass value="' + str(mass) + '" />'

        self.depth = 3

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write(self.string + '\n' )
