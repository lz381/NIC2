from individual import INDIVIDUAL
import copy
import numpy as np
import constants as c

np.random.seed(c.randomSeed)

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
                self.p[i].Compute_Fitness(metric=c.fitnessMetric)
        
        # final fitness is average fitness over number of environments
        for i in self.p:
            self.p[i].fitness = self.p[i].fitness / len(envs.envs)
            
    def Evaluate_Winner(self, envs, pb=False):

        # with the elitism size > 1, winner could be any one of the first few in the population(coz of implementation)
        # hence finding the winner individual first
        a = []
        for i in self.p:
            a.append(self.p[i].fitness)
        a = np.array(a)
        best_individual_ind = np.argmax(a)  # get the index of winner

        for e in envs.envs:
            # evaluate winner individual in population for visual
            self.p[best_individual_ind].Start_Evaluation(env=envs.envs[e], pb=pb)
            self.p[best_individual_ind].sim.wait_to_finish()
        # fitness is already computed
        print("\n Fitness of Winner from last generation: ", self.p[best_individual_ind].fitness)
            
    def Initialize(self):
        
        # generate random population of individuals
        for i in range(0, self.popsize):
            self.p[i] = INDIVIDUAL(i)
    
    def Mutate(self):
        for i in range(0, self.popsize):
            self.p[i].Mutate()
            
    def Copy_Best_From(self, other, elite_size):
        
        # ELITISM - select best solution from parent pop (other) to include in children population
        # ELITISM - elite_size to decide the no of best solutions to be copied in children generation
        a = []
        for i in other.p:
            a.append(other.p[i].fitness)
        a = np.array(a)
        best_individual_ind = np.argpartition(a, -elite_size)[-elite_size:]

        for i, idx in enumerate(best_individual_ind):
            self.p[i] = copy.deepcopy(other.p[idx])

    def Collect_Children_From(self, other, elite_size):
        
        # fill other solutions with mutated children
        
        for i in other.p:
            # skip first few best solutions (as these are few best solutions copied from parents for elitism)
            if i in range(0, elite_size):
                continue
            
            # tournament selection to select children to mutate and store
            winner = other.Tournament_Selection()
            
            # MUTATION
            winner.Mutate()
            self.p[i] = copy.deepcopy(winner)
           
    def Fill_From(self, other):
        # elitism : elitism_rate to decide the no of best solutions to be copied in children generation
        elite_size = int(self.popsize * c.elitismRate / 100)
        self.Copy_Best_From(other, elite_size)
        # selection and mutation
        self.Collect_Children_From(other, elite_size)

    def Tournament_Selection(other):
        
        # binary tournament selection function
        parent1_idx, parent2_idx = np.random.choice(range(other.popsize), size=2)
        parent1 = other.p[parent1_idx]
        parent2 = other.p[parent2_idx]
        
        if parent1.fitness > parent2.fitness:
            return parent1
        else:
            return parent2
