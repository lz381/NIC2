"""
This module has the the implementation of genetic algorithm for virtual robots. Using this algorithm, a generation of
robots is evolved to be able to perform the task of goal-keeping.
The algorithm is outlined as below:
a. Create and evaluate a population of n parents.
b. For each generation,

    c. Create an empty child population.

    d. Copy the few best parents into the first few slots of the child population as per the elitism rate.

    e. For each of the empty slots left after elite individuals are copied in the child population,

          f. Select two parents at random.

          g. Determine which has the higher fitness.

          h. If crossover is enabled, select another winner from parent generation through tournament selection and
            perform crossover between the two parents else skip this step.

          i. Create a mutant from this winner and store it in the empty slot.

    j. Evaluate each individual in the child population.

    k. Replace the parent population with the child population.
"""

from population import POPULATION
from environments import ENVIRONMENTS
import constants as c
import csv
import pickle
import random
import numpy as np

# This is the generations that will be recorded, just went for 1/4*numGens
instant_replay = [1, round(c.numGens/4), round(c.numGens/2), round((c.numGens/4)*3), c.numGens-1]
print(instant_replay)
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

    # setting the random seed
    np.random.seed(c.randomSeed)
    random.seed(c.randomSeed)

    # generate initial population
    parents = POPULATION(popsize=c.popSize)
    parents.Initialize()
    # Evaluating the first gen of parents
    parents.Evaluate(envs=envs)

    parents.Print()

    for i in range(c.numGens):

        # Write data to csv
        line = [i]
        for j in range(c.popSize):
            line.append(parents.p[j].ID)
            line.append(parents.p[j].fitness)
        writer.writerow(line)    

        # If the gen number is right, then it saves the replay of the best individual in the that generation
        if i in instant_replay:
            filename = "RobotReplayGen_" + str(i) + ".p"
            best_of_gen = parents.find_winner()
            with open(filename, "wb") as f:
                pickle.dump(best_of_gen, f)

        # Start of actual GA
        children = POPULATION(popsize=c.popSize)
        
        # selection and mutation
        children.Fill_From(parents)
        print("\n Generation ", i+1, ":")
        children.Evaluate(envs=envs)
        children.Print()
        parents = children

# visual check of the best solution in the last generation
parents.Evaluate_Winner(envs=envs)

