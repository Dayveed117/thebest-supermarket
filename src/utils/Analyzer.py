"""
Analyzer module for 'TheBest Supermarket'
"""

import numpy
from csv import reader
from typing import Any, List
from pandas.core.frame import DataFrame
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt

def snd(tuple):
    return tuple[1]

def calculate_profit(products : List[int], p_df : DataFrame) -> float:

    tot_profit = 0.0

    for p in products:

        price  = p_df['Preço'].values[p-1]
        profit = p_df['Margem Lucro'].values[p-1] * 0.01
        tot_profit += price * profit

    return tot_profit

class Analyzer:

    @classmethod
    def extract_client_oriented(cls, r_dict : dict, e_dict : dict, p_df : DataFrame, receipt_num : int) -> List[Any]:
        """

        """
        # Association dict for every product and their code
        assoc_dict = dict([(p,c+1) for (c,p) in enumerate(p_df.index)])

        # Receipt_num / Total in receipt / Stamina for this receipt
        receipt = f'receipt_{receipt_num}'
        total   = r_dict['TOTAL']
        stamina = e_dict['STAMINA']

        # Encoded product lists
        coded_products = [assoc_dict[p] for p in r_dict['Products']]
        coded_wishlist = [assoc_dict[p] for p in e_dict['Wishlist']]
        coded_random   = [assoc_dict[p] for p in e_dict['Random Products']]

        # Profit for this receipt
        profit  = calculate_profit(coded_products, p_df)

        return [receipt, total, profit, stamina, coded_wishlist, coded_random, coded_products]

    @classmethod
    def count_products(cls, data, coded_products, coded_random) -> None:
        """

        """
        # Add counter to product
        for p in coded_products:
            data[p-1][0] += 1

            # This product was also picked by chance
            if p in coded_random:
                data[p-1][1] += 1

    @classmethod
    def combine_product_checkpoints(cls, fins : List[str], p_df : DataFrame) -> dict:
        """

        """
        products_dict = {}
        total_products = [[0,0] for _ in range(165)]
        profit_column = p_df['Margem Lucro'].values

        # Fill final list with product count and random count
        for fname in fins:

            with open(fname, 'r') as f:
                csv_reader = reader(f, delimiter=',')
                for i,v in enumerate(csv_reader):
                    total_products[i][0] += int(v[0])
                    total_products[i][1] += int(v[1])


        # Create dictionary for the product
        for j,p in enumerate(p_df.index):

            total_sold_for_p = total_products[j][0]
            total_random_for_p = total_products[j][1]
            product_profit = total_sold_for_p * (profit_column[j] * 0.01)

            d = {
                'Name' : p,
                'Sold' : total_sold_for_p,
                'Random' : total_random_for_p,
                'Profit' : round(product_profit, 3)
            }

            products_dict.update({(j+1) : d})

        return products_dict

    @classmethod
    def generate_customer_files(cls, fins : List[str]) -> dict:
        """
           0       1       2       3        4        5        6
        receipt, total, profit, stamina, wishlist, random, products
        """

        customer_dict = {}

        # For each customer csv file
        for fname in fins:

            # Total | Profit | Stamina | Num Receipts
            customer_info = [0.0, 0.0, 0.0, 0]
            customer_nif = fname[-12:-4]
            print(customer_nif)

            # For each receipt
            with open(fname, 'r') as f:
                csv_reader = reader(f, delimiter=',')

                for j,row in enumerate(csv_reader):
                    customer_info[0] += float(row[1])
                    customer_info[1] += float(row[2])
                    customer_info[2] += float(row[3])

                # Number of receipts for a customer
                customer_info[3] = (j+1)

            d = {
                'Spent' : round(customer_info[0], 1),
                'Profit' : round(customer_info[1], 3),
                'Average Stamina' : round(customer_info[2] / customer_info[3], 1)
            }

            # Insert customer in final customer dict
            customer_dict.update({customer_nif : d})

            # Clear buffer
            customer_info.clear()

        return customer_dict

    @classmethod
    def print_top_x_customers_by_y(cls, customers_dict : dict, x : int, y : str) -> None:

        valid = ['Spent', 'Profit', 'Average Stamina']

        if y not in valid:
            print(f'Customers do not have metric {y}')
            return

        lst = [(k, v[y]) for k,v in customers_dict.items()]
        slst = sorted(lst, key=snd, reverse=True)

        print('----------------------------------')
        print(f'TOP {x} THEBEST CUSTOMERS - BY {y}')
        for i,v in enumerate(slst[:x]):
            print(f'{i+1} - {v[0]} with {v[1]}')
        print('----------------------------------')

    @classmethod
    def print_top_x_products_by_y(cls, products_dict : dict, x : int, y : str) -> None:

        valid = ['Sold', 'Random', 'Profit']

        if y not in valid:
            print(f'Products do not have metric {y}')
            return

        lst = [(v['Name'], v[y]) for _,v in products_dict.items()]
        slst = sorted(lst, key=snd, reverse=True)

        print('----------------------------------')
        print(f'TOP {x} THEBEST PRODUCTS - BY {y}')
        for i,v in enumerate(slst[:x]):
            print(f'{i+1} - {v[0]} with {v[1]}')
        print('----------------------------------')

    @classmethod
    def generate_stamina_distribution(cls, fins : List[str]):
        """
        Iteratate over every customer checkpoint
        Get stamina value from each receipt
        Plot stamina density
        """

        # Adapted from
        # https://www.askpython.com/python/examples/density-plots-in-python

        stamina_buffer = []

        for fname in fins:

            with open(fname, 'r') as f:
                csv_reader = reader(f, delimiter=',')

                # 4th column in customer files is stamina for that receipt
                for row in csv_reader:
                    stamina_buffer.append(float(row[3]))

        # Gaussian object
        kde = gaussian_kde(stamina_buffer)
        kde.covariance_factor = lambda : .5
        kde._compute_covariance()

        limits = numpy.linspace(100, 700, 1200)

        plt.plot(limits, kde(limits))
        plt.show()

        return kde
