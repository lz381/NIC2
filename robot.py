import sys
sys.path.insert(0, '../..')
import pyrosim # noqa
import numpy as np
import random
import math
import constants as c

random.seed(42)
np.random.seed(42)


# create a random func that will return either True or False (Bool logic)
def random_bool():               
    return np.random.randint(2,size=1)[0]

# create a random func that will select the number of wheels (pairs)  
def random_Wheel():               
    return np.random.randint(9,size=1)[0]

# create a random number between -1 and 1 using the random module with uniform dist
def random2():               
    return random.uniform(-1,1)

class ROBOT:
    """
    Robot blueprints.
    """
    def __init__(self, sim, genome,WHEEL_RADIUS,SPEED,MASS, hidden_genome):
               
        Number_of_Wheels = 4
        # create a list for each Wheel.
        wheels = [0] * Number_of_Wheels
        
        # set the count to be 0.
        count = 0
        
        # Number of sides wheels can be placed on. (on a real life car this is 2).
        N_Sides = 2
        
        
        # Create a random number between 2 and 16 for number of Wheeels.
        random_num = random_Wheel()
        random_num = (random_num+1)*2

        
        # if 1 pair of wheels place it randomly
        if Number_of_Wheels ==2:        
            # create the length of the car based on the number of wheels
            Len_Car = ((Number_of_Wheels-1)/2)
            # sclae the car so i can call range with a float.
            # Pyrosim plots objects with a centre so an object len 800 is (-400,400)
            Scaled_Car_Len = Len_Car*100
            Wheel_Space_2 = [(np.random.randint(-50,51,1)/100)[0]]
        # if more than 1 pair of wheels place it equal distance.
        else:
            # Set the len of the Car to always be odd.
            Len_Car = ((Number_of_Wheels-1)/2)
            # sclae the car so i can call range with int.
            # Pyrosim plots objects with a centre so an object len 800 is (-400,400)
            Scaled_Car_Len = Len_Car*100
            
            Step_Wheels = int((Scaled_Car_Len*2)/((Number_of_Wheels/2)-1))
            
            Wheel_Space = list(range(int(-(Scaled_Car_Len)),int(Scaled_Car_Len-10),Step_Wheels))
            Wheel_Space_2 = list(map(lambda x: (x/100)*WHEEL_RADIUS, Wheel_Space))
            Wheel_Space_2.append(Len_Car*WHEEL_RADIUS)
        
        
        
        
        # Create a Red Car Body.
        box = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length= Len_Car*2 *
                           WHEEL_RADIUS, width=4 * WHEEL_RADIUS, height=WHEEL_RADIUS,
                           mass=MASS,r=1, g=0, b=0, collision_group = 'robot')
                           
        # create the pole for the car to attach to
        box2 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS*2, length= Len_Car*2 *
                           WHEEL_RADIUS*0.02, width=4 * WHEEL_RADIUS *0.02, height=WHEEL_RADIUS*2,
                           mass=1,r=0, g=1, b=0, collision_group='robot')
                           
        # create a box for the top of the pole.
        box3 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS*3 , length= Len_Car*2 *
                           WHEEL_RADIUS*0.25, width=4 * WHEEL_RADIUS *0.02, height=WHEEL_RADIUS*2,
                           mass=1,r=0, g=1, b=0, collision_group='robot')
                                                                
        # Join the 3 boxes together.                            
        joint = sim.send_hinge_joint( first_body_id = box , second_body_id = box2, lo=0, hi=0)
        joint2 = sim.send_hinge_joint( first_body_id = box2 , second_body_id = box3,lo=0, hi=0)
        
        #if random() == True:
        #    X_Position = 
        #    X_Position = [-Number_of_Wheels/2,
        
        # create the wheels for the car.
        # wheels are spheres and placed accroding to the values in x_pos and y_pos.
        for x_pos in [-2 * WHEEL_RADIUS, 2 * WHEEL_RADIUS]:
            for y_pos in Wheel_Space_2:
                #print(x_pos,y_pos)
                wheels[count] = sim.send_sphere(
                    x=x_pos, y=y_pos, z=WHEEL_RADIUS, radius=WHEEL_RADIUS, r=0, g=0, b=0, collision_group='robot')
                count += 1
        
        
        axles = [0] * Number_of_Wheels
        count = 0
        
        for x_pos in [-2 * WHEEL_RADIUS, 2 * WHEEL_RADIUS]:
            for y_pos in Wheel_Space_2:
                # position_control = False -> continuous range of motion
                axles[count] = sim.send_hinge_joint(first_body_id=wheels[count],
                                                    second_body_id=box, x=x_pos,
                                                    y=y_pos, z=WHEEL_RADIUS,
                                                    n1=1, n2=0, n3=0,
                                                    position_control=False,
                                                    speed=SPEED)
                count += 1
             
       
        post0 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length= 0.01, width=0.01, height=0.01,
                           r=0, g=0, b=1, collision_group = 'robot')
        
        joint0 = sim.send_hinge_joint( first_body_id = box , second_body_id = post0, lo=0, hi=0)
        
        post1 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length= 0.01, width=0.01, height=0.01,
                           r=0, g=0, b=1, collision_group = 'robot')
        joint1 = sim.send_hinge_joint( first_body_id = box , second_body_id = post1, lo=0, hi=0)
        
        post2 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length= 0.01, width=0.01, height=0.01,
                           r=0, g=0, b=1, collision_group = 'robot')
        joint2 = sim.send_hinge_joint( first_body_id = box , second_body_id = post2, lo=0, hi=0)
        
        post3 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length= 0.01, width=0.01, height=0.01,
                           r=0, g=0, b=1, collision_group = 'robot')
        joint3 = sim.send_hinge_joint( first_body_id = box , second_body_id = post3, lo=0, hi=0)
        
        post4 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length= 0.01, width=0.01, height=0.01,
                           r=0, g=0, b=1, collision_group = 'robot')
        joint4 = sim.send_hinge_joint( first_body_id = box , second_body_id = post4, lo=0, hi=0)
        
        post5 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length= 0.01, width=0.01, height=0.01,
                           r=0, g=0, b=1, collision_group = 'robot')
        joint5 = sim.send_hinge_joint( first_body_id = box , second_body_id = post5, lo=0, hi=0)
        
        post6 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length= 0.01, width=0.01, height=0.01,
                           r=0, g=0, b=1, collision_group = 'robot')
        joint6 = sim.send_hinge_joint( first_body_id = box , second_body_id = post6, lo=0, hi=0)
        
        post7 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length= 0.01, width=0.01, height=0.01,
                           r=0, g=0, b=1, collision_group = 'robot')
        joint7 = sim.send_hinge_joint( first_body_id = box , second_body_id = post7, lo=0, hi=0)
        
        post8 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length= 0.01, width=0.01, height=0.01,
                           r=0, g=0, b=1, collision_group = 'robot')
        joint8 = sim.send_hinge_joint( first_body_id = box , second_body_id = post8, lo=0, hi=0)
        
        post9 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length= 0.01, width=0.01, height=0.01,
                           r=0, g=0, b=1, collision_group = 'robot')
        joint9 = sim.send_hinge_joint( first_body_id = box , second_body_id = post9, lo=0, hi=0)
        
        post10 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length= 0.01, width=0.01, height=0.01,
                           r=0, g=0, b=1, collision_group = 'robot')
        joint10 = sim.send_hinge_joint( first_body_id = box , second_body_id = post10, lo=0, hi=0)
        
        post11 = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length= 0.01, width=0.01, height=0.01,
                           r=0, g=0, b=1, collision_group = 'robot')
        
        joint11 = sim.send_hinge_joint( first_body_id = box , second_body_id = post11, lo=0, hi=0)

        # ray sensors spaced Pi/6 radians apart.
        
        rayOffset = 0.1
        raySensors = {}
                
        # 1.00000000e-02,  0.00000000e+00]
        raySensors[0] = sim.send_ray_sensor(body_id = post0, x=-0.01, y=0, z=1.5*WHEEL_RADIUS+rayOffset, r1=1, r2=0, r3=0, max_distance=20)
        
        # [ 8.66025404e-03,  5.00000000e-03],
        raySensors[1] = sim.send_ray_sensor(body_id = post1, x=0.00866, y=0.005, z=1.5*WHEEL_RADIUS+rayOffset, r1=0.866, r2=0.5, r3=0, max_distance=20) 
        
        
        # [ 5.00000000e-03,  8.66025404e-03],
        raySensors[2] = sim.send_ray_sensor(body_id = post2, x=0.005, y=0.00866, z=1.5*WHEEL_RADIUS+rayOffset, r1=0.5, r2=0.866, r3=0, max_distance=20) 
        
        
        # [ 1.73472348e-18,  1.00000000e-02],
        raySensors[3] = sim.send_ray_sensor(body_id = post3, x=0, y=0.01, z=1.5*WHEEL_RADIUS+rayOffset, r1=0, r2=1, r3=0, max_distance=20) 
        
        # [-5.00000000e-03,  8.66025404e-03],
        raySensors[4] = sim.send_ray_sensor(body_id = post4, x=0.005, y=0.00866, z=1.5*WHEEL_RADIUS+rayOffset, r1=0.5, r2=0, r3=0, max_distance=20) 
       
        # [-8.66025404e-03,  5.00000000e-03],
        raySensors[5] = sim.send_ray_sensor(body_id = post5, x=-0.00866, y=0.005, z=1.5*WHEEL_RADIUS+rayOffset, r1=-0.866, r2=0.5, r3=0, max_distance=20) 
        
        # [-1.00000000e-02,  5.20417043e-18],
        raySensors[6] = sim.send_ray_sensor(body_id = post6, x=-0.01, y=0, z=1.5*WHEEL_RADIUS+rayOffset, r1=-1, r2=0, r3=0, max_distance=20) 
        
        # [-8.66025404e-03, -5.00000000e-03],
        raySensors[7] = sim.send_ray_sensor(body_id = post7, x=-0.00866, y=-0.005, z=1.5*WHEEL_RADIUS+rayOffset, r1=-0.866, r2=-0.5, r3=0, max_distance=20) 
        
         # [-5.00000000e-03, -8.66025404e-03],
        raySensors[8] = sim.send_ray_sensor(body_id = post8, x=-0.005, y=-0.00866, z=1.5*WHEEL_RADIUS+rayOffset, r1=-0.5, r2=-0.866, r3=0, max_distance=20)
        
         # [-8.67361738e-18, -1.00000000e-02],
        raySensors[9] = sim.send_ray_sensor(body_id = post9, x=0, y=-0.01, z=1.5*WHEEL_RADIUS+rayOffset, r1=0, r2=-1, r3=0, max_distance=20) 
        
        # [ 5.00000000e-03, -8.66025404e-03],
        raySensors[10] = sim.send_ray_sensor(body_id = post10, x=-0.005, y=-0.00866, z=1.5*WHEEL_RADIUS+rayOffset, r1=0.5, r2=-0.866, r3=0, max_distance=20) 
        
        # [ 8.66025404e-03, -5.00000000e-03]])
        raySensors[11] = sim.send_ray_sensor(body_id = post11, x=-0.00866, y=-0.005, z=1.5*WHEEL_RADIUS+rayOffset, r1=0.866, r2=-0.5, r3=0, max_distance=20)         
        
        
        # add sensor neurons
        sensorNeurons = {}
        for i, s in (raySensors.items()):
            sensorNeurons[i] = sim.send_sensor_neuron(s)
        
        # # hidden layer 1
        # hiddenNeurons = {}
        # #numHiddenNeurons = 24
        # for i in range(c.numHiddenNeurons):
        #     hiddenNeurons[i] = sim.send_hidden_neuron()
        
        # # weightings between sensor neurons and hidden layer
        # self.hidden_weights = hidden_genome
        # # self.hidden_weights2 = hidden_genome2
        
        # # connect sensor neurons to hidden neurons 1
        # for hidden_weight_i, s in sensorNeurons.items():
        #     for hidden_weight_j, h in hiddenNeurons.items():
        #         sim.send_synapse(s, h, weight=self.hidden_weights[hidden_weight_i, hidden_weight_j])
    
        
        # motor neurons
        mneurons = [0] * Number_of_Wheels
        for i in range(Number_of_Wheels):
            mneurons[i] = sim.send_motor_neuron(axles[i],tau = 0.3)
            #sim.send_synapse(bias, mneurons[i], weight=random2())
        
        # weight matrix
        self.weight_array= genome
        
        # # connect hidden neurons to motor neurons
        # for weight_i, h in hiddenNeurons.items():
        #     for weight_j, m in enumerate(mneurons):
        #         sim.send_synapse(h, m, weight = self.weight_array[weight_i, weight_j])
                
                
        # connect sensor neurons to motor neurons
        for weight_i, s in (sensorNeurons.items()):
            for weight_j, m in enumerate(mneurons):
                sim.send_synapse(s, m, weight = self.weight_array[weight_i, weight_j])
        
        
        # Can set surface area to a constraint
        Surface_Area = Number_of_Wheels*4*math.pi*WHEEL_RADIUS**2 + 2*Len_Car*2*WHEEL_RADIUS*4 * WHEEL_RADIUS*WHEEL_RADIUS
        
        # create a sensor to detect the collision between the ball and robot - do we need this if we just assign the robot to collision group?
        self.tsensor_id = sim.send_touch_sensor(body_id = box)
        self.position = sim.send_position_sensor(body_id = box)

    
