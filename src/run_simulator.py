"""
Attempt of simulator for "TheBest" Supermarket
"""

import os
import random
import numpy as np
import networkx as nx
from csv import reader
from pprint import pprint
from networkx.exception import NetworkXNoPath
from utils.Analyzer import Analyzer as Anal
from utils.Reader import Reader

def apply_filter(n, map_filter, config : bool) -> int:
    """Filter for mapping shelves and floor into a vector or matrix

    config : bool
        True  -- Floor tiles are mapped
        False -- Shelves are mapped
    """

    if n in [0, 22, 482, 460]:
        return 4

    if n == 114:
        return 3

    if n == 413:
        return 2

    if config:
        if n in map_filter:
            return 1
        return 0

def print_matrix(matrix) -> None:

    for row in matrix:
        for el in row:
            print(el, end=' ')
        print()
    print()

def get_adjacency_dict():

    def get_tile_index(dimy, x, y) -> int:
        """
        Get tile according to supermarket tile number
        """
        return (x*dimy + y) + 1

    def make_adjacency(matrix):

        (x,y) = matrix.shape

        # if [x,y] is 0 then no adjency
        # if [x,y] is 1 then adjency with every cell around it
        # if [x,y] is 2 or 3 then adjency with the cell left of itself

        adjacency_dict = {}

        for i in range(x):

            for j in range(y):

                ind = get_tile_index(y, i, j)

                # No adjacency for shelves
                if matrix[i][j] == 0:
                    adjacency_dict[ind] = []

                # Full adjacency for every tile
                elif matrix[i][j] == 1:
                    # Tiles cannot be borders, hence no need to out of bounds exceptions
                    l = get_tile_index(y, i, j-1)
                    r = get_tile_index(y, i, j+1)
                    u = get_tile_index(y, i-1, j)
                    d = get_tile_index(y, i+1, j)
                    adjacency_dict[ind] = [l, u, r, d]

                # Ignore corners
                elif matrix[i][j] == 4:
                    pass

                # If cell is start or end, then adjacency on left tile
                else:
                    l = get_tile_index(y, i, j-1)
                    adjacency_dict[ind] = [l]


        return adjacency_dict

    no_shelf_filter = [
            24,25,26,27,28,29,
            30,31,32,33,34,35,36,37,38,39,
            40,41,42,43,44,47,
            63,64,65,67,
            70,86,87,88,
            90,93,94,95,96,97,98,99,
            100,101,102,103,104,105,106,107,108,109,
            110,111,112,113,116,117,118,119,
            120,121,122,123,124,125,126,127,128,129,
            130,131,132,133,134,135,136,139,
            155,156,159,162,178,179,
            182,185,186,187,188,189,
            190,191,192,193,194,195,196,197,198,199,
            200,201,202,203,204,205,208,
            224,225,226,227,228,
            231,247,248,
            251,254,255,256,257,258,259,
            260,261,262,263,264,265,266,267,268,269,
            270,271,274,277,279,
            280,281,282,283,284,285,286,287,288,289,
            290,291,292,293,294,297,
            300,316,317,318,319,320,323,
            339,340,341,342,343,346,347,348,349,
            350,351,352,353,354,355,356,357,358,359,
            360,361,362,363,366,369,
            370,371,372,373,374,375,376,377,378,379,
            380,381,382,383,384,385,386,389,
            392,408,409,412,415,431,432,435,438,439,
            440,441,442,443,444,445,446,447,448,449,
            450,451,452,453,454,455,456,457,458]

    walkable_filter = [apply_filter(i, no_shelf_filter, True) for i in range(483)]

    # Reshaping for visualization and adjacency maker
    walkable = np.asarray(walkable_filter, dtype=int).reshape([21,23])
    walkable_adjacency = make_adjacency(walkable)

    return walkable_adjacency, walkable

def get_stamina_distribution():

    customer_file_names = []

    for _,_,fnames in os.walk(Reader.CSTMR_FOLDER):
        for f in fnames:
            fname = f'{Reader.CSTMR_FOLDER}{f}'
            customer_file_names.append(fname)

    kde = Anal.generate_stamina_distribution(customer_file_names)

    return kde

def pull_wishlist(n):
    """
    Pull a number n of wishlists randomly from customers
    """

    customer_file_names = []

    for _,_,fnames in os.walk(Reader.CSTMR_FOLDER):
        for f in fnames:
            fname = f'{Reader.CSTMR_FOLDER}{f}'
            customer_file_names.append(fname)

    wishlist_list = []
    for _ in range(n):

        # Random integer for list index
        random_index = random.randint(0, len(customer_file_names) - 1)

        with open(customer_file_names[random_index], 'r') as fin:
            csv_reader = reader(fin, delimiter=',')
            numlines = csv_reader.line_num

            # Random integer for line num
            rand_line = random.randint(0, numlines - 1)
            row = list(iter(csv_reader))[rand_line]

            # Index 4 is wishlist
            wishlist = row[4]
            wishlist_list.append(wishlist)

    return wishlist_list

def get_configuration():

    PRODUTOS = "resources/Products.txt"
    products_df = Reader.read_produtos(PRODUTOS)

    # Index corresponds to the product itself
    to_place_in_shelves = products_df['Total Prateleiras'].values

    pass

def main():

    # Make adjancency dict for path finding
    adjacency_dict,m = get_adjacency_dict()

    # Make djikstra graph from adjacency dict?
    G = nx.DiGraph(adjacency_dict)

    print_matrix(m)

    pprint(adjacency_dict)

    pprint(nx.dijkstra_path(G, 414, 386))

    # Stamina distribution for customer stamina
    # stamina_pool = get_stamina_distribution()

    # Wishlists to be run for initial customers
    # wishlists_to_run = pull_wishlist(1000)

    # Start genetic algorithm
    # ...

if __name__ == '__main__':
    random.seed(469)
    main()
