import hashlib,binascii,base64,json,requests,random,datetime
class Transaction:
    def __init__(self,buyer_name,seller_name, property_name, amount, Timestamp_of_the_transaction):
        self.buyer_name=buyer_name
        self.seller_name=seller_name
        self.property_name=property_name
        self.amount=amount
        self.Timestamp_of_the_transaction=Timestamp_of_the_transaction
class Block:
    def __init__(self,index,hash,previousHash,timestamp,data,difficulty,nonce):
        self.index=index
        self.hash=hash
        self.previousHash=previousHash
        self.timestamp=timestamp
        self.data=data
        self.difficulty=difficulty
        self.nonce=nonce
class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.new_block(previous_hash=1, proof=100)
