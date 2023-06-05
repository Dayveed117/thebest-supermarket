import random, math
import numpy as np

class Selection():
    """
    Selection methods from a population of chromossoms (specimens)
    """

    @classmethod
    def random_selection(cls, population, **kwargs):
        """
        Randomly select chromossomes for next generation

        population : list
            A copy of population of a genetic algorithm
        """
        unlucky = random.randint(0, len(population) - 1)
        held = population.pop(unlucky)

        return held

    @classmethod
    def proportional_selection(cls, population, **kwargs):
        """
        Select based on fitness - higher fitness higher chance to survive

        population : list
            A copy of population of a genetic algorithm
        """

        # Extract fit_method from kwargs
        fit_method = kwargs["fit_method"]
        epsilon = np.random.uniform(0, 1)
        fitsum = 0
        i = 0

        for c in population:
            fitsum += fit_method(c)

        s = fit_method(population[i]) / fitsum

        while s < epsilon:
            i += 1
            s += fit_method(population[i]) / fitsum

        held = population.pop(i)
        return held

    @classmethod
    def tournament_selection(cls, population, **kwargs):
        """
        Selection based on tournament

        population : list
            A copy of population of a genetic algorithm
        """

        try:
            fit_method = kwargs["fit_method"]
            t_size = kwargs["t_size"]

            if t_size < 0 or t_size > len(population):
                raise KeyError()

        except KeyError:
            if len(population) >= 4:
                t_size = math.floor(len(population) * 0.5)
            else:
                t_size = len(population)

        # Create a bracket of t_size elements
        # Create temporary list so that brackets dont have duplicates
        bracket = []
        waschosen = []
        for _ in range(t_size):

            # TODO : Not very performant
            # bracket = random.sample(population, t_size) ??
            while True:
                # One random index within current population range
                chosen = random.randint(0, len(population) - 1)
                if chosen not in waschosen:
                    waschosen.append(chosen)
                    break

            bracket.append( (chosen, population[chosen]) )

        # Assume best element is in index 0
        best = (bracket[0][0], bracket[0][1])
        bf = fit_method(best[1])

        # Find most fit within bracket
        for i, c in bracket:
            cf = fit_method(c)
            if cf > bf:
                best = (i, c)
                bf = cf

        held = population.pop(best[0])
        return held

    @classmethod
    def elitist_selection(cls, population, **kwargs):
        """
        Select the most fit individual of the given population

        population : list
            A copy of population of a genetic algorithm
        """

        fit_method = kwargs["fit_method"]

        best = (0, population[0])
        bf = fit_method(best[1])

        for i, c in enumerate(population):
            cf = fit_method(c)
            if cf > bf:
                best = (i, c)
                bf = cf

        held = population.pop(best[0])
        return held
