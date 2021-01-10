"""
This module has INDIVIDUAL class that has methods which implements the initializing, evaluation and
fitness score computation  of an individual. It also has mutation and crossover functions.
"""

import random
import pyrosim
from robot import ROBOT
import math
import numpy as np
import constants as c

random.seed(c.randomSeed)
np.random.seed(c.randomSeed)

class INDIVIDUAL:
    """
    Individual robot simulation.
    """
    def __init__(self, i):
        """
        Initializes an individual with initial traits like ID, ball_psensor_id, robot_position, genome, hidden_genome,
        WHEEL_RADIUS, SPEED, MASS, fitness and adaptiveMutRate.
        i: ID of an individual in a population
        return: None
        """
        self.ID = i
        self.ball_psensor_id = 0
        self.robot_position = 0
        
        # intialize random weight array (len(sensor neurons) * len(mneurons))
        # genome: sensors to hidden layer
        self.hidden_genome = np.random.random(size=(12, c.numHiddenNeurons)) * 200  - 100
        
        # genome: hidden layer to output
        self.genome = np.random.random(size=(c.numHiddenNeurons, 4))*200-100

        self.WHEEL_RADIUS = 0.05
        self.SPEED = 5
        self.MASS = 25
        
        self.fitness = 0
        
        self.adaptiveMutRate = c.mutRate
    
    def Start_Evaluation(self, env, pb=True, pp=True):
        """
        Evaluates an individual over a simulation environment in pyrosim.
        env: Pyrosim simulation env (object of ENVIRONMENT class)
        play_blind   : bool, optional
            If True the simulation runs without graphics (headless) else if
            False the simulation runs with graphics (the default is False)
        play_paused : bool, optional
            If True the simulation starts paused else if False the simulation
            starts running. With simulation window in focus use Ctrl-p to
            toggle pausing the simulation. (the default is False)
        return:None
        """
        self.sim = pyrosim.Simulator(eval_time=c.evalTime, play_blind=pb, play_paused=pp, xyz=[0, 7.5, 0.8], hpr=[270,0,0.0])
        
        # add robot to sim
        self.robot = ROBOT(self.sim,genome = self.genome, hidden_genome = self.hidden_genome, WHEEL_RADIUS = self.WHEEL_RADIUS, SPEED=self.SPEED, MASS=self.MASS)
       
        # add environment to sim
        env.Send_To(sim = self.sim)
        
        # define collisions in sim
        self.sim.assign_collision('ball', 'robot')
        self.sim.assign_collision('goalpost', 'robot')
        self.sim.assign_collision('ball', 'goalpost')
    
        self.sim.start()
        # retrieve the id of the ball position sensor
        self.ball_psensor_id = env.ball_psensor_id
        self.robot_position = self.robot.position

    def Compute_Fitness(self, metric="goals_scored"):
        """
        Computes the sum of fitness of an individual over all the environments.
        metric: Approach used for fitness score calculation
        return: None
        """
        self.sim.wait_to_finish()

        # current fitness function is the sum of fitness outputs over each environment

        #returns the x,y and z position of the ball
        sphere_position_x = self.sim.get_sensor_data(sensor_id = self.ball_psensor_id, svi=0)
        sphere_position_y = self.sim.get_sensor_data(sensor_id = self.ball_psensor_id, svi=1)
        sphere_position_z = self.sim.get_sensor_data(sensor_id = self.ball_psensor_id, svi=2)

        # computes the fitness according to the specified fitness metric
        if metric == "goals_scored":
            self.fitness += self.Goals_Scored(sphere_position_x, sphere_position_y, sphere_position_z)
        elif metric == "distance_travelled":
            penalty = -1
            self.fitness += self.Distance_Travelled(sphere_position_x, sphere_position_y, sphere_position_z,penalty)

        elif metric == "best_keeper":
            #no penalty
            penalty = 1
            #returns 1 when a collision is detected and 0 otherwise
            t_data = self.sim.get_sensor_data(sensor_id = self.robot.tsensor_id ) 
            self.fitness += self.Best_Keeper(sphere_position_x, sphere_position_y, sphere_position_z, penalty, t_data)

        elif metric == "reward_efforts":
            self.fitness += self.reward_efforts(sphere_position_x, sphere_position_y, sphere_position_z)

        del self.sim

    def Goals_Scored(self,x,y,z):
        """
        Determines whether a goal is scored or not.
        x,y,z: x,y and z coordinate position of the ball
        return goal_scored: Goal scored or saved (Boolean)
        """
        ball_radius = 0.16
        goal_post_y = 0
        goal_width = 5
        goal_height = 2

        # mask for when the ball is within the goal_width
        x_cross_mask = (x > (-1*(goal_width/2) + ball_radius) ) & (x< (goal_width/2) - ball_radius)

        # mask for when the ball has crossed the goal post line
        y_cross_mask = y< (goal_post_y + (-1*ball_radius) )

        # mask for when the ball is within the goal_height
        z_cross_mask = (z >= ball_radius) & (z< (goal_height - ball_radius) )

        # mask for when the ball has crossed within goal post 
        valid_mask  = x_cross_mask * y_cross_mask * z_cross_mask

        # returns 1 if a goal was scored during that event or 0 otherwise
        goal_scored = 1 if np.sum(valid_mask) >0 else 0

        return goal_scored

    def Distance_Travelled(self,x,y,z,penalty):
        """
        Computes the final distance between the ball and the robot.
        x,y,z: x,y and z coordinate position of the ball
        penalty: penalizing number if goal was not scored
        return final_distance: Final distance between the ball and the robot
        """
        # check if goal was scored
        goal_scored = self.Goals_Scored(x,y,z)
        ball_position_3d = np.vstack((x,y,z))

        pythag_distance = np.sqrt(np.sum(ball_position_3d[:,-1]**2))
        if goal_scored == 1: 
            # if goal was scored, return the distance
            final_distance = pythag_distance
        else:
            # penalise if goal was not scored 
            final_distance = penalty * pythag_distance

        return final_distance

    def Best_Keeper(self,x,y,z,penalty,t_data):
        """
        Computes the fitness score taking into account the reward for saving the goal and final distance between ball
        and robot.
        x,y,z: x,y and z coordinate position of the ball
        penalty: penalizing number if goal was not scored
        t_data: Touch sensor data from the robot (array)
        return : fitness score
        """
        not_conceding_score = 1
        save_reward = 1000

        # check if the robot collided with the ball
        collision_detected = 1 if np.sum(t_data) > 0 else 0 
        # check if the ball crossed within the goal post 
        goals_saved = 0 if self.Goals_Scored(x,y,z) == 1 else 1
        # measure the distance travelled by the ball relative to the goal post line
        distance_travelled = self.Distance_Travelled(x,y,z,penalty)

        # check the distance of saved goal
        goal_saved_distance = collision_detected * goals_saved * distance_travelled
        
        if goal_saved_distance > 0 :
            # reward for saving the goal + distance travelled
            return save_reward + distance_travelled
        
        elif collision_detected == 1 :
            # reward for not saving the goal but touching the ball
            return 100
        
        elif goals_saved == 1:
            # reward for not conceding a goal even though by chance
            return not_conceding_score
        
        else:
            return 0

    def reward_efforts(self, sphere_position_x, sphere_position_y, sphere_position_z):
        """It takes into consideration the distance between robot and ball at the time step when ball is just crossing
        the goal post(in case of goal success). Smaller is this distance,more will be the reward and higher will be the
        fitness. When the goal is saved, fitness is simply the twice of goal width, which is the highest."""
        fitness = 0
        ball_radius = 0.16
        goal_post_y = 0
        goal_width = 5
        goal_height = 2

        # x, y and z position of the robot
        robot_position_x = self.sim.get_sensor_data(sensor_id=self.robot_position, svi=0)
        robot_position_y = self.sim.get_sensor_data(sensor_id=self.robot_position, svi=1)
        robot_position_z = self.sim.get_sensor_data(sensor_id=self.robot_position, svi=2)

        # mask for when the ball has crossed the goal post line
        y_cross_mask = sphere_position_y < (goal_post_y + (-1 * ball_radius))

        # mask for when the ball is within the goal_height
        # z_cross_mask = (z >= ball_radius) & (z< (goal_height - ball_radius) ) # excluding the flying shot for now

        # mask for when the ball has crossed within goal post
        valid_mask = y_cross_mask

        # returns 1 if a goal was saved during that event or 0 otherwise
        goal_saved = False if np.sum(valid_mask) > 0 else True
        if goal_saved:
            fitness = 2 * goal_width
        else:  # calculate the distance between car and ball at the time step when ball is just crossing the goal post
            timestep_idx = len(y_cross_mask) - np.sum(y_cross_mask)
            distance_x = (robot_position_x[timestep_idx] - sphere_position_x[timestep_idx])**2
            distance_y = (robot_position_y[timestep_idx] - sphere_position_y[timestep_idx]) ** 2
            distance_z = (robot_position_z[timestep_idx] - sphere_position_z[timestep_idx]) ** 2
            # subtract this distance from the goal width to reward
            fitness = goal_width - np.sqrt(distance_x + distance_y + distance_z)

        return fitness
        
    def Mutate(self):
        """
        Implements mutation genetic operator. It mutates the individual's traits like WHEEL_RADIUS, SPEED, MASS,
        genome, hidden layer genome etc. WHEEL_RADIUS, SPEED and MASS are changed to random values within specified range.
        Main genome and hidden layer genome are changed changed according to the chance determined from mutation rate.
        This method incorporates the adaptive mutation of genomes.
        return : None
        """

        # WHEEL_RADIUS, SPEED and MASS are changed to random values within specified range.
        self.WHEEL_RADIUS = np.random.randint(5,15,size=1)[0]/100
        self.SPEED = np.random.randint(5,30,size=1)[0]
        self.MASS = np.random.randint(80,120,size=1)[0]
        
        # genome mutation according to chance from mutation rate.
        if not c.vectorized_mutation:
            for row_idx, row in enumerate(self.genome):
                for col_idx, col in enumerate(row):
                    chance = random.random()*100
                    if chance < self.adaptiveMutRate:
                        self.genome[row_idx, col_idx] = random.uniform(-100, 100)
                    else:
                        pass
        # introducing the numpy vectorization for faster computation when muteRate is higher
        else:
            genome_copy = self.genome.copy()
            self.genome = self.genome.reshape(genome_copy.size)
            m = int(self.adaptiveMutRate*c.popSize/100)
            # sampling the m indices from the solution without replacement
            idx = random.sample(range(len(self.genome)), k=m)
            self.genome[idx] = [random.uniform(-100, 100) for i in idx]
            # self.genome[idx] = [random.gauss(self.genome[i], math.fabs(self.genome[i])) for i in idx]
            self.genome = self.genome.reshape(*genome_copy.shape)

        # hidden genome mutation
        for row_idx, row in enumerate(self.hidden_genome):
            for col_idx, col in enumerate(row):
                chance = random.random()*100
                if chance < self.adaptiveMutRate:
                    self.hidden_genome[row_idx, col_idx] = np.random.random() * 200 - 100

        #print(self.genome)
        
        # adaptive mutation
        
        if c.adaptive_mutation_enabled:
            rechenberg_constant = 1.3
            xi = np.random.uniform(1/rechenberg_constant, rechenberg_constant)
            self.adaptiveMutRate = np.min([100, self.adaptiveMutRate * xi])
        
    def Crossover(self, other):
        """
        Perform crossover operation of genetic algorithm between 2 individuals from parent generation. It selects a
        crossover point randomly and swap the main genomes and hidden genomes of the two individuals.
        other: Other individual
        return: None
        """
        flat_parent1_genome = self.genome.flatten()
        flat_parent2_genome = other.genome.flatten()
        
        # random crossover point
        crossover_idx = np.random.randint(len(flat_parent1_genome))
        crossover_idx2 = np.random.randint(crossover_idx, len(flat_parent1_genome))
        
        # swap genes
        flat_parent1_genome[crossover_idx:crossover_idx2] = flat_parent2_genome[crossover_idx:crossover_idx2]
        
        # NB. produces only one child
        self.genome = flat_parent1_genome.reshape(self.genome.shape)
        
        # do the same for other genome
        flat_parent1_hidden_genome = self.hidden_genome.flatten()
        flat_parent2_hidden_genome = other.hidden_genome.flatten()
        flat_parent1_hidden_genome[crossover_idx:crossover_idx2] = flat_parent2_hidden_genome[crossover_idx:crossover_idx2]
        self.hidden_genome = flat_parent1_hidden_genome.reshape(self.hidden_genome.shape)

    def Print(self):
        """ Print the individual ID and fitness score"""
        print('[', self.ID, ':', self.fitness, end=']')
