import sys
sys.path.insert(0, '../..')
import pyrosim # noqa
import numpy as np
import random
import math

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
<<<<<<< Updated upstream
    def __init__(self, sim, genome,WHEEL_RADIUS,SPEED,MASS):
=======
    def __init__(self, sim, genome, hidden_genome):
>>>>>>> Stashed changes
               
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
        joint = sim.send_hinge_joint( first_body_id = box , second_body_id = box2)
        joint2 = sim.send_hinge_joint( first_body_id = box2 , second_body_id = box3)
        
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
             
        # dex426-patch-1
        # create a weight matrix - im a little confused by this looking at other code examples i believe i want
        # it to be a matrix with the number of wheels and touch sensors, but wheels are always touching the ground.
        #### Example Video www.youtube.com/watch?v=GcWJXxrKNk
        
        # ray sensors spaced Pi/6 radians apart.
        
        raySensors = {}
        raySensors[0] = sim.send_ray_sensor( body_id = box, x=0, y=0, z=1.5*WHEEL_RADIUS, r1=1, r2=0,r3=0)
        raySensors[1] = sim.send_ray_sensor( body_id = box, x=0, y=0, z=1.5*WHEEL_RADIUS, r1=1, r2=math.pi*1/6,r3=0) 
        raySensors[2] = sim.send_ray_sensor( body_id = box, x=0, y=0, z=1.5*WHEEL_RADIUS, r1=1, r2=math.pi*2/6,r3=0) 
        raySensors[3] = sim.send_ray_sensor( body_id = box, x=0, y=0, z=1.5*WHEEL_RADIUS, r1=1, r2=math.pi*3/6,r3=0) 
        raySensors[4] = sim.send_ray_sensor( body_id = box, x=0, y=0, z=1.5*WHEEL_RADIUS, r1=1, r2=math.pi*4/6,r3=0) 
        raySensors[5] = sim.send_ray_sensor( body_id = box, x=0, y=0, z=1.5*WHEEL_RADIUS, r1=1, r2=math.pi*5/6,r3=0) 
        raySensors[6] = sim.send_ray_sensor( body_id = box, x=0, y=0, z=1.5*WHEEL_RADIUS, r1=1, r2=math.pi*6/6,r3=0) 
        raySensors[7] = sim.send_ray_sensor( body_id = box, x=0, y=0, z=1.5*WHEEL_RADIUS, r1=1, r2=math.pi*-1/6,r3=0) 
        raySensors[8] = sim.send_ray_sensor( body_id = box, x=0, y=0, z=1.5*WHEEL_RADIUS, r1=1, r2=math.pi*-2/6,r3=0)
        raySensors[9] = sim.send_ray_sensor( body_id = box, x=0, y=0, z=1.5*WHEEL_RADIUS, r1=1, r2=math.pi*-3/6,r3=0) 
        raySensors[10] = sim.send_ray_sensor( body_id = box, x=0, y=0, z=1.5*WHEEL_RADIUS, r1=1, r2=math.pi*-4/6,r3=0) 
        raySensors[11] = sim.send_ray_sensor( body_id = box, x=0, y=0, z=1.5*WHEEL_RADIUS, r1=1, r2=math.pi*-5/6,r3=0)         
        
        
        # add sensor neurons
        sensorNeurons = {}
        for i, s in (raySensors.items()):
            sensorNeurons[i] = sim.send_sensor_neuron(s)
            
            
        
        
        hiddenNeurons = {}
        numHiddenNeurons = 12
        for i in range(numHiddenNeurons):
            hiddenNeurons[i] = sim.send_hidden_neuron()
        
        self.hidden_weights = hidden_genome
        
        # connect sensor neurons to hidden neurons
        for hidden_weight_i, s in sensorNeurons.items():
            for hidden_weight_j, h in hiddenNeurons.items():
                sim.send_synapse(s, h, weight=self.hidden_weights[hidden_weight_i, hidden_weight_j])
            
        # motor neurons
        mneurons = [0] * Number_of_Wheels
        for i in range(Number_of_Wheels):
            mneurons[i] = sim.send_motor_neuron(axles[i],tau = 0.3)
            #sim.send_synapse(bias, mneurons[i], weight=random2())
        
        # weight matrix
        self.weight_array= genome
        
        # connect hidden neurons to motor neurons
        #for weight_i, s in (sensorNeurons.items()):
        for weight_i, h in hiddenNeurons.items():
            for weight_j, m in enumerate(mneurons):
                sim.send_synapse(h, m, weight = self.weight_array[weight_i, weight_j])
        
        
        # Can set surface area to a constraint
        Surface_Area = Number_of_Wheels*4*math.pi*WHEEL_RADIUS**2 + 2*Len_Car*2*WHEEL_RADIUS*4 * WHEEL_RADIUS*WHEEL_RADIUS
        
        # create a sensor to detect the collision between the ball and robot - do we need this if we just assign the robot to collision group?
        self.tsensor_id = sim.send_touch_sensor(body_id = box)
        self.position = sim.send_position_sensor(body_id = box)

    
