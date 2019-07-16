#!/usr/bin/env python
# coding: utf-8

# In[1]:


# %load labrpt.py
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
    TDIsPulledfromDB = {(item["Pesticide Name"]).lower(): item['ADI'] for item in db}
    verb("Imported Database")
    for key,value in TDIsPulledfromDB.items(): ###convert any numerical ADIs into a float
        try:
            TDIsPulledfromDB[key]=float(value)
        except:
            pass #some have none numerical values so need to pass exceptions
    verb("Done")


    # Read in entire copy corpus into a dict (Map).
    # Access values like: corpus["carbaryl"]
    verb("Reading corpus... ", end='')
    with open(args.corpus, 'r') as fd:
        corpus = yaml.safe_load(fd)
    with open('copycorpus.yml', 'r') as fd:
    corpus = yaml.safe_load(fd)
    for item in corpus:
        item['']=(item['']).lower() #making all pesticide names lowercase
        item['Pesticide Name']=item.pop('') #For some reason when the yaml was imported the pesticdes were all given the key ''
    verb("Corpus read")


    verb("There are %d files to process" % len(args.fnames))
    for fnamei in args.fnames:
        fnameo = fnamei + ".txt"
        

        # Read in lab results CSV line by line.
        # Analyse and decide what pieces of copy text to use.
        verb("Reading CSV %s... " % fnamei, end='')
        with open(fnamei, 'r', newline='') as fd:
            reader = csv.DictReader(fd)
            fdUncomment = filter(notCommentLine, fd)
            fdClean = map(deduplicateSpaces, fdUncomment)
            reader = csv.reader(fdClean, delimiter=args.delimiter)
            labresults= {(rows['Parameter']).lower():float(rows['Result']) for rows in reader} #This should give us just the results. The name of the chemical and the amount detected

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


# In[141]:


with open('labdata0.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    AmountsDetectedfromlab = {rows['Parameter']:float(rows['Result']) for rows in reader}


# AmountsDetectedfromlab={
# "chemical1":0.085,
# "chemical2":0.1,
# "chemical3":0.02,
# "chemical4":0.1,
# } #pretend data. Really we want to pull these from the csv that the lab sent us

AmountsDetectedfromlab


# In[171]:





# In[145]:


####I only want to look in the database for items that were actually detected in the lab.
###So iterate through the key in AmountsDetectedfromlab which will give the chemical names
### and return a dictionary of chemical_name:TDI

TDIsNeeded = {key.split()[0]: (TDIsPulledfromDB[(key.split()[0])]) for key in AmountsDetectedfromlab.keys()}

TDIsNeeded


# In[153]:


###TII (mg per individual)=Tolerable Daily Intake (mg/kg b.w.)*Body weight(kg b.w)###
# Define body weight
bw=75

###Define function to calculate the tolerable intake per person for each chemical
### multiply the TDI by the bodyweight
def calcTII(TDI,bw):
    TII=TDI*bw
    return TII

TIIS={key:calcTII(TDIsPulledfromDB[key.split()[0]],bw) for key in AmountsDetectedfromlab.keys()}

TIIS


# In[162]:


###TCL (mg/kg(food)) =TII/Amount of food consumed(kg)=TII/AE###

def calcTCL(TII,AE):
    TCL=TII/AE
    return TCL

AE=0.25 #this is the amount eaten in kg. Want this input on command line

TCLresultsDict={key:calcTCL(value,AE) for key,value in TIIS.items()} #This should apply the calcTCL func to every TII value, dividing each by 0.25
TCLresultsDict


# In[155]:



##Define a function to claculate the Concern Index for any chemical
def calcCIChem(AD,TCL):
    FCIc=AD/TCL #this still needs to be *100 but I think it's best to do that later
    return FCIc

#Calculate the Concern index for each chemical (Amount detected/TCL)
##Create the CI results dict
ChemicalCIresultDic={key:(calcCIChem(AmountsDetectedfromlab[key],value)) for key,value in TCLresultsDict.items()}

ChemicalCIresultDic


# In[156]:


#find the chemical with the max value
highestCI=max(ChemicalCIresultDic, key=ChemicalCIresultDic.get)
highestCI


# In[157]:


keylst=list(ChemicalCIresultDic.keys())
keylst.remove(highestCI)
keylst


# In[21]:


# ##Geomean approach
# ###copied this method from here: https://bytes.com/topic/python/answers/727876-geometrical-mean



# def geomean(numbers):
#     product = 1
#     for n in numbers:
#         product *= n
#     return product ** (1.0/len(numbers))

# FCIoverall=geomean(FCIresultDict.values())
# FCIoverall


# In[181]:


###Calculate the Overall-FCI for all except the highest
###~~~FCI=AD1TCL1*100+AD2TCL22*100+AD3TCL32*100...ADnTCLn2*100

def calcCI_low(CI):
    return ((CI**2))*100

### run CalcOverallFCI on all except the highest
totalFCI=0
for chem in keylst:
    totalFCI+=(calcCI_low(ChemicalCIresultDic[chem]))


def calcCI_highest(CI):
    return(CI*100)

totalFCI=int(+(calcCI_highest(ChemicalCIresultDic[highestCI])))
print("Overall Food Concern Index =",totalFCI)


# In[ ]:


#
