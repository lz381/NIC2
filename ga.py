from population import POPULATION
from environments import ENVIRONMENTS
import constants as c
import csv
import pickle

instant_replay = [1, round(c.numGens/4), round(c.numGens/2), round((c.numGens/4)*3), c.numGens-1]
count = 0


with open("mo1_nw4_sp10_wt12_ws10_wn100.csv", "w", newline="") as f:
    # Header creation for columns - stores gen num, parent solution ID, and solution number in pop
    header = ['Generation']
    for i in range(c.popSize):
        header.append("ParentID")
        header.append('Solution_' + str(i+1))
    writer = csv.writer(f, delimiter=',')
    writer.writerow(header)
 
    envs = ENVIRONMENTS()

    # generate intial population
    parents = POPULATION(popsize=c.popSize)
    parents.Initialize()
    parents.Evaluate(envs=envs)

    parents.Print()

        
    for i in range(c.numGens):

        # Write data to csv
        line = [i]
        for j in range(c.popSize):
            line.append(parents.p[j].ID)
            line.append(parents.p[j].fitness)
        writer.writerow(line)    

        if i in instant_replay:
            filename = "RobotReplayGen_" + str(count) + ".p"
            with open(filename, "wb") as f:
                pickle.dump(parents.p[0], f)

        children = POPULATION(popsize=c.popSize)
        
        # selection and mutation
        children.Fill_From(parents)
        print("\n Generation ", i+1, ":")
        children.Evaluate(envs=envs)
        children.Print()
        parents = children

# visual check of last gen population
parents.Evaluate(envs=envs, pb=False)






