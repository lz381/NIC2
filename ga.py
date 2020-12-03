from population import POPULATION

# generate intial population
parents = POPULATION(popsize=5)
parents.Initialize()
parents.Evaluate()
parents.Print()
    
generations = 100
POPSIZE = 5


for i in range(generations):
    
    children = POPULATION(popsize=POPSIZE)
    
    # selection and mutation
    children.Fill_From(parents)
    print("\n Generation ", i, ":")
    children.Evaluate()
    children.Print()
    parents = children

# best solution
parents.p[0].Start_Evaluation(pb=False)
parents.p[0].Compute_Fitness()



