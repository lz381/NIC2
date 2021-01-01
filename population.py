from individual import INDIVIDUAL
import copy
import numpy as np


np.random.seed(42)

class POPULATION:
    """
    Population of individual robot simulations.
    """
    def __init__(self, popsize):
        
        # empty population of individuals
        self.p = {}
        self.popsize=popsize
        
        
    def Print(self):
        # print fitness of all individuals in population
        for i in self.p:
            self.p[i].Print()

    
    def Evaluate(self, envs, pb=True):
        
        # reset fitness to 0 before evaluation to ensure no carry-over from previous gens
        for i in self.p:
            self.p[i].fitness = 0
        
        # compute fitness for each environment
        for e in envs.envs:
            
            # evaluate each individual in population
            for i in self.p:
                self.p[i].Start_Evaluation(env = envs.envs[e], pb=pb)
                
            # compute fitness of each individual in population
            for i in self.p:
                #self.p[i].Compute_Fitness(metric="goals_scored")
                #self.p[i].Compute_Fitness(metric="distance_travelled")
                self.p[i].Compute_Fitness(metric="best_keeper")
        
        # final fitness is average fitness over number of environments
        for i in self.p:
            self.p[i].fitness = self.p[i].fitness / len(envs.envs)
            
    def Evaluate_Winner(self, envs, pb=False):
        for e in envs.envs:
            self.p[0].Start_Evaluation(env=envs.envs[e], pb=False)
            
            self.p[0].Compute_Fitness(metric="best_keeper")
            
        self.p[0].fitness = self.p[0].fitness / len(envs.envs)
        print("\nFinal Fitness of Winner: ", self.p[0].fitness)
            
            
    def Initialize(self):
        
        # generate random population of individuals
        for i in range(0, self.popsize):
            self.p[i] = INDIVIDUAL(i)
    
    def Mutate(self):
        for i in range(0, self.popsize):
            self.p[i].Mutate()
            
    def Copy_Best_From(self, other):
        
        # ELITISM - select best solution from parent pop (other) to include in children population
        best_fitness = 0
        best_individual_index = 0
        
        for i in other.p:
            fitness = other.p[i].fitness
            
            if fitness >= best_fitness:
                best_fitness = fitness
                best_individual_index = i
        
        best_individual = copy.deepcopy(other.p[best_individual_index])
        
        self.p[0] = best_individual        
    
    
    def Collect_Children_From(self, other):
        
        # fill other solutions with mutated children
        
        for i in other.p:
            # skip first solution (as this is best solution copied from parents for elitism)
            if i == 0:
                continue
            
            # tournament selection to select children to mutate and store
            winner = other.Tournament_Selection()
            
            # MUTATION
            winner.Mutate()
            self.p[i] = copy.deepcopy(winner)
           
    def Fill_From(self, other):
        # elitism
        self.Copy_Best_From(other)
        # selection and mutation
        self.Collect_Children_From(other)
        

    def Tournament_Selection(other):
        
        # binary tournament selection function
        parent1_idx, parent2_idx = np.random.choice(range(other.popsize), size=2)
        parent1 = other.p[parent1_idx]
        parent2 = other.p[parent2_idx]
        
        if parent1.fitness > parent2.fitness:
            return parent1
        else:
            return parent2
