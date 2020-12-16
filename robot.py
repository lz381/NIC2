class ROBOT:
    """
    Robot blueprints.
    """
    def __init__(self, sim, wheel_size):
               
        WHEEL_RADIUS = wheel_size
        SPEED = 10
        
        wheels = [0] * 4
        count = 0
        for x_pos in [-2 * WHEEL_RADIUS, 2 * WHEEL_RADIUS]:
            for y_pos in [-2 * WHEEL_RADIUS, 2 * WHEEL_RADIUS]:
                
                wheels[count] = sim.send_sphere(x=x_pos, y=y_pos, z=WHEEL_RADIUS, radius=WHEEL_RADIUS, b=0, g=0, r=1)
                count += 1
        
        box = sim.send_box(x=0, y=0, z=1.5 * WHEEL_RADIUS, length=4 *
                           WHEEL_RADIUS, width=5 * WHEEL_RADIUS, height=WHEEL_RADIUS,
                           mass=10, collision_group = 'robot', b=1, g=0, r=0)
        
        axles = [0] * 4
        count = 0
        
        for x_pos in [-2 * WHEEL_RADIUS, 2 * WHEEL_RADIUS]:
            for y_pos in [-2 * WHEEL_RADIUS, 2 * WHEEL_RADIUS]:
                # position_control = False -> continuous range of motion
                axles[count] = sim.send_hinge_joint(first_body_id=wheels[count],
                                                    second_body_id=box, x=x_pos,
                                                    y=y_pos, z=WHEEL_RADIUS,
                                                    n1=1, n2=0, n3=0,
                                                    position_control=False,
                                                    speed=SPEED)
                count += 1
        
        bias = sim.send_bias_neuron()
        
        mneurons = [0] * 4
        for i in range(4):
            mneurons[i] = sim.send_motor_neuron(axles[i])
            sim.send_synapse(bias, mneurons[i], weight=-1.0)
        
        self.position = sim.send_position_sensor(body_id = box)
        # create a sensor to detect the collision between the ball and robot
        self.tsensor_id = sim.send_touch_sensor(body_id = box)
        
        #sim.film_body(box, method='follow')


    
