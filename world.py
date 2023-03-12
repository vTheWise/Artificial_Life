import pybullet as p
import pybullet_data
from hide_warnings import hide_warnings

class WORLD:
    @hide_warnings
    def __init__(self, physicsClient):
        self.physicsClient = physicsClient
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.planeId = p.loadURDF("plane.urdf", flags=p.URDF_USE_SELF_COLLISION)
        self.ballId = p.loadSDF("data/world.sdf")