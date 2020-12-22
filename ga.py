from population import POPULATION
from environments import ENVIRONMENTS
import constants as c
#import constants

envs = ENVIRONMENTS()

# generate intial population
parents = POPULATION(popsize=c.popSize)
parents.Initialize()
parents.Evaluate(envs=envs)

parents.Print()
    
for i in range(c.numGens):
    
    children = POPULATION(popsize=c.popSize)
    
    # selection and mutation
    children.Fill_From(parents)
    print("\n Generation ", i, ":")
    children.Evaluate(envs=envs)
    children.Print()
    parents = children

# visual check of last gen population
parents.Evaluate(envs=envs, pb=False)






