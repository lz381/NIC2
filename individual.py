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
        self.ball_psensor_id = 0
        
        # intialize random weight array (len(sensor neurons) * len(mneurons))
        self.genome = np.random.random(size=(12, 4))
        
        self.fitness = 0
    
    def Start_Evaluation(self, env, pb=True, pp=True):
        
        
        self.sim = pyrosim.Simulator(eval_time=c.evalTime, play_blind=pb, play_paused=pp, xyz=[0, 7.5, 0.8], hpr=[270,0,0.0])
        
        # add robot to sim
        self.robot = ROBOT(self.sim, genome = self.genome)
        
        # add environment to sim
        env.Send_To(sim = self.sim)
        
        # define collisions in sim
        self.sim.assign_collision('ball', 'robot')
        self.sim.assign_collision('goalpost', 'robot')
        self.sim.assign_collision('ball', 'goalpost')
    
        self.sim.start()
        # retrieve the id of the ball position sensor
        self.ball_psensor_id = env.ball_psensor_id

    def Compute_Fitness(self,metric = "goals_scored"):
        self.sim.wait_to_finish()
        
        # current fitness function is the sum of fitness outputs over each environment

        #returns the x,y and z position of the ball
        sphere_position_x = self.sim.get_sensor_data(sensor_id = self.ball_psensor_id, svi=0)
        sphere_position_y = self.sim.get_sensor_data(sensor_id = self.ball_psensor_id, svi=1)
        sphere_position_z = self.sim.get_sensor_data(sensor_id = self.ball_psensor_id, svi=2)

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

        del self.sim

    def Goals_Scored(self,x,y,z):

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
            # reward for saving the goal 
            return save_reward

        elif goals_saved == 1:
            # reward for not conceding a goal even though by chance
            return not_conceding_score

        else:
            # punish for conceding a goal
            return 0 *np.abs(distance_travelled)
        
    def Mutate(self):
        
        # mutation function
        # edit the genome to 
        
        for row_idx, row in enumerate(self.genome):
            for col_idx, col in enumerate(row):
                self.genome[row_idx, col_idx] = random.gauss(0,100)
                #self.genome[row_idx, col_idx] = random.gauss(self.genome[row_idx, col_idx], math.fabs(self.genome[row_idx, col_idx]) )
        print(self.genome)
        
    def Print(self):
        print('[', self.ID, ':', self.fitness, end=']')
