
#Bank Keys
bankKeyN = 571
bankKeyD = 59 
bankKeyE = 29

import sys
import os
import random
import hashlib
import pickle
from utils import *

class Customer:
    def __init__(self, id, config_path= "config.json"):
        self.identity = id
        self.config = load_config(config_path)
        self.BASE_DIR = os.getcwd()

    def reveal_id_strings(self,nbit,monum):

        money_order = []
        fileName = "BitCommitNums{}.txt".format(str(monum))
        save_path = os.path.join(self.BASE_DIR, fileName)

        with open(save_path) as inputfile:
            for line in inputfile:
                money_order.append(line.strip())
        
        first_row = money_order[0]
        fourth_row_pair = money_order[3]
        I11R = first_row[1]
        
        I12S = fourth_row_pair[3]
        I12S = fourth_row_pair[1]
        
        returnMO = []
        if nbit == 0: 
            I11R

        elif nbit == 1: 
            I12S


    def unblind_signed_mo(self, money_order):
        values_dict = {"value_of_mo":  money_order[0],
                       "uniqueness" : money_order[1],
                       "I11R" :  int(money_order[2]), 
                        "I11S" : int(money_order[3]),
                        "I12R": int(money_order[4]),
                        "I12S": int(money_order[5]), 
                        "I21R": int(money_order[6]),
                        "I21S" : int(money_order[7]),
                        "I22R" : int(money_order[8]),
                        "I22S" : int(money_order[9])
                    }
        return_mo = []
        #Value of Money Order
        for _,v in values_dict.items():
            return_mo.append(int(v)**bankKeyD%bankKeyN)
       
        return return_mo    
                       
    
    def create_money_order(self, value_Of_morder, id): 
        id_list = []
        with open (self.config["custIDs"], 'rb') as f:
            try:
                id_list = pickle.load(f)
            except EOFError:
                id_list = []
                print("error pickle reading")
        uniqueness_string = randomInt(100,500)
        while True:
            if uniqueness_string in id_list: 
                uniqueness_string = randomInt(100,500)
            else: 
                id_list.append(uniqueness_string)
                break
            
        with open(self.config["custIDs"], 'wb') as f:
            pickle.dump(id_list, f)

        customerID = self.identity
        base_morder = []
        base_morder.append(value_Of_morder)
        base_morder.append(value_Of_morder)
        base_morder.append(self.identity)
        fileName = "BaseMO{}.txt".format(str(id+1))
        save_path = os.path.join(self.BASE_DIR, fileName)

        writeFile(save_path,base_morder)

        secret_split_mo = []
        secret_split_mo.append(value_Of_morder)
        secret_split_mo.append(value_Of_morder)
        I11 = getSecretSplitting(self)  
        I12 = getSecretSplitting(self) 
        I21 = getSecretSplitting(self)
        I22 = getSecretSplitting(self)
        secretSplit = []
        I11L = I11[0]
        I11R = I12[0]
        I12L = I21[0]
        I12R = I22[0]
        secretSplit.append([I11L,I11R])
        secretSplit.append([I12L,I12R])
        secret_split_mo.append(secretSplit)
        secret_split_mofilename = "SecretSplitMO{}.txt".format(str(id+1)) 
        writeFile(secret_split_mofilename,secret_split_mo)
        secret_split_num_mofilename = "PRNG_SS.txt".format(str(id+1))
        writeFile(secret_split_num_mofilename,secretSplit)

        BC_raw_output =perform_bit_commitment(I11,I12,I21,I22)
        BC_out = BC_raw_output[0]
        BC_rand = BC_raw_output[1]
        R111 = BC_rand[0]
        R112 = BC_rand[1]
        R121 = BC_rand[2]
        R122 = BC_rand[3]
        S111 = BC_rand[4]
        S112 = BC_rand[5]
        S121 = BC_rand[6]
        S122 = BC_rand[7]
        R211 = BC_rand[8]
        R212 = BC_rand[9]
        R221 = BC_rand[10]
        R222 = BC_rand[11]
        S211 = BC_rand[12]
        S212 = BC_rand[13]
        S221 = BC_rand[14]
        S222 = BC_rand[15]
        rand_int_BCfilename = "PRNG_BC{}.txt".format(str(id+1))
        writeFile(rand_int_BCfilename,BC_rand)

        bit_comming_numsfilename = "BitCommitNums{}.txt".format(str(id+1))
        R11 = I11[0]
        S11 = I11[1]
        R12 = I12[0]
        S12 = I12[1]
        I11R = BC_out[0]
        I11S = BC_out[1]
        I12R = BC_out[2]
        I12S = BC_out[3]
        BCNUMS = []
        BCNUMS.append([R11,I11R])
        BCNUMS.append([S11,I11S])
        BCNUMS.append([R12,I12R])
        BCNUMS.append([S12,I12S])
        writeFile(bit_comming_numsfilename,BCNUMS)   

        R21 = I21[0]
        S21 = I21[1]
        R22 = I22[0]
        S22 = I22[1]
        bitCommitFileName = "BitCommitMO{}.txt".format(str(id+1))
        BitCommitMO = []
        BitCommitMO.append(value_Of_morder)
        BitCommitMO.append(uniqueness_string)
        BitCommitMO.append(R21)
        BitCommitMO.append(S21)
        BitCommitMO.append(R22)
        BitCommitMO.append(S22)
        BitCommitMO.append(R11)
        BitCommitMO.append(S11)
        BitCommitMO.append(R12)
        BitCommitMO.append(S12)
        writeFile(bitCommitFileName,BitCommitMO)

        blindedMO = blindMO(BitCommitMO)
        blindedMOFileName = "BlindedMO{}.txt".format(str(id+1))
        unblindedMO = unblindMO(blindedMO)
        blindedMOFileName = "UnblindedMO{}.txt".format(str(id+1))
        writeFile(blindedMOFileName,unblindedMO)

        revealedMO = reveal_mo(unblindedMO,R11,R111,R112,S11,S111,S112,R12,R121,R122,S12,S121,S122,I11R,I12R,I11S,I12S,value_Of_morder,uniqueness_string)
        #BitCommitRevealMOn.txt
        revealMOFileName = "BitCommitRevealMO" + str(id+1) + ".txt"
        writeFile(revealMOFileName,revealedMO)

        joinedMO = join_mo(reveal_mo,R11,S11,value_Of_morder,uniqueness_string)
        joinedFileName = "SecretJoinMO{}.txt".format(str(id+1))
        writeFile(joinedFileName,joinedMO)



