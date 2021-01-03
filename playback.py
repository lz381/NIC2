from environments import ENVIRONMENTS
import constants as c
import pickle


envs = ENVIRONMENTS()

with open('RobotReplayGen_0.p', 'rb') as f:
    best = pickle.load(f)
    for i in range(c.numEnvs):
        best.Start_Evaluation(env=envs.envs[i], pb=False)
        best.sim.wait_to_finish()
    print('Fitness of the best in this generation: ', best.fitness)
