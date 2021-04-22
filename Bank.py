import random
import pickle
import os
from utils import load_config, validate_file_path
config = load_config("config.json")
bankKeyN= config["bankKeyN"]
bankKeyD = config["bankKeyD"]
bankKeyE = config["bankKeyE"]

class Bank:
    def __init__(self, config_path= "config.json"):
        self.config = load_config(config_path)
        self.BASE_DIR = os.getcwd()
    
    def validateUID(self, UID):
        return_msg  = None
        bankfile_status = validate_file_path(self.config["bankIDs"]) 
        with open (self.config["bankIDs"], 'rb') as f:
            ids_list = pickle.load(f)
            if UID in ids_list: 
                return_msg =  "Error! This ID has been used before."
            else: 
                return_msg = "Success!  This is a new ID."
                                                           
        with open(self.config["bankIDs"], 'wb') as f:
            pickle.dump(ids_list, f)
        return return_msg

    def blindSignatureProtocol(self, orderNumber):
        money_order = []
        fileName = "UnblindedMO{}.txt".format(str(orderNumber))
        save_path = os.path.join(self.BASE_DIR, fileName)
        with open(save_path, "r+") as inputfile:
            for line in inputfile:
                money_order.append(line.strip())
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