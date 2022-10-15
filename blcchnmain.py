from hashlib import sha256
import collections
import time
import json
mpp = {}
mph = {}
class Transaction:
    def __init__(self, buyer,seller,prop_obj,amount):
        self.buyer=buyer
        self.seller=seller
        self.prop_obj=prop_obj
        self.amount=amount
        
    def getTransactionData(self): 
        return self.buyer.name +" "+ self.seller.name +" "+self.prop_obj.PropertyName +" "+ str(self.amount)
class Block:
    def __init__ (self,prev_hash,merkleRootHash,timestamp,hash):
        self.prev_hash=prev_hash
        self.merkleRootHash=merkleRootHash
        self.timestamp=timestamp
        self.hash=hash
        
    def computeHash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
class Property:
    def __init__(self,currentOwner,id,PropertyName,PreviousTransacs,sizep):
        self.currentOwner=currentOwner
        self.id=id
        self.PropertyName=PropertyName
        self.PreviousTransacs=PreviousTransacs
        self.sizep=sizep
    def updateOwner(self,NewOwner,Transac):
        self.currentOwner=NewOwner
        self.PreviousTransacs.append(Transac)
class Blockchain:    
    def __init__(self):
        self.chain_array=[]
    def create_genesis(self):
        to_hash1=str("0")+str("-1")+str(time.time())
        hashblock= sha256(to_hash1.encode()).hexdigest()
        genesis_block=Block("-1","0",time.time(),hashblock)
        genesis_block.hash=Block.computeHash(genesis_block)
        self.chain_array.append(genesis_block)   
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
def winner(list_of_per):
    st=[]
    n=len(list_of_per)
    for i in range(n):
        r=int(input("Enter the stake you want to put in: "))
        t=((r*list_of_per[i].total)/100)
        st.append([list_of_per[i],t])
    st.sort(key = lambda x: x[1])
    return st[n-1][0]
class person:
    def __init__(self,id,name,prop,total):
        self.id=id
        self.name=name
        self.prop=prop
        self.total=total
    
    def AddTotal(self,NewProp):
        self.prop.append(NewProp)
        self.total+=NewProp.sizep
    
    def SubTotal(self,NewProp):
        self.total-=NewProp.sizep
        
class validator(person):
    def validate_transaction(self,transaction):
        t=transaction.prop_obj
        r=t.currentOwner.name
        if r!=transaction.seller.name:
            return False
        else:
            return True
    def validate_chain(self,chain_array):
        _prevBlock = "-1"
        for block in chain_array:
            if block.prev_hash==_prevBlock:
                _prevBlock = block.hash
            else:
                return False
            return True  
    def validate_block(transaction,chain_array):
        if validate_transaction(transaction) and validate_chain(chain_array):
            return True
        return False


def owner_adding(arr_of_people,no_of_owners):
    for i in range(no_of_owners):
        list_of_prop=[]
        id=int(input("Enter ID of person: "))
        name=input("Enter name of person: ")
        num_of_prop=int(input("Enter number of property user has: "))
        total=0
        for j in range(num_of_prop):
            a=int(input("Enter property ID: "))
            total+=int(input("Enter property size: "))
            list_of_prop.append(a)
        per =person(id,name,list_of_prop,total)
        mph[id]=per
        arr_of_people.append(per)
def prop_adding(arr_of_prop,no_of_property):
    
    for i in range(no_of_property):
        list_of_prevtrans=[]
        id=int(input("Enter ID of property: "))
        name=input("Enter property name: ")
        curr_owner=int(input("Enter the id of curr owner: "))
        size=int(input("Enter size of property: "))
        prop=Property(mph[curr_owner],id,name,list_of_prevtrans,size)
        mpp[id]=prop
        arr_of_prop.append(prop)
        
def trans_adding(arr_of_trans,trans,arr_of_people,BC):
    
    print("To begin with transactions we first implement the proof of stake algorithm")
    winner_of_round=winner(arr_of_people)
    leader_of_chain=validator(winner_of_round.id,winner_of_round.name,winner_of_round.prop,winner_of_round.total)
    print(leader_of_chain.name)
    f=0
    while trans:
        Buyer=int(input("Enter the buyer's id: "))
        seller=int(input("Enter seller's id: "))
        id_prop=int(input("Enter property id: "))
        amount=int(input("Enter the amount: "))
        transac=Transaction(mph[Buyer],mph[seller],mpp[id_prop],amount)
        Trans_valid=leader_of_chain.validate_transaction(transac)
        if Trans_valid==False:
            f=1
            print("Transaction is invalid, so the process has been terminated")
            break
        arr_of_trans.append(transac)
        trans-=1 
    last_blc=BC.last_block()
    chain_true=leader_of_chain.validate_chain(BC.chain_array)
    print(chain_true)
    if f==0:
        if chain_true:
            hash_of_trans=[]
            for transac in arr_of_trans:
                to_hash=transac.getTransactionData()
                hash_of_trans.append(sha256(to_hash.encode()).hexdigest())
                mpp[transac.prop_obj.id].updateOwner(transac.buyer,transac)
                transac.buyer.AddTotal(transac.prop_obj)
                transac.seller.SubTotal(transac.prop_obj)
                print(transac.prop_obj.id)
                
            merkle_root=CalculateMerkleRoot(hash_of_trans) 
            to_hash1=str(merkle_root)+str(last_blc.hash)+str(time.time())
            hashblock= sha256(to_hash1.encode()).hexdigest()
            newBlock=Block(last_blc.hash,merkle_root,time.time(),hashblock)
            BC.chain_array.append(newBlock)


def main():
    BC=Blockchain()
    BC.create_genesis()
    arr_of_people=[]
    arr_of_prop=[]
    arr_of_trans=[]
    
    no_of_owners=int(input("Enter the number of owners: "))
    owner_adding(arr_of_people,no_of_owners)
    
    no_of_property=int(input("Enter number of property: "))
    prop_adding(arr_of_prop,no_of_property) 

   
    run=True
    while run:
        print("Enter 1 for : Add new Transactions \nEnter -1 to exit \nEnter 2 to add new person for transaction\nEnter 3 to check Transaction History of a Property\nEnter 4 to check block structure")
        val=int(input())
        if val == -1:
            run=False
        elif val == 1:
            trans=int(input("Enter the number of transactions: "))
            trans_adding(arr_of_trans,trans,arr_of_people,BC)  
        elif val == 2:
            no_of_owners=int(input("Enter the number of people to be added: "))
            owner_adding(arr_of_people,no_of_owners)        
            print("People Registered Sucessfully! \n")
        elif val == 3:
            prop_id=int(input("Please Enter the Property ID whose previous transactions you want to view: "))
            if mpp.get(prop_id) is None:
                print("\nProperty named does NOT exist.\n")
            elif len(mpp[prop_id].PreviousTransacs)==0:
                print("No transactions have occured for this given property")
            else:
                for transac in mpp[prop_id].PreviousTransacs:
                    print(transac.buyer.name+" bought this from "+transac.seller.name+" for "+str(transac.amount))
        elif val == 4:
            for block in BC.chain_array:
                print("previous hash is ",block.prev_hash," current block hash is ",block.hash," merke root is ",block.merkleRootHash,"\n")
    
    
    
    
if __name__=="__main__":
    main()





