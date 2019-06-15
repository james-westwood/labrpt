#!/usr/bin/env python3

# Generate reports from lab results.
# Run like:
#   python3 labrpt.py [--db <database>.csv] [--corpus <corpus>.yml] <data>.csv
#       --> Output written to <data>.txt
#       There are default values for <database> and <corpus>.
# E.g.
#   python3 labrpt.py --db badstuffdb.csv --corpus copycorpus.yml cake0.csv
#       --> Make the report in cake0.csv.txt with specific db and corpus
# or
#   python3 labrpt.py cake1.csv
#       --> Make the report in cake0.csv.txt with default db and corpus.
# or
#   python3 labrpt.py cakes/*.csv
#       --> Make the reports in cake/cake0.csv.txt, cake/cake1.csv.txt,
#           cake/cake2.csv.txt, etc with default db and corpus.
# Use the -v flag to see progress messages.

# Standard library.
import argparse
import csv
import os
import re
import sys

# Non-standard modules.
import yaml     # PyYAML: pip3 install --user pyyaml

verbose = False # Global usually only read by verb().
def verb(msg='', end='\n', sv_tm=False, rpt_tm=False): # {{{
    '''Print a message to STDOUT when verbose flag is set.
    Each line is prefixed with its number which is kept track with a static
    variable, so this should not be called from parallel code.
    Optionally save and/or report time since last call, which is useful for
    coarse profiling.
    '''
    import time

    tm_now = time.time()

    # Initialize static variables on first execution.
    static_vars = ["linenum", "newline", "tm_saved"]
    if False in [hasattr(verb, x) for x in static_vars]:
        verb.linenum = 1     # Strictly incrementing counter of printed lines.
        verb.newline = True  # FSM used for counting lines and printing numbers.
        verb.tm_saved = None # Storage for time state.

    if verbose:
        if verb.newline:
            outstr = "%d %s" % (verb.linenum, str(msg))
        else:
            outstr = str(msg)

        if rpt_tm:
            outstr += " [%s]" % tmdiff_s2wdhms_ascii(tm_now - verb.tm_saved)

        fd = sys.stdout

        print(outstr, end=end, file=fd)
        fd.flush()

        if end == '\n':
            verb.linenum += 1
            verb.newline = True
        else:
            verb.newline = False

    if sv_tm:
        verb.tm_saved = time.time()
# }}}

def notCommentLine(line: str) -> bool:
    return (not line.lstrip().startswith('#'))

def deduplicateSpaces(line: str) -> str:
    return re.sub(" +", ' ', line)

def processRow(state, rowNum, row): # {{{

    # TODO
    ret = state

    return ret # }}}

def stateToReport(state): # {{{

    # TODO
    ret = ""

    return ret # }}}

def getArgs(): # {{{

    parser = argparse.ArgumentParser(
        description = "labrpt Report Maker",
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("-v", "--verbose",
        default=False,
        action='store_true',
        help="Display progress messages.")

    parser.add_argument("-d", "--delimiter",
        type=str,
        default=',',
        help="String separating columns.")

    # NOTE: CSV format is possible but parsing is harder.
    parser.add_argument("--db",
        type=str,
        default="badstuffdb.yml", # TODO: Change to something proper.
        help="Database of chemical info. YAML format.")

    parser.add_argument("--corpus",
        type=str,
        default="copycorpus.yml", # TODO: Change to something proper.
        help="Copytext for each chemical. YAML format.")

    parser.add_argument("fnames",
        nargs='+',
        type=str,
        help="List of CSV files to generate reports for.")

    args = parser.parse_args()

    global verbose
    verbose = args.verbose

    return args # }}}

def main(args): # {{{

    # Read in entire chemical database into a dict (Map).
    # Access values like: db["carbaryl"]["colour"]
    # NOTE: This is easier in YAML format instead of CSV.
    verb("Reading database... ", end='')
    with open(args.db, 'r') as fd:
        db = yaml.safe_load(fd)
    verb("Done")

    # Read in entire copy corpus into a dict (Map).
    # Access values like: corpus["carbaryl"]
    verb("Reading corpus... ", end='')
    with open(args.corpus, 'r') as fd:
        corpus = yaml.safe_load(fd)
    verb("Done")

    verb("There are %d files to process" % len(args.fnames))
    for fnamei in args.fnames:
        fnameo = fnamei + ".txt"

        # Read in lab results CSV line by line.
        # Analyse and decide what pieces of copy text to use.
        verb("Reading CSV %s... " % fnamei, end='')
        with open(fnamei, 'r', newline='') as fd:

            fdUncomment = filter(notCommentLine, fd)
            fdClean = map(deduplicateSpaces, fdUncomment)
            reader = csv.reader(fdClean, delimiter=args.delimiter)

            state = {}
            for rowNum,row in enumerate(reader):
                state = processRow(state, rowNum, row)

        report = stateToReport(state)
        verb("Writing report... ", end='')
        with open(fnameo, 'w') as fd:
            fd.write(report)
        verb("Done")

    return 0 # }}}

if __name__ == "__main__":
    args = getArgs()
    sys.exit(main(args))

