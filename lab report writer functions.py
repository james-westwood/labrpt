#!/usr/bin/env python
# coding: utf-8

# In[3]:


###TII (mg per individual)=Tolerable Daily Intake (mg/kg b.w.)*Body weight(kg b.w)###

def calcTII(TDI,bw):
    TII=TDI*bw
    return TII

bw=75

TDIsPulledfromDB={
"chemical1":0.1,
"chemical2":0.2,
"chemical3":0.3,
"chemical4":1.5,
}


TIIs={key:(calcTII(value,bw)) for key,value in TDIsPulledfromDB.items()}
TIIs


# In[6]:


###TCL (mg/kg(food)) =TII/Amount of food consumed(kg)=TII/AE###

def calcTCL(TII,AE):
    TCL=TII/AE
    return TCL

AE=0.25 #this is the amount eaten in kg. Making it a variable as we might want to redefine it elsewhere

TCLresultsDict={key:calcTCL(value,AE) for key,value in TIIs.items()} #This should apply the calcTCL func to every TII value, dividing each by 0.25

TCLresultsDict


# In[13]:


def calcFCIChem(AD,TCL):
    FCIc=AD*TCL #this still needs to be *100 but I think it's best to do that later
    return FCIc

AmountsDetectedfromlab={
"chemical1":0.085,
"chemical2":0.1,
"chemical3":0.02,
"chemical4":0.1,
} #pretend data. Really we want to pull these from the csv that the lab sent us

##Create the FCI results dict
FCIresultDict={key:(calcFCIChem(AmountsDetectedfromlab[key],value)) for key,value in TCLresultsDict.items()}    

FCIresultDict.values()


# In[17]:


##Geomean approach
###copied this method from here: https://bytes.com/topic/python/answers/727876-geometrical-mean



def geomean(numbers):
    product = 1
    for n in numbers:
        product *= n
    return product ** (1.0/len(numbers))

FCIoverall=geomean(FCIresultDict.values())
FCIoverall


# In[ ]:


# from operator import itemgetter
# highestFCIchem=(max(FCIresultDict.items(), key=itemgetter(1))) #finding the key with the highest value (this returns a tuple)
# sqrdFCIs=([value**2 for key,value in calcVars if key != highestFCIchem[0]]) #squaring all but the highest FCI
    
overallFCI = (sum(n*100) for n in sqrdFCIs)+highestFCIchem[1]

def calcFCIoverall(calcVars:dict): #I wanted to specify that the datatype should be a dictionary here
    ## some way of identifying the highest FCI (FCI1), as that is treated differently.
    ## some way of taking all other FCIs except the highest, squaring them, multiplying by 100 and adding them
    ## add FCI1

