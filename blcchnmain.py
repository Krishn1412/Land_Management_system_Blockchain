import hashlib,binascii,base64,json,requests,random,datetime
from hashlib import sha256
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
