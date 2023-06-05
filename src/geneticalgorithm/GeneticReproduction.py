import numpy as np
import random

class Reproduction():
    """
    Reproduction functions within a population of chromossomes
    """

    @classmethod
    def arithmetic_cross_over_reproduction(cls, selected, **kwargs):
        """
        Cross over reproduction methods, such as
        uniform, 1point, 2point, arithmetic

        selected : list
            Selected sample from the population of genetic algorithm
        """
        # Only arithmetic for now

        # Randomly select parent from selected
        p1 = selected[random.randint(0, len(selected)-1)]
        p2 = selected[random.randint(0, len(selected)-1)]

        # To make sure parents are not the same
        while p2 is p1:
            p2 = selected[random.randint(0, len(selected)-1)]


        """
        If pulling randoms is only made once
        (eps1, eps2) = (np.random.uniform(0, 1), np.random.uniform(0, 1))
        alpha = [ eps1 * p1[i] + (1 - eps1) * p2[i] for i,_ in enumerate(p1) ]
        beta  = [ (1 - eps2) * p1[i] + eps2 * p2[i] for i,_ in enumerate(p1) ]
        """

        (alpha, beta) = ([], [])

        for i,_ in enumerate(p1):
            # Calculating random for every gene of the parent chromossome
            (eps1, eps2) = (np.random.uniform(0, 1), np.random.uniform(0, 1))

            alpha.append( eps1 * p1[i] + (1 - eps1) * p2[i] )
            beta.append( (1 - eps2) * p1[i] + eps2 * p2[i] )

        return (alpha, beta)


    @classmethod
    def arithmetic_mutation_reproduction(cls, r_indices, pm, **kwargs):
        """
        Mutation reproduction methods, such as
        random, inorder, non-binary variables

        r_indices : list
            List of indices of every selected chromossome in real population
        pm : float
            Mutation probability
        fit_method : str
            Fitness method for chromossom
        """

        fit_method = kwargs["fit_method"]
        r_population = kwargs["population"]

        # Random index in indice list length range
        r = random.randint(0, len(r_indices)-1)

        # Randomly selected individual from population that was in selected group
        to_mutate = r_population[r_indices[r]]
        # Standard deviation is inversely proportional to fitness
        std_d = 1/fit_method(to_mutate)

        for alell in range(len(to_mutate)):
            eps = np.random.uniform(0, 1)
            eta = np.random.uniform(0, std_d)

            # If small numebr
            if eps <= pm:
                to_mutate[alell] += eta

        # Save mutation in real population
        r_population[r_indices[r]] = to_mutate
