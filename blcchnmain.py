from hashlib import sha256
import collections
import time
import json
mpp = {}
mph = {}
class Transaction:
    def __init__(self, buyer_name,seller_name,prop_obj,amount):
        self.buyer_name=buyer_name
        self.seller_name=seller_name
        self.prop_obj=prop_obj
        self.amount=amount
        
    def getTransactionData(self): 
        return self.buyer_name +" "+ self.seller_name +" "+self.prop_name +" "+ str(self.amount)
class Block:
    def __init__ (self,prev_hash,merkleRootHash,timestamp):
        self.prev_hash=prev_hash
        self.merkleRootHash=merkleRootHash
        self.timestamp=timestamp
        
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
class validator(person):
    def validate_transaction(self,transaction):
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
    BC=Blockchain()
    no_of_owners=int(input("Enter the number of owners: "))
    arr_of_people=[]
    arr_of_prop=[]
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
    no_of_property=int(input("Enter number of property: "))
    for i in range(no_of_property):
        list_of_prevtrans=[]
        id=int(input("Enter ID of property: "))
        name=input("Enter property name: ")
        curr_owner=int(input("Enter the id of curr owner: "))
        size=int(input("Enter size of property: "))
        prop=Property(mpp[curr_owner],id,name,list_of_prevtrans,size)
        mpp[id]=prop
        arr_of_prop.append(prop)
    print("To begin with transactions we first implement the proof of stake algorithm")
    winner_of_round=winner(arr_of_people)
    leader_of_chain=validator(winner_of_round.id,winner_of_round.name,winner_of_round.prop,winner_of_round.total)
    print(leader_of_chain.name)
    trans=int(input("Enter the number of transactions: "))
    arr_of_trans=[]
    while trans>0:
        Buyer=input("Enter the buyer's name: ")
        seller=input("Enter seller's name: ")
        id_prop=int(input("Enter property id: "))
        amount=int(input("Enter the amount"))
        trans=Transaction(Buyer,seller,mpp[id_prop],amount)
        Trans_valid=leader_of_chain.validate_transaction(trans)
        if Trans_valid==False:
            print("Transaction is invalid, so the process has been terminated")
            break
        arr_of_trans.append(trans)
        trans-=1
    
    merkle_root=CalculateMerkleRoot(arr_of_trans)
    last_blc=BC.last_block()
    chain_true=leader_of_chain.validate_chain(BC.chain_array)
    if chain_true:
        for i in range(len(arr_of_trans)):
            Property.updateOwner(arr_of_trans[i].buyer_name,arr_of_trans[i])
        newBlock=Block(last_blc.hash,merkle_root,time.time())
        BC.chain_array.append(newBlock)
        block_true=leader_of_chain.validate_chain(BC.chain_array)
    

    # run=True
    # while run:
    #     print("Enter 1 for : Add new Transactions \nEnter -1 to exit \nEnter 2 to add new property\nEnter 3 to check Transaction History of a Property\nEnter 4 to check block structure")
    #     val=int(input())
    #     if val == -1:
    #         run=False
    #     elif val == 1:
    #         print("To begin with transactions we first implement the proof of stake algorithm")
    #         winner_of_round=winner(arr_of_people)
    #         print("Enter number of Transactions occured")
    #         val2=int(input())
    #         transacs=[]
    #         for i in range(val2):
    #             print("Enter details of transaction :",i+1,"\n")
    #             obj=take_Transac_Input()
    #             if checkTransactionValidity(obj)==True:
    #                 transacs.append(obj)
    #                 print("Transaction Valid.\n")
    #             else:
    #                 print("\nTransaction: ",i+1," is Invalid, Hence Rejected and Not Added into Blockchain\n")
    #         if transacs:
    #             LMS.mine(transacs)
    #     elif val == 2:
    #         print("\nPlease Enter the following in order: 1.Property Name 2.Owner Name\n")
    #         prop_name=input()
    #         owner=input()
    #         prop_obj=Property(currentOwner=owner,
    #                           previousOwners=[],
    #                           PropertyName=prop_name,
    #                           PreviousTransacs=[])
    #         mp[prop_name]=prop_obj          #map new property name to its newly crated object
    #         print("Property Registered Sucessfully! \n")
    #     elif val == 3:
    #         print("Please Enter the Property Name whose previous transactions you want to view:")
    #         prop_name=input()
    #         if mp.get(prop_name) is None:
    #             print("\nProperty named does NOT exist.\n")
    #         elif len(mp[prop_name].PreviousTransacs)==0:
    #             print("No transactions have occured for this given property")
    #         else:
    #             for transac in mp[prop_name].PreviousTransacs:
    #                 print(transac)
    #     elif val == 4:
    #         for block in LMS.chain_array:
    #             print("previous hash is ",block.prev_hash," current block hash is ",block.hash," merke root is ",block.merkleRootHash,"\n")

    
if __name__=="__main__":
    main()





