from environments import ENVIRONMENTS
import constants as c
import pickle


envs = ENVIRONMENTS()

with open('RobotReplayGen_0.p', 'rb') as f:
    best = pickle.load(f)
    best.Start_Evaluation(env=envs.envs[0], pb=False)
    best.Compute_Fitness()