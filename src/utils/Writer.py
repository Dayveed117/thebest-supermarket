"""
Writer module for 'TheBest Supermarket'
"""


import json
from csv import writer, reader


class Writer:

    @classmethod
    def dump_data_csv_single(cls, fout, data):

        with open(fout, 'a', newline='') as fp:
            w = writer(fp, delimiter=',')
            w.writerow(data)

    @classmethod
    def dump_data_csv_multi(cls, fout, data):

        with open(fout, 'a', newline='') as fp:
            w = writer(fp, delimiter=',')
            w.writerows(data)

    @classmethod
    def dump_client_csv_multi(cls, data):

        for (path,dat) in data:

            with open(path, 'a', newline='') as fp:
                w = writer(fp, delimiter=',')
                w.writerow(dat)

    @classmethod
    def dump_final_dict(cls, fout, final_dict):

        with open(fout, 'w') as f:
            json.dump(final_dict, f, indent=2)

    @classmethod
    def dump_total_fpgrowth(cls, fout, fnames):
        """

        """
        # Abrir um ficheiro csv
        # Abrir todos os checkpoints e colocar dentor do anterior
        with open(fout, 'w', newline='') as fo:

            csv_writer = writer(fo, delimiter=',')
            transactions = []

            # For every checkpoint
            for fname in fnames:

                with open(fname, 'r') as fi:
                    csv_reader = reader(fi, delimiter=',')

                    # Read every transaction made in checkpoinit and append to list
                    for row in csv_reader:
                        transactions.append(row)

                csv_writer.writerows(transactions)
                transactions.clear()

