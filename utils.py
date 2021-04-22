import os
import json
import random

def validate_file_path(path):
    status = os.path.isfile(path)
    return status

def load_config(path):
    status = validate_file_path(path)
    config = None
    if status:
        with open(path) as f:
            config = json.load(f)
    else:
        raise Exception("No configration found")
    return config
    
    
def join_mo(MO,R11,S11,valueOfMoneyOrder,uniquenessString):
   Identity = R11^S11 
   returnMO = []
   returnMO.append(valueOfMoneyOrder)
   returnMO.append(uniquenessString)
   returnMO.append(Identity)
   return returnMO


def reveal_mo(MO,R11,R111,R112,S11,S111,S112,R12,R121,R122,S12,S121,S122,I11R,I12R,I11S,I12S,valueOfMoneyOrder,uniquenessString):
    VAR1 = [(I11R[0]^R111^R112),(I11S[0]^S111^S112)]
    VAR3 = [(I12R[0]^R121^R122),(I12S[0]^S121^S122)]
    returnList = []
    returnList.append(valueOfMoneyOrder)
    returnList.append(uniquenessString)
    returnList.append(VAR1)
    returnList.append(VAR3)
    return returnList


def unblindMO(mo):
    config = load_config("config.json")
    bankKeyN= config["bankKeyN"]
    bankKeyD = config["bankKeyD"]
    unblinded_mo = []
    for order in mo:
        unblinded_mo.append(int(order)**bankKeyD%bankKeyN)
    return unblinded_mo

def blindMO(money_order):
    config = load_config("config.json")
    bankKeyN= config["bankKeyN"]
    bankKeyE = config["bankKeyE"]

    blinded_mo = []
    for order in money_order:
        blinded_mo.append(int(order)**bankKeyE%bankKeyN)
    return blinded_mo

def perform_bit_commitment(I11,I12,I21,I22):
    R11 = I11[0]
    S11 = I11[1]
    R12 = I12[0]
    S12 = I12[1]
    R21 = I21[0]
    S21 = I21[1]
    R22 = I22[0]
    S22 = I22[1]
        
    R111 = randomNumberwithLength(len(str(R11)))
    R112 = randomNumberwithLength(len(str(R12)))
    R121 = randomNumberwithLength(len(str(R11)))
    R122 = randomNumberwithLength(len(str(R12)))
    S111 = randomNumberwithLength(len(str(S11)))
    S112 = randomNumberwithLength(len(str(S12)))
    S121 = randomNumberwithLength(len(str(S11)))
    S122 = randomNumberwithLength(len(str(S12)))
    R211 = randomNumberwithLength(len(str(R11)))
    R212 = randomNumberwithLength(len(str(R12)))
    S211 = randomNumberwithLength(len(str(R11)))
    S212 = randomNumberwithLength(len(str(R12)))
    R221 = randomNumberwithLength(len(str(S11)))
    R222 = randomNumberwithLength(len(str(S12)))
    S221 = randomNumberwithLength(len(str(S11)))
    S222 = randomNumberwithLength(len(str(S12)))

    I11R = [(R11^R111^R112),R111]
    I11S = [(S11^S111^S112),S111]
    I12R = [(R12^R121^R122),R121]
    I12S = [(S12^S121^S122),S121]

    I21R = [(R21^R211^R212),R211]
    I21S = [(S21^S211^S212),S211]
    I22R = [(R22^R221^R222),R221]
    I22S = [(S22^S221^S222),S221]

    outputValue = []
    outputValue.append(I11R)
    outputValue.append(I11S)
    outputValue.append(I12R)
    outputValue.append(I12S)
    outputValue.append(I21R)
    outputValue.append(I21S)
    outputValue.append(I22R)
    outputValue.append(I22S)

    outputValue2 = []
    outputValue2.append(R111)
    outputValue2.append(R112)
    outputValue2.append(R121)
    outputValue2.append(R122)
    outputValue2.append(S111)
    outputValue2.append(S112)
    outputValue2.append(S121)
    outputValue2.append(S122)
    outputValue2.append(R211)
    outputValue2.append(R212)
    outputValue2.append(R221)
    outputValue2.append(R222)
    outputValue2.append(S211)
    outputValue2.append(S212)
    outputValue2.append(S221)
    outputValue2.append(S222)

    returnValue = []
    returnValue.append(outputValue)
    returnValue.append(outputValue2)

    return returnValue

def getSecretSplitting(obj):
    R = randomNumberwithLength(len(str(obj.identity)))
    S = R ^ obj.identity
    returnList = [R,S]
    return(returnList)

def randomNumberwithLength(length):
    lower = 10**(length-1)
    upper = 10**length - 1
    return random.randint(lower, upper)
        
def writeFile(fileName,outputList):
    with open(fileName, "w") as f:
        for value in outputList:
            f.write(str(value)+ '\n')

def randomInt(min,max):
    randomNumber = random.randint(min,max)
    return int(randomNumber)
