from hashlib import sha256
import time
import json
mp = {}
class Block:
    def __init__ (self,prev_hash,merkleRootHash,timestamp,nonce=0):
        self.nonce=nonce
        self.prev_hash=prev_hash
        self.merkleRootHash=merkleRootHash
        self.timestamp=timestamp
        
    def computeHash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    
class Transaction:
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
class Blockchain:
    
    difficulty=2   #difficulty of our PoW algo
    
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
        prev_hash=self.last_block.hash   # hash of previous block
        
        if(prev_hash != Block.prev_hash):   #last block ka hash is not equal to previous hash of this current block 
            return False
        
        if not Blockchain.is_valid_proof(Block,proof):  #check validity of proof hash
            return False
        
        Block.hash=proof
        self.chain_array.append(Block)
        return True
    
    @staticmethod
    def proof_of_work(block):
        block.nonce=0
        
        computed_hash=block.computeHash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1                       #change nonce until hash of new block meets requirements
            computed_hash = block.computeHash()

        return computed_hash

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and  #if starts woth x zeros
                block_hash == block.computeHash())    #if hash is equal to computed hash of data+nonce
        
    @classmethod
    def check_chain_validity(cls, chain_array):
        result = True
        previous_hash = "0"

        for block in chain_array:
            block_hash = block.hash
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block_hash) or previous_hash != block.prev_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result
    def mine(self,transacs):    # sourcery skip: use-fstring-for-concatenation
        hashes_List_Of_Transactions=[]
        for transac in transacs:
            to_hash=transac.getTransactionData()
            hashes_List_Of_Transactions.append(sha256(to_hash.encode()).hexdigest())     #add hash of all transaction into a list
            mp[transac.prop_name].updateOwner(transac.buyer_name,to_hash)                #update property ownerships

        #now we find merkle root
        merkleRoot=CalculateMerkleRoot(hashes_List_Of_Transactions)
        
        last_block = self.last_block
        new_block = Block(prev_hash=last_block.hash,
                          merkleRootHash=merkleRoot,
                          timestamp=time.time())

        proof = self.proof_of_work(new_block)   #get proof by solving the puzzle
        self.add_block(new_block, proof)        # send proof to add the new block
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

#take input as : enter number of transactions, then store all transactions into an object and out into uncifmrned transacs array.
def take_Transac_Input(): 
    print("Please Enter the following in order: 1.Buyer Name 2.Seller Name 3.Property Name 4.Amount\n")
    buyer=input()
    seller=input()
    prop=input()
    amount=int(input())
    timestamp=time.time()
    return Transaction(buyer_name=buyer,
                       seller_name=seller,
                       prop_name=prop,
                       amount=amount,
                       timestamp=timestamp)
    
def checkTransactionValidity(transac):
    #check if property exists or not
    if mp.get(transac.prop_name) is None:
        return False
    #check if seller owns the property of not
    return mp[transac.prop_name].currentOwner == transac.seller_name

def main():
    run=True
    LMS=Blockchain()
    LMS.create_genesis()
    while run:
        print("Enter 1 for : Add new Transactions occured \nEnter -1 to exit \nEnter 2 to add new property\nEnter 3 to check Transaction History of a Property\nEnter 4 to check block structure")
        val=int(input())
        if val == -1:
            run=False
        elif val == 1:
            print("Enter number of Transactions occured")
            val2=int(input())
            transacs=[]
            for i in range(val2):
                print("Enter details of transaction :",i+1,"\n")
                obj=take_Transac_Input()
                if checkTransactionValidity(obj)==True:
                    transacs.append(obj)
                    print("Transaction Valid.\n")
                else:
                    print("\nTransaction: ",i+1," is Invalid, Hence Rejected and Not Added into Blockchain\n")
            if transacs:
                LMS.mine(transacs)
        elif val == 2:
            print("\nPlease Enter the following in order: 1.Property Name 2.Owner Name\n")
            prop_name=input()
            owner=input()
            prop_obj=Property(currentOwner=owner,
                              previousOwners=[],
                              PropertyName=prop_name,
                              PreviousTransacs=[])
            mp[prop_name]=prop_obj          #map new property name to its newly crated object
            print("Property Registered Sucessfully! \n")
        elif val == 3:
            print("Please Enter the Property Name whose previous transactions you want to view:")
            prop_name=input()
            if mp.get(prop_name) is None:
                print("\nProperty named does NOT exist.\n")
            elif len(mp[prop_name].PreviousTransacs)==0:
                print("No transactions have occured for this given property")
            else:
                for transac in mp[prop_name].PreviousTransacs:
                    print(transac)
        elif val == 4:
            for block in LMS.chain_array:
                print("previous hash is ",block.prev_hash," current block hash is ",block.hash," merke root is ",block.merkleRootHash,"\n")


if __name__=="__main__":
    main()
