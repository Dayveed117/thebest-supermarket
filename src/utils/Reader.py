"""
Reader module for 'TheBest Supermarket' input files
"""


import os
import sys
import pandas as pd
import json
from utils.Parser import Parser
from utils.Writer import Writer
from pandas.core.frame import DataFrame
from utils.Analyzer import Analyzer as Anal


class Reader:
    """
    Reader class for abstraction on reading input files
    """

    FILESPERFOLDER = 10000
    CSTMR_FOLDER = 'resources/customers/'
    CSTMR_TMPLT = 'resources/customers/NIF_'
    PRDTS_TMPLT = 'resources/products_checkpoint/product_'
    FPGWT_TMPLT = 'resources/fpgrowth_checkpoint/fpgrowth_'

    @classmethod
    def read_produtos(cls, products_file: str) -> DataFrame:
        # region
        """
        Read 'products.txt' text file and return dict.

        Arguments
        ---------
        products_file : str
            Path to products.txt file.

        Returns
        -------
        pandas DataFrame or dictionary of parsed information in products.txt file.
        """
        # endregion

        if not os.path.isfile(products_file):
            raise FileNotFoundError(
                f"FileNotFoundError : ( {products_file} ) file not found\n"
            )

        df = pd.DataFrame(pd.read_csv(products_file, sep="\t", encoding="utf-8"))
        df = df.set_index("Nome")

        return df

    @classmethod
    def read_receipts(
        cls, recpt_folder: str, expln_folder: str, products_df: DataFrame, i: int
    ):
        # region
        """Read receipts corresponding explanation.

        Arguments
        ---------
        recpt_folder : str
            Template for receipts folder path.
        expln_folder : str
            Template for explanations folder path.
        i : int
            Current folder iteration.
        """
        # endregion


        out_fpgrowth = f"{Reader.FPGWT_TMPLT}{i}.csv"
        out_products = f"{Reader.PRDTS_TMPLT}{i}.csv"

        # First  -- Product Count for this folder
        # Second -- Product Random count for this folder
        products_data = [[0, 0] for _ in range(len(products_df.index))]

        # Batch size and buffers
        batchsize = 250
        batch_client = []
        batch_coded = []

        sys.stderr.write(f"Reading folder {i}...\n")

        #      0             1                     49
        # (0 ~ 9999) (10 000 ~ 19 999) .. (490 000 ~~ 49 999)
        for k in range(Reader.FILESPERFOLDER * i, Reader.FILESPERFOLDER * (i + 1)):

            # region PARSE RECEIPTS / EXPLANATIONS
            f_receipt = f"{recpt_folder}/{i}/receipt_{k}.txt"
            f_explanation = f"{expln_folder}/{i}/explanation_{k}.txt"

            if not os.path.isfile(f_receipt):
                raise FileNotFoundError(
                    f"FileNotFoundError : {f_receipt} files not found\n"
                )

            if not os.path.isfile(f_explanation):
                raise FileNotFoundError(
                    f"FileNotFoundError : {f_explanation} files not found\n"
                )

            # Open receipt file
            with open(f_receipt, "r") as receipt:
                receipt.reconfigure(encoding="utf-8")
                lines = receipt.readlines()

                # Parse text file
                receipt_dict = Parser.parse_receipt(lines)

            # Open explanation file
            with open(f_explanation, "r") as explanation:
                explanation.reconfigure(encoding="utf-8")
                lines = explanation.readlines()

                # Parse explanations file
                explanation_dict = Parser.parse_explanation(lines)
            # endregion

            # region ANALYZERS PER FILE
            client_data = Anal.extract_client_oriented(
                receipt_dict, explanation_dict, products_df, k
            )

            # Products coded in unique number
            random_products = client_data[5]
            coded_products = client_data[6]

            Anal.count_products(products_data, coded_products, random_products)
            # endregion

            # region WRITERS PER FILE
            nif = receipt_dict["NIF"]
            customer_file = f"{Reader.CSTMR_TMPLT}{nif}.csv"

            batch_client.append([customer_file, client_data])
            batch_coded.append(coded_products)
            # Minimize file access
            if ((k+1) % batchsize == 0):
                Writer.dump_client_csv_multi(batch_client)
                Writer.dump_data_csv_multi(out_fpgrowth, batch_coded)
                # Clear buffers
                batch_client.clear()
                batch_coded.clear()
            # endregion


        # region WRITERS PER FOLDER
        Writer.dump_data_csv_multi(out_products, products_data)
        # endregion

        sys.stderr.write(f"Finished reading folder {i}.\n")


    @classmethod
    def combine_checkpoints(cls, numfoders : int, products_df : DataFrame) -> None:
        """
        Combine analysis checkpoints to generate final files for analysis
        """

        customer_file_names  = []
        product_file_names   = []
        fpgrowth_file_names  = []
        final_fpgrowth_path  = 'resources/fpgrowth_final.csv'
        final_products_path  = 'resources/products_final.json'
        final_customers_path = 'resources/customers_final.json'

        # region FILLING LIST WITH FILENAMES
        for _,_,fnames in os.walk(Reader.CSTMR_FOLDER):
            for f in fnames:
                fname = f'{Reader.CSTMR_FOLDER}{f}'
                customer_file_names.append(fname)

        for i in range(numfoders):
            in_products = f"{Reader.PRDTS_TMPLT}{i}.csv"
            in_fpgrowth = f"{Reader.FPGWT_TMPLT}{i}.csv"

            # Append file names
            product_file_names.append(in_products)
            fpgrowth_file_names.append(in_fpgrowth)
        # endregion

        # Combine data that needs ot be combined
        products_dict = Anal.combine_product_checkpoints(product_file_names, products_df)
        print('Combining product data...')
        Writer.dump_final_dict(final_products_path, products_dict)
        print('Combining fpgrowth data...')
        Writer.dump_total_fpgrowth(final_fpgrowth_path, fpgrowth_file_names)

        # Combining customer data
        print('Combining customer data...')
        customers_dict = Anal.generate_customer_files(customer_file_names)
        Writer.dump_final_dict(final_customers_path, customers_dict)

        print('All done!')

    @classmethod
    def analyze_finals(cls, customers_final_path, products_final_path) -> None:
        """
        Query-like functions to final customers and products final dicts
        """

        customer_file_names = []

        for _,_,fnames in os.walk(Reader.CSTMR_FOLDER):
            for f in fnames:
                fname = f'{Reader.CSTMR_FOLDER}{f}'
                customer_file_names.append(fname)

        with open(customers_final_path, 'r') as fin:
            customers_dict = json.load(fin)
            Anal.print_top_x_customers_by_y(customers_dict, 100, 'Total')
            Anal.print_top_x_customers_by_y(customers_dict, 100, 'Profit')

        with open(products_final_path, 'r') as fin:
            products_dict = json.load(fin)
            Anal.print_top_x_products_by_y(products_dict, 50, 'Sold')
            Anal.print_top_x_products_by_y(products_dict, 50, 'Random')
            Anal.print_top_x_products_by_y(products_dict, 50, 'Profit')

