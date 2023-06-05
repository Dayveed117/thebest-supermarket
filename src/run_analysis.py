"""
Main module for Analysis of input files for Supermarket analysis Data Science Project
"""


import time
import json
from pprint import pprint
from fpgrowth_py.fpgrowth import fpgrowthFromFile

import os
import sys
import traceback
from os import mkdir
from os.path import isdir
from shutil import rmtree
from multiprocessing import Process
from utils.Reader import Reader
from utils.Writer import Writer


def prep_part_1():
    def recreate_folders(path):
        if isdir(path):
            rmtree(path)
        mkdir(path)

    recreate_folders("resources/customers")
    recreate_folders("resources/fpgrowth_checkpoint")
    recreate_folders("resources/products_checkpoint")

def prep_part_2():

    def elim_file(path):
        if os.path.isfile(path):
            os.remove(path)

    elim_file('resources/customers_final.json')
    elim_file('resources/products_final.json')
    elim_file('resources/fpgrowth_final.csv')

def do_etl_part_1():

    PRODUTOS = "resources/Products.txt"
    RECPT_TMPLT = "resources/receipts/"
    EXPLN_TMPLT = "resources/explanations/"
    NUMFOLDERS = 50

    try:
        # TODO : COMMENT IF USING CHECKPOINT
        # prep_part_1()
        products_df = Reader.read_produtos(PRODUTOS)
        processes = []

        for i in range(NUMFOLDERS):
            args = (
                RECPT_TMPLT,
                EXPLN_TMPLT,
                products_df,
                i,
            )
            p = Process(target=Reader.read_receipts, args=args)
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        # partial_receipts = partial(Reader.read_receipts, RECPT_TMPLT, EXPLN_TMPLT, products_df)
        # with ProcessPoolExecutor() as executor:
        #     executor.map(partial_receipts, NUMFOLDERSP)

        # for i in range(NUMFOLDERS):
        #     Reader.read_receipts(RECPT_TMPLT, EXPLN_TMPLT, products_df, i)

    except Exception:
        traceback.print_exception(*sys.exc_info())

def do_etl_part_2():

    PRODUTOS = "resources/Products.txt"
    NUMFOLDERS = 50

    try:
        prep_part_2()
        products_df = Reader.read_produtos(PRODUTOS)
        Reader.combine_checkpoints(NUMFOLDERS, products_df)
    except Exception:
        traceback.print_exception(*sys.exc_info())

def last_pass():

    CUSTOMERS_PATH = "resources/customers_final.json"
    PRODUCTS_PATH = "resources/products_final.json"

    try:
        Reader.analyze_finals(CUSTOMERS_PATH, PRODUCTS_PATH)
    except Exception:
        traceback.print_exception(*sys.exc_info())

def do_fpgrowth():

    FPGROWTH_PATH = "resources/fpgrowth_final.csv"
    print('Timing fpgrowth\n')

    # Results give first the itemset and then the rules

    s1 = time.time()
    results = fpgrowthFromFile(FPGROWTH_PATH, 0.5, 0)
    f1 = time.time()

    freqset = results[0]
    rules = results[1]

    print(f'Time -- 0.5 CONF -- {f1-s1}')
    pprint(freqset)
    pprint(rules)

    print('---------------------------')

    s2 = time.time()
    results2 = fpgrowthFromFile(FPGROWTH_PATH, 0.1, 0)
    f2 = time.time()

    freqset2 = results2[0]
    rules2 = results2[1]

    print(f'Time -- 0.1 CONF -- {f2-s2}')
    pprint(freqset2)
    pprint(rules2)

    print('---------------------------')

    s3 = time.time()
    results3 = fpgrowthFromFile(FPGROWTH_PATH, 0.05, 0)
    f3 = time.time()

    freqset3 = results3[0]
    rules3 = results3[1]

    print(f'Time -- 0.05 CONF -- {f3-s3}')
    pprint(freqset3)
    pprint(rules3)

    print('---------------------------')

    s4 = time.time()
    results4 = fpgrowthFromFile(FPGROWTH_PATH, 0.05, 0)
    f4 = time.time()

    freqset4 = results4[0]
    rules4 = results4[1]

    print(f'Time -- 0.01 CONF -- {f4-s4}')
    pprint(freqset4)
    pprint(rules4)

    print('---------------------------')

def main2():

    # Testing stuff

    PRODUTOS = "resources/Products.txt"
    products_final = "resources/products_final.json"
    products_df = Reader.read_produtos(PRODUTOS)

    # Número total de prateleiras para cada produto
    available = products_df['Total Prateleiras'].values
    assoc_dict = dict([(p,c+1) for (c,p) in enumerate(products_df.index)])

    ordered_profit = []

    def snd(tuple):
        return tuple[1]

    with open(products_final, 'r') as fin:
        prod_dict = json.load(fin)

        # lst = [(v['Name'], v['Profit']) for _,v in prod_dict.items()]
        lst = [(v['Name'], v['Sold']) for _,v in prod_dict.items()]
        slst = sorted(lst, key=snd, reverse=True)

        # Most sold first from the back
        for i,v in enumerate(slst):
            ordered_profit.append(assoc_dict[v[0]])

    sol = []
    i = 0

    while len(sol) < 248:

        product_code = ordered_profit[i]

        if available[product_code - 1] > 0:
            sol.append(product_code)
            available[product_code - 1] += (-1)

        i += 1
        if i == len(ordered_profit):
            i = 0

    pprint(ordered_profit)
    pprint(sol)

    sol.reverse()

    Writer.dump_data_csv_single('sales_conf.csv', sol)
    # Writer.dump_data_csv_single('profit_conf.csv', sol)


if __name__ == "__main__":
    print("Which python interpreter is executing the file?")
    print(sys.executable)

    # CORRECT ORDER OF EXECUTION

    # Segment the data in receipts and explanations
    # do_etl_part_1()

    # Recombine checkpoints and generate final files
    # do_etl_part_2()

    # Extract rules and itemsets
    # do_fpgrowth()

    # Analyze final customers, products and fpgrowth
    # last_pass()

    # Testing
    main2()
