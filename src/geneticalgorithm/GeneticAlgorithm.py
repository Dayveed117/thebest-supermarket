import numpy as np
import pandas as pd
import random
from GeneticFitness import Fitness
from GeneticSelection import Selection
from GeneticReproduction import Reproduction

class GeneticAlgorithm():
    """
    Encapsulation of methods and variables capable with the purpose to solve problems using genetic algorithms
    """

    def __init__(self, n_pop, v_range, n_variables, seed=123454321, fit_method="fun1"):
        """
        n_pop : int
            Number of chromossomes for the algorithm
        v_range : (float, float)
            Range for the values in each alell of the chromossom
        n_features : int
            Number of alells in each chromossom
        fit_method : str
            Name of the fitness method used for this algorithm
        seed : int
            Seed to initiate random number generator
        """
        super().__init__()
        np.random.seed(seed)
        random.seed(seed)
        # The actual method bound to an instance attribute
        self.fit_method = getattr(Fitness, fit_method, Fitness.fun1)
        self.population = [ np.random.uniform(v_range[0], v_range[1], n_variables) for n in range(n_pop) ]

    def swap_fit_method(self, fit_method):
        """
        Change fitness method for this genetic algorithm

        fit_method : str
            String representation of fitness method to be swapped in
        """
        self.fit_method = getattr(Fitness, fit_method, self.fit_method)

    def print_most_fit(self):
        """
        Prints most fit individual in current population
        """

        best = (0, self.fit_method(self.population[0]), self.population[0])

        for i, c in enumerate(self.population):
            cf = self.fit_method(c)
            if cf > self.fit_method(best[2]):
                best = (i, cf, c)

        print("Most fit is Specimen {0} = {1}\n{2}".format(best[0]+1, best[1], best[2]))

    def get_most_fit(self):

        tmp = self.population.copy()
        tmp.sort(reverse=True, key=self.fit_method)
        v = self.fit_method(tmp[0])

        return v

    def print_population(self):
        """
        Prints every individual with information regarding to its index, its fitness, and its alells
        """
        for i, chrom in enumerate(self.population):
            print("Chromossome {0}:\nFitness = {1}\n{2}".format(i+1, self.fit_method(chrom), chrom))

    def sort_by_fitness(self):
        """
        Create and return a descending sorted list of fitness according to the current population
        """
        # fitness_list = list(map(self.fit_method, self.population))
        fitness_list = [ self.fit_method(chrom) for chrom in self.population ]
        fitness_list.sort(reverse=True)

        return fitness_list

    @classmethod
    def class_sort_by_fitness(cls, population, fit_method='fun1'):
        """
        Create and return a descending sorted list of fitness according to the given population and fitness method

        population : list
            A series of individuals whose data has to match the fitness method
        fit_method : string
            Name of the fitness method to be used
        """
        method = getattr(Fitness, fit_method, Fitness.fun1)
        fitness_list = [ method(chrom) for chrom in population]
        fitness_list.sort(reverse=True)

        return fitness_list

    def select(self, num, sel_method="random", **kwargs):
        """
        Select "num" specimens using a specific selection method 'sel_method'

        num : int
            Number of specimens to be selected with the specified method
        sel_method : str
            Representation of selection method as string
        """

        if "t_size" in kwargs.keys():
            t_size = kwargs["t_size"]
        else:
            t_size = None

        try:
            if num < 0 or num > len(self.population):
                raise ValueError("Num should be in range [0, len(population)]\n")

            else:
                # Extract method from GeneticSelection class
                method = getattr(Selection, sel_method+"_selection", Selection.random_selection)

                tmp_population = self.population.copy()
                selected = []

                for _ in range(num):
                    # Get a specimen from a selection method
                    selected.append(method(tmp_population,
                        fit_method = self.fit_method,
                        t_size = t_size)
                    )

                return selected

        except Exception as e:
            print(e)

    def reproduce_cross_over(self, selected, num, co_method, **kwargs):
        """
        Reproduce current selected sample using a cross over method

        selected : list
            List of selected individuals for reproduction
        num : int
            Number of reproductions to do within selected group
        co_method : str
            String representative of cross_over method
        """

        if "pm" in kwargs.keys():
            pm = kwargs["pm"]
        else:
            pm = 0.3

        method = getattr(Reproduction, co_method+"_cross_over_reproduction", Reproduction.arithmetic_cross_over_reproduction)
        children = []

        for _ in range(num):
            # Get two new children alpha and beta
            c1, c2 = method(selected, pm=pm)
            children.append(c1)
            children.append(c2)

        # Extend the current population
        self.population.extend(children)

    def reproduce_mutation(self, selected, num, mut_method, pm, **kwargs):
        """
        Reproduce current selected sample using a mutation method

        selected : list
            List of selected individuals for reproduction
        num : int
            Number of reproductions to do within selected group
        mut_method : str
            String representative of mutation method
        """

        method = getattr(Reproduction, mut_method+"_mutation_reproduction", Reproduction.arithmetic_mutation_reproduction)

        # This only works if there is no repeated chromossome within population
        # Does not work yet
        real_indices = [self.population.index(c) for c in selected]

        for _ in range(num):
            method(real_indices, pm, fit_method=self.fit_method, population=self.population)

    def evolve(self, num):
        """
        Choose the best 'num' specimens for next generation

        num : int
            Number of chromossomes to take place in next generation
        """

        try:
            if num < 1:
                raise ValueError("Population has to have at least length 1")
            else:
                self.population.sort(reverse=True, key=self.fit_method)
                # It is of no problem for num to be beyond max range
                self.population = self.population[:num]
                random.shuffle(self.population)

        except Exception as e:
            print(e)
