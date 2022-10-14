import hashlib,binascii,base64,json,requests,random,datetime
from hashlib import sha256
class Transaction:
    def __init__(self,buyer_name,seller_name, property_name, amount, Timestamp_of_the_transaction):
        self.buyer_name=buyer_name
        self.seller_name=seller_name
        self.property_name=property_name
        self.amount=amount
        self.Timestamp_of_the_transaction=Timestamp_of_the_transaction
class Block:
    def __init__ (self,prev_hash,merkleRootHash,timestamp,nonce=0):
        self.nonce=nonce
        self.prev_hash=prev_hash
        self.merkleRootHash=merkleRootHash
        self.timestamp=timestamp
        
    def computeHash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()class Transaction:
    def __init__(self, buyer_name,seller_name,prop_name,amount,timestamp):
        self.buyer_name=buyer_name
        self.seller_name=seller_name
        self.prop_name=prop_name
        self.amount=amount
        self.timestamp=timestamp
        
    def getTransactionData(self): 
        return self.buyer_name +" "+ self.seller_name +" "+self.prop_name +" "+ str(self.amount) +" "+str(self.timestamp)
class Property:
    def __init__(self,currentOwner,previousOwners,PropertyName,PreviousTransacs):
        self.currentOwner=currentOwner
        self.previousOwners=previousOwners
        self.PropertyName=PropertyName
        self.PreviousTransacs=PreviousTransacs
    def updateOwner(self,NewOwner,Transac):
        self.previousOwners.append(self.currentOwner)
        self.currentOwner=NewOwner
        self.PreviousTransacs.append(Transac)
