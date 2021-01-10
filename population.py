"""
This module has implementation of population initialization, evaluation (fitness computation) and genetic operators
like mutation, crossover, elitism, and tournament selection.
"""

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
        """Initialization method of the Population class. It generates an empty population of individuals
        (i.e. an empty dictionary representing population)
        popsize: Number of individuals required in the population (i.e. population size)
        return: None
        """
        # empty population of individuals
        self.p = {}
        self.popsize=popsize

    def Print(self):
        """
        Method to print the fitness of all individuals in population
        return: None
        """
        for i in self.p:
            self.p[i].Print()

    def Evaluate(self, envs, pb=True):
        """
        Evaluate each individual in the population over the specified simulation environments. Computes the final
        fitness score of each individual by taking the average over number of environments.
        envs: collection of simulation environments over which the population has to be evaluated
        pb: play_blind argument for Simulator class of pyrosim : bool, optional
            If True the simulation runs without graphics (headless) else if
            False the simulation runs with graphics (the default is False)
        return: None
        """
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
        """
        Evaluate an individual from the population (used mostly to evaluate winner after tournament selection)
        envs: collection of simulation environments over which the population has to be evaluated
        pb: play_blind argument for Simulator class of pyrosim : bool, optional
            If True the simulation runs without graphics (headless) else if
            False the simulation runs with graphics (the default is False)
        return: None
        """
        # get the winner from the population
        winner = self.find_winner()

        for e in envs.envs:
            # evaluate winner individual in population for visual
            winner.Start_Evaluation(env=envs.envs[e], pb=pb)
            winner.sim.wait_to_finish()
        # fitness is already computed
        print("\n Fitness of Winner from last generation: ", winner.fitness)

    def find_winner(self):
        """
        Find the individual having best fitness score from the population.
        return: best individual (winner)
        """
        # with the elitism size > 1, winner could be any one of the first few in the population(coz of implementation)
        # hence finding the winner individual first
        a = []
        for i in self.p:
            a.append(self.p[i].fitness)
        a = np.array(a)

        best_individual_ind = np.argpartition(a, -1)[-1:]  # get the index of winner
        
        return self.p[best_individual_ind[0]]

    def Initialize(self):
        """
        Generates the initial population of individuals. Empty dictionary representing population is filled with desired
        number of individuals having traits like genome, robot wheel size, mass etc randomly initialized.
        return: None
        """
        for i in range(0, self.popsize):
            self.p[i] = INDIVIDUAL(i)
    
    def Mutate(self):
        """
        Implements mutation genetic operator. It mutates the whole population.
        return: None
        """
        for i in range(0, self.popsize):
            self.p[i].Mutate()
            
    def Copy_Best_From(self, other, elite_size):
        """
        Copy the few best parents into the first few slots of the child population. No of best parents to be
         copied to next generation is decided from the elitism rate (elite_size).
        other: Other represents the immediate previous generation of parents
        elite_size: number of best individuals to be copied to next children generation.
        return: None
        """
        # ELITISM - select best solution from parent pop (other) to include in children population
        # ELITISM - elite_size to decide the no of best solutions to be copied in children generation
        a = []
        for i in other.p:
            a.append(other.p[i].fitness)
        a = np.array(a)
        best_individual_ind = np.argpartition(a, -elite_size)[-elite_size:]
        # copy the best individuals to next children generation
        for i, idx in enumerate(best_individual_ind):
            self.p[i] = copy.deepcopy(other.p[idx])

    def Collect_Children_From(self, other, elite_size):
        """
        For each of the empty slots left after elite individuals are copied in the child population,
          a. Select two parents at random from parent gen.
          b. Determine which has the higher fitness.
          c. If crossover is enabled, select another winner from parent gen through tournament selection and perform
                crossover between the two parents else skip this step.
          d. Create a mutant from this winner and store it in the empty slot.
        other: Other represents the immediate previous generation of parents
        elite_size: number of best individuals to be copied to next children generation.
        return: None
        """
        # fill other solutions with mutated children
        
        for i in other.p:
            # skip first few best solutions (as these are few best solutions copied from parents for elitism)
            if i in range(0, elite_size):
                continue
            
            # tournament selection to select children to mutate and store
            winner = other.Tournament_Selection()
            
            # select another winner from parent gen through tournament selection and perform
            # crossover between the two parents if crossover is enabled
            if c.crossover_enabled:
                parent2 = other.Tournament_Selection()
                # perform (single-sided) crossover
                winner.Crossover(parent2)
            
            # MUTATION
            winner.Mutate()
            self.p[i] = copy.deepcopy(winner)
           
    def Fill_From(self, other):
        """
        Copies the elite individuals from parent generation according to the elitism rate and fill the remaining slots
        of child population with individuals selected from parent generation through tournament selection and then
        changed by performing mutation and crossover (if enabled).
        other: Other represents the immediate previous generation of parents
        return: None
        """
        # elitism : elitism_rate to decide the no of best solutions to be copied in children generation
        elite_size = int(self.popsize * c.elitismRate / 100)
        self.Copy_Best_From(other, elite_size)
        # selection and mutation
        self.Collect_Children_From(other, elite_size)

    def Tournament_Selection(other):
        """
        Performs binary tournament selection on the parent generation. Randomly selects the two individuals from the
        parent generation and evaluates the winner that has highest fitness score.
        return: Winner - Individual with highest fitness score among the two.
        """
        # binary tournament selection function
        parent1_idx, parent2_idx = np.random.choice(range(other.popsize), size=2)
        parent1 = other.p[parent1_idx]
        parent2 = other.p[parent2_idx]
        
        if parent1.fitness > parent2.fitness:
            return parent1
        else:
            return parent2
