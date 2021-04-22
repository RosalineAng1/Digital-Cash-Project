import random 
from utils import load_config

config = load_config("config.json")
bankKeyN= config["bankKeyN"]
bankKeyD = config["bankKeyD"]
bankKeyE = config["bankKeyE"]

class Merchant:
    def __init__(self):
        pass
        
    def generate_nbit(self):
        value = random.randint(0,1)
        return value

    def unblind_signed_morder(self, mo):
        unblinded_mo = []
        for order in mo:
            unblinded_mo.append(int(order)** bankKeyD % bankKeyN)
        return unblinded_mo