import dask.dataframe as dd
from dask.diagnostics import ProgressBar
import sys
import csv


class LoanAggregate(object):
    """
    This class envelops the methods and data used to store data aggregates
    It should be instantiated with an input filename, then execute should be called.
    To save the result, call write_csv with the the output filename as parameter.
    """
    input_file = ""

    def __init__(self, filename):
        self.input_file = filename
        self.parse_csv()

    def execute(self):
        """
        Shortcut to prepare the computation and perform it after instantiating the class
        """
        self.prepare_computation()
        self.compute()

    def parse_csv(self):
        """
        Loads the structure of an input CSV file of loans into a Dask dataFrame
        """
        dataframe = dd.read_csv(self.input_file)
        # These lines trim the quotation marks and unused date information from the rows
        dataframe["Network"] = dataframe["Network"].map(lambda x: x[1:-1])
        dataframe["Date"] = dataframe["Date"].map(lambda x: x[4:7])
        dataframe["Product"] = dataframe["Product"].map(lambda x: x[1:-1])
        self.dataframe = dataframe

    def prepare_computation(self):
        """
        Defines the Dask computations to be performed on our dataFrame
        """
        dataframe = self.dataframe
        # The sum and count of loan amounts are aggregated below for each network, product, and month
        networks = dataframe.groupby("Network").Amount.agg(["sum", "count"])
        products = dataframe.groupby("Product").Amount.agg(["sum", "count"])
        months = dataframe.groupby("Date").Amount.agg(["sum", "count"])
        self.data_set = networks, products, months

    def compute(self):
        """
        Simply perform the Dask computations while showing a progress bar
        """
        with ProgressBar():
            self.values = dd.compute(*self.data_set)

    def write_csv(self, output_file):
        """
        Save a properly formatted CSV file of computed loan aggregates
        """
        with open(output_file, 'w', newline='') as output:
            writer = csv.writer(output, dialect='excel')
            writer.writerow(('Network/Product/Month', 'Sum', 'Count'))
            for computation in self.values:
                for line_tuple in computation.to_records(index=True):
                    line = (line_tuple[0], "{:0.2f}".format(line_tuple[1]), line_tuple[2])
                    writer.writerow(line)


def main():
    """
    Runs the module using a Loans CSV file passed by CLI argument as input
    """
    if len(sys.argv) < 2 or sys.argv[1] == help:
        print("----- JUMO Loan Validation helper -----")
        print("Please specify an input file as argument, e.g. 'python aggregate.py loans.csv'")
        quit(1)
    loan_aggregate = LoanAggregate(sys.argv[1])
    loan_aggregate.execute()
    loan_aggregate.write_csv("Output.csv")

if __name__ == '__main__':
    main()
