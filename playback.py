from environments import ENVIRONMENTS
import constants as c
import pickle


envs = ENVIRONMENTS()

with open('RobotReplayGen_0.p', 'rb') as f:
    best = pickle.load(f)
    for i in range(c.numEnvs):
        best.Start_Evaluation(env=envs.envs[i], pb=False)
        best.Compute_Fitness()

# with open('RobotReplayGen_0.p', 'rb') as f:
#     best = pickle.load(f)
#     for i in range(c.numEnvs):
#         best.Start_Evaluation(env=envs.envs[i], pb=False)
#         best.Compute_Fitness()
    
# with open('RobotReplayGen_0.p', 'rb') as f:
#     best = pickle.load(f)
#     for i in range(c.numEnvs):
#         best.Start_Evaluation(env=envs.envs[i], pb=False)
#         best.Compute_Fitness()

# with open('RobotReplayGen_0.p', 'rb') as f:
#     best = pickle.load(f)
#     for i in range(c.numEnvs):
#         best.Start_Evaluation(env=envs.envs[i], pb=False)
#         best.Compute_Fitness()