import random
import pyrosim
from robot import ROBOT
import math
import numpy as np

class INDIVIDUAL:
    """
    Individual robot simulation.
    """
    def __init__(self, i):
        
        self.ID = i
        self.genome = np.random.random()
        self.fitness = 0
    
    def Start_Evaluation(self, pb=True):
        
        self.sim = pyrosim.Simulator(eval_time=1000, play_blind=pb)
        self.robot = ROBOT(self.sim, self.genome)
        self.sim.start()
        
    def Compute_Fitness(self):
        self.sim.wait_to_finish()
        
        # fitness function goes here - currently distance given by position sensor
        self.fitness = self.sim.get_sensor_data(sensor_id = self.robot.position, svi=1)[-1]
        del self.sim
        
    def Mutate(self):
        
        # mutation function
        self.genome = math.fabs(random.gauss(self.genome, math.fabs(self.genome)))
        
    def Print(self):
        print('[', self.ID, ':', self.fitness, end=']')
        