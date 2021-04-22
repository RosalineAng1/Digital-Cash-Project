
from Customer import Customer
from Bank import Bank
from Merchant import Merchant
import random
from utils import writeFile

identity = int(input("Please enter your ID: "))
# writeFile("custusedIDs.txt", [identity])
num_of_morders = int(input("How many money orders would you like to make today?: "))
value_of_money_order = []

Alice = Customer(id=identity)
Bob = Bank()
Merchant = Merchant() 

for i in range(num_of_morders):
    inputVal = int(input("What is the value of the Money Order " + str((i+1)) + "?: "))
    value_of_money_order.append(inputVal)

for i in range(num_of_morders):
    Alice.create_money_order(value_Of_morder=value_of_money_order[i],id=i)

random_morder = random.randint(1,num_of_morders)

signedMO = Bob.blindSignatureProtocol(random_morder)
signedMOFileName = "SignedBlindedMO{}.txt".format(str(random_morder)) 
writeFile(signedMOFileName,signedMO)

unblindSignedMOFileName = "SignedUnblindedMO{}.txt".format(str(random_morder)) 
unblindSignedMO = Alice.unblind_signed_mo(signedMO)
writeFile(unblindSignedMOFileName,unblindSignedMO)

merchantUnblindFileName = "MerchantUnblind{}.txt".format(str(random_morder)) 
merchantUnblindMO = Merchant.unblind_signed_morder(signedMO)
writeFile(merchantUnblindFileName,merchantUnblindMO)
if merchantUnblindMO == unblindSignedMO:
    print("Success! The signature is valid.")
else: 
    print("Failure! The signature is NOT valid.")

print(Bob.validateUID(unblindSignedMO[1]))

nbitval = Merchant.generate_nbit()
Alice.reveal_id_strings(nbit=nbitval,monum=random_morder)