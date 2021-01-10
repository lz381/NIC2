"""
Use this module to playback the simulation of evaluation of a particular robot individual. It takes a .p file as input
and playback the simulation in all the environments. .p files has the instances of robot individuals recorded using
pickle library of python.
"""

from environments import ENVIRONMENTS
import constants as c
import pickle

envs = ENVIRONMENTS()
file_to_be_played = 'RobotReplayGen_0.p'  # change the name of file as required

with open(file_to_be_played, 'rb') as f:
    best = pickle.load(f)
    for i in range(c.numEnvs):
        best.Start_Evaluation(env=envs.envs[i], pb=False)
        best.sim.wait_to_finish()
    print('Fitness of the best in this generation: ', best.fitness)
