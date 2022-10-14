from hashlib import sha256
import time
import json
mp = {}
class Transaction:
    def __init__(self, buyer_name,seller_name,prop_name,amount,timestamp):
        self.buyer_name=buyer_name
        self.seller_name=seller_name
        self.prop_name=prop_name
        self.amount=amount
        self.timestamp=timestamp
        
    def getTransactionData(self): 
        return self.buyer_name +" "+ self.seller_name +" "+self.prop_name +" "+ str(self.amount) +" "+str(self.timestamp)
class Block:
    def __init__ (self,prev_hash,merkleRootHash,timestamp,nonce=0):
        self.nonce=nonce
        self.prev_hash=prev_hash
        self.merkleRootHash=merkleRootHash
        self.timestamp=timestamp
        
    def computeHash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
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
class Blockchain:    
    def __init__(self):
        self.chain_array=[]
    def create_genesis(self):
        genesis_block=Block("-1","0",time.time())
        genesis_block.hash=Block.computeHash(genesis_block)
        self.chain_array.append(genesis_block)   
    @property  
    def last_block(self):
        return self.chain_array[-1]
    def add_block(self,Block,proof):
        prev_hash=self.last_block.hash 
        if(prev_hash != Block.prev_hash): 
            return False
        if not Blockchain.is_valid_proof(Block,proof):  
            return False
        Block.hash=proof
        self.chain_array.append(Block)
        return True     
def CalculateMerkleRoot(hashes_List_Of_Transactions):
    tempList=hashes_List_Of_Transactions
    while len(tempList)>1:
        tmp=[]
        if(len(tempList)%2!=0):            #if odd size then duplicate last elem
            tempList.append(tempList[-1])
        for i in range(0, len(tempList), 2):
            hashPair=tempList[i]+tempList[i+1]       #A+B
            tmp.append(sha256(hashPair.encode()).hexdigest())
        tempList=tmp
    return tempList[0]
class person:
    def __init__(self,name,property):


