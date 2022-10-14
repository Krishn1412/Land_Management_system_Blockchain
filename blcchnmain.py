from hashlib import sha256
import collections
import time
import json
mp = {}
class Transaction:
    def __init__(self, buyer_name,seller_name,prop_obj,amount,timestamp):
        self.buyer_name=buyer_name
        self.seller_name=seller_name
        self.prop_obj=prop_obj
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
    def __init__(self,currentOwner,id,PropertyName,PreviousTransacs):
        self.currentOwner=currentOwner
        self.id=id
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
    def add_block(self,Block):
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
def winner(self):
    st=[]
    li = [5,7,9,1,3,4,6,7,8,4]
    for i in range(10):
        r=input()
        t=((r*li[i])/100)
        st.append([li[i],t])
    st.sort(key = lambda x: x[1])
    return st[0][0]
class person:
    def __init__(self,id,name,prop):
        self.id=id
        self.name=name
        self.prop=prop
    
def validate_transaction(transaction):
    winn=winner()
    t=transaction.prop_obj
    r=t.currentOwner
    if r!=transaction.seller_name:
        return False
    else:
        return True
def validate_chain(self,chain_array):
    _prevBlock = ''
    for block in chain_array:
        if self.is_block_valid(block, prevBlock=_prevBlock):
            _prevBlock = block
        else:
            return False
        return True  
def validate_block(transaction,chain_array):
    if validate_transaction(transaction) and validate_chain(chain_array):
        return True
    return False

def main():
    no_of_owners=input("Enter the number of owners: ")
    arr_of_people=[]
    arr_of_prop=[]
    for i in range(no_of_owners):
        list_of_prop=[]
        id=input("Enter ID of person: ")
        name=input("Enter name of person: ")
        num_of_prop=input("Enter number of property: ")
        for j in range(num_of_prop):
            a=input("Enter property ID: ")
            list_of_prop.append(a)
        per =person(id,name,list_of_prop)
        arr_of_people.append(per)
    no_of_property=input("Enter number of property: ")
    for i in range(no_of_property):
        list_of_prevtrans=[]
        id=input("Enter ID of property: ")
        name=input("Enter property name: ")
        curr_owner=input("Enter the name of curr owner: ")
        prop=property(curr_owner,id,name,list_of_prevtrans)
        arr_of_prop.append(prop)
    





