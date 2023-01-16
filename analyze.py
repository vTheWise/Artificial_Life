import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load('data/backLegSensorValues.npy', mmap_mode='r')
print('backLegSensorValues::::', backLegSensorValues)
frontLegSensorValues = np.load('data/frontLegSensorValues.npy', mmap_mode='r')
print('frontLegSensorValues::::', frontLegSensorValues)
plt.plot(backLegSensorValues, label='Back Leg Sensor Values', linewidth=6)
plt.plot(frontLegSensorValues, label='Front Leg Sensor Values')
plt.legend(loc='upper right', bbox_to_anchor=(1, 1.13), borderaxespad=0)
plt.show()