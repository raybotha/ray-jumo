
--- JUMO Loan Validation Tool ---
Coding test - Raymond Botha

----------------
Project Details
----------------
Given a CSV file from the accounting department, this Python program calculates the aggregate
loans given out on the Jumo networks by the tuple of (Network, Product, Month). For each of
these, the sum and count of issued loans is calculated. The result is saved to Output.csv,
as instructed in the assignment. The program is expected to be run every two months.

-----------
Assumptions
-----------
The most important assumption I've made is that the input CSV file of loans follows a strict format,
the exact format given in the assignment. I believe this is a safe assumption since the data is
computer-generated. If the system generating the data changes, minor changes will have to be made
to the parsing script.

This program will be run from a command line interface with the loan file passed as an argument in order
to maximise its applications, for example: easily running the tool as a cron-job or through other
automated means. If need be it can be adapted to a simple GUI or CLI with a prompt.

-----------------------------------------
Assumptions about scaling and performance
-----------------------------------------

The time and space complexity of my solution follows the assumption that Jumo will calculate aggregates
for less than one hundred million loans, assuming this program is to be run on a standard laptop computer.
I've tested the extremes of input loan size by writing a small program to generate randomized loan data
for up to millions of loans (program included in the testing directory). Using a loan CSV file of exactly
ten million loans, my solution successfully runs in 15 seconds, never using more than 500 MB of memory.
If every mobile money account in Africa made a Jumo loan once a year, the two-month aggregate could be
calculated on a laptop in less than a minute.

--------------------------------
Choice of language and libraries
--------------------------------

I've chosen Python since it's a highly favored language for data analysis, especially in finance, and
it's the language I'm most skilled in. Python strikes a great balance between scale and sophistication
in data science.

For a simple task like calculating aggregates, it would be easy to just use Python's csv module and
iterate over the CSV file's lines, extracting tbe data and storing networks, products and months in a
dictionary whilst calculating a running average and count. But this approach would quickly degrade once
the scale of loans is increased, or the data-points used for validation changes.
For dealing with the problems of scale and performance, I've used the Dask library, which is a parallel
computing library that wraps most of the Pandas data processing library. Dask ensures that memory
constraints are kept in mind when loading and manipulating a large list of loans, and that CPU multiprocessing
is fully utilised. In case of massive scale, Dask can easily be set to run on several clients in a distributed
computing system.

I've used the standard Python CSV module to write the output file, there's no need to optimise here.

---------------
Setup and Usage
---------------

1.  Make sure Python 3.6 is installed, with the Python and pip directories added to the environment path
    during setup.
2.  Open a command line and go to the ray-jumo directory.
3.  Run 'pip install -r requirements.txt' (this works in a virtual environment as well).
    Now you're ready to go!

4.  Run 'python aggregate.py Loans.csv' where Loans.csv is the input, I've included the input given with
    the assignment.
5.  The output file is stored as 'Output.csv' - best viewed in Excel/spreadsheet apps.

-------------
Extra Testing
-------------
I wrote a small Python program to generate randomized loan data, in order to test how well my solution
performs at extremes. I only tested up to ten million loans, since generating random data in Python at a large scale
takes about twenty times longer than analysing it.

-Tool included in testing directory.
-Make sure the main requiremnets are installed, one of these (Faker) is exclusively used here for random dates.
-Run with 'python gencsv.py <n>' - n is for specifying how many loans to generate, here n specifies 10 to the power n
 loans, so 'python gencsv.py 6' would generate one million random loans.
-The randomised data is stored as generated_loans.csv.