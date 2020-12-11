class ENVIRONMENT:
    
    def __init__(self, env_id):
        self.ID = env_id

        # ball params
        self.ball_radius = 0.16
        self.ball_z = self.ball_radius
        
        
        
    def Send_To(self, sim):
        
        # goalpost params
        goal_width = 5
        goal_height = 2
        
        # goalpost object
        left_post = sim.send_cylinder(x=goal_width/2, y=0, z=goal_height/2, length=goal_height, radius=0.05, collision_group = 'goalpost', mass=999)
        right_post = sim.send_cylinder(x=-goal_width/2, y=0, z=goal_height/2, length=goal_height, radius=0.05, collision_group = 'goalpost', mass=999)
        crossbar = sim.send_cylinder(x=0, y=0, z=goal_height, r1=1, r2=0, r3=0, length=goal_width, radius=0.05, collision_group = 'goalpost', mass=999)
        sim.send_fixed_joint(left_post, crossbar)
        sim.send_fixed_joint(right_post, crossbar)
        
        
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
           
        # for jumping robots?
        if self.ID == 3:
            ball = sim.send_sphere(x=-0, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=-24, y=-60, z=30, time=5)

                
        
        