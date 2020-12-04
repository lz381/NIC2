class ENVIRONMENT:
    
    def __init__(self, env_id):
        self.ID = env_id
        print(self.ID)
        
        self.ball_radius = 0.2
        self.ball_z = self.ball_radius
        
        
        
    def Send_To(self, sim):
        
        # first shot at goal
        if self.ID == 0:
            ball = sim.send_sphere(x=0, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=0, y=-10, z=0, time=5)
        
        # second shot at goal    
        if self.ID == 1:
            ball = sim.send_sphere(x=2, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=0, y=-10, z=0, time=5)
        
        # third shot at goal
        if self.ID == 2:
            ball = sim.send_sphere(x=-2, y=6, z=self.ball_z, radius=self.ball_radius, collision_group = 'ball')
            sim.send_external_force(ball, x=0, y=-10, z=0, time=5)

                
        
        