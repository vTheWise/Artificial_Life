# region Imports
import constants as c
import numpy as np
# endregion Imports

class LINK:
    def __init__(self, linkName, parent, dim, relPos):
        self.linkName = linkName
        self.globalPos = [0, 0, 0]
        self.relPos = relPos
        self.dim = dim
        self.color = c.color_nosensor_link
        self.rgba = c.rgba_nosensor_link
        self.mass = np.prod(dim)
        self.parent = parent
        self.face = []

    def setDim(self, l, w, h):
        self.dim = [l, w, h]

    def setGlobalPos(self, x, y, z):
        self.globalPos = [x, y, z]

    def setColor(self, color, rgba):
        self.color = color
        self.rgba = rgba
