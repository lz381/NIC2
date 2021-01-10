"""
environment module has ENVIRONMENT class to simulate the pyrosim
"""


class ENVIRONMENT:
    """
    Sets the environment for evaluation of virtual creature robots. It defines the structure and position of goal post.
    It also defines the 10 ball shots which are directed towards the goal with certain force and angle. These ball shots
    are a target for the goal keeper robot to stop.
    """
    def __init__(self, env_id):
        """
        Initialize an environment. It sets an environment ID, ball_radius, ball_z, ball_psensor_id.
        return: None
        """
        self.ID = env_id

        # ball params
        self.ball_radius = 0.16
        self.ball_z = self.ball_radius
        self.ball_psensor_id = 0
        
    def Send_To(self, sim):
        """
        Defines the 10 ball shots which are directed towards the goal with certain force and angle. These ball shots
        are a target for the goal keeper robot to stop. Each environment simulates a different starting position,
        application of force and direction on the ball.
        """
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
        
        
        # first shot at goal
        if self.ID == 0:
            ball = sim.send_sphere(x=0, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=0, y=-10, z=0, time=5)
            
          
        # second shot at goal    
        if self.ID == 1:
            ball = sim.send_sphere(x=1, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=0, y=-10, z=0, time=5)
    

        
        # third shot at goal
        if self.ID == 2:
            ball = sim.send_sphere(x=-1, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=0, y=-10, z=0, time=5)

           
        # fourth shot
        if self.ID == 3:
            ball = sim.send_sphere(x=-0, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=-6, y=-10, z=0, time=5)


        # Fifth Shot
        if self.ID == 4:
            ball = sim.send_sphere(x=0, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=-4, y=-12, z=0, time=5)
            
            
        #Sixth Shot
        if self.ID == 5:
            ball = sim.send_sphere(x=0, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=4, y=-12, z=0, time=5)
        
        # Seventh Shot
        if self.ID == 6:
            ball = sim.send_sphere(x=-2.5, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=8, y=-12, z=0, time=5)

        # Eighth shot
        if self.ID == 7:
            ball = sim.send_sphere(x=2.5, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=-8, y=-12, z=0, time=5)

        # Nineth shot
        if self.ID == 8:
            ball = sim.send_sphere(x=-2.5, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=4, y=-12, z=0, time=5)

        # Tenth Shot
        if self.ID == 9:
            ball = sim.send_sphere(x=2.5, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=-4, y=-12, z=0, time=5)
                
        # retrieve the position sensor id for the ball
        self.ball_psensor_id = sim.send_position_sensor(body_id = ball)
