#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 12:19:05 2021

@author: leon
"""

import numpy as np
import pickle
import constants as c
import sys

class TESTS:
    
    def __init__(self):
        
        self.envs = {}
        
        # dict of 100 tests
        for e in range(0, numTests):
            self.envs[e] = TEST(e)
            


class TEST:
    
    def __init__(self, env_id):
        self.ID = env_id

        # ball params
        self.ball_radius = 0.16
        self.ball_z = self.ball_radius
        self.ball_psensor_id = 0
        
    def Send_To(self, sim):
        
        # goalpost params
        goal_width = 5
        goal_height = 2
        supportLength = 0.5
        postRad = 0.05
        avoid_sensor_offset = 0.5
        
        # goalpost object
        left_post = sim.send_cylinder(x=goal_width/2, y=0, z=goal_height/2+postRad+avoid_sensor_offset, length=goal_height, radius=postRad, collision_group = 'goalpost', mass=999)
        right_post = sim.send_cylinder(x=-goal_width/2, y=0, z=goal_height/2+postRad+avoid_sensor_offset, length=goal_height, radius=postRad, collision_group = 'goalpost', mass=999)
        crossbar = sim.send_cylinder(x=0, y=0, z=goal_height+postRad+avoid_sensor_offset, r1=1, r2=0, r3=0, length=goal_width, radius=postRad, collision_group = 'goalpost', mass=999)
        leftSupport = sim.send_cylinder(x=goal_width/2, y=--100, z=postRad, r1=0, r2=1, r3=0, length=supportLength, radius=postRad, collision_group='goalpost', mass=999)
        rightSupport = sim.send_cylinder(x=-goal_width/2, y=-100, z=postRad, r1=0, r2=1, r3=0, length=supportLength, radius=postRad, collision_group='goalpost', mass=999)
        
        
        sim.send_fixed_joint(left_post, crossbar)
        sim.send_fixed_joint(right_post, crossbar)
        sim.send_fixed_joint(leftSupport, left_post)
        sim.send_fixed_joint(rightSupport, right_post)
        
        
        # left < as might want to add aireal or more challenging shots after a number of gens. Could be good to stop over fitting?
        # E.g if a car saves 6/10 shots give it the ability to try 3 more complex shots. otherwise return 0 and dont start sim for extra shots. 
        if self.ID < 1000:
            y_speed = np.random.randint(-25,-10)
            x_speed = np.random.randint(-33,33)*y_speed/100
            ball = sim.send_sphere(x=0, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=x_speed, y=y_speed, z=0, time=5)
           
                
        # retrieve the position sensor id for the ball
        self.ball_psensor_id = sim.send_position_sensor(body_id = ball)
        
            #sim.send_external_force(ball, x=-6, y=np.random.randint(-100,-10), z=0, time=5)
        
# filename as first argument        
filename = sys.argv[1]

if sys.argv[2]:
    numTrials = sys.argv[2]
else:
    numTrials = 10
    
if sys.argv[3]:
    numTests = sys.argv[3]
else:
    numTests = 100

with open(filename, 'rb') as f:
    # load pickle
    best = pickle.load(f)

    for trial in range(numTrials):
        c.randomSeed = trial
        envs = TESTS()
        total_score = 0
        counter = 0
        for i in range(numTests):
            best.fitness = 0 
            best.Start_Evaluation(env=envs.envs[i], pb=True)
            #best.sim.wait_to_finish()
            best.Compute_Fitness(metric='best_keeper')
            print(best.fitness)
            total_score += best.fitness
            counter += 1
        #print('Fitness of the best in this generation: ', best.fitness)
        print(total_score/counter)