import random
import pyrosim
from robot import ROBOT
import math
import numpy as np
import constants as c

class INDIVIDUAL:
    """
    Individual robot simulation.
    """
    def __init__(self, i):
        
        self.ID = i
        self.genome = np.random.random()*0.1
        self.fitness = 0
    
    def Start_Evaluation(self, env, pb=True, pp=True):
        
        
        self.sim = pyrosim.Simulator(eval_time=c.evalTime, play_blind=pb, play_paused=pp)
        
        # add robot to sim
        self.robot = ROBOT(self.sim, self.genome)
        
        # add environment to sim
        env.Send_To(sim = self.sim)
        
        # define collisions in sim
        self.sim.assign_collision('ball', 'robot')
    
        self.sim.start()
        
    def Compute_Fitness(self):
        self.sim.wait_to_finish()
        
        # current fitness function is the sum of movement distance over each environment
        self.fitness += self.sim.get_sensor_data(sensor_id = self.robot.position, svi=1)[-1]
        del self.sim
        
    def Mutate(self):
        
        # mutation function
        self.genome = min(math.fabs(random.gauss(self.genome, math.fabs(self.genome))), 0.1)
        
    def Print(self):
        print('[', self.ID, ':', self.fitness, end=']')
        