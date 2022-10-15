import hashlib

class MerkleTreeHash(object):
    def _init_(self):
        pass
    def find_merkle_hash(self,file_hashes):
        blocks=[]
        if not file_hashes:
            raise ValueError('Missing required file hashes for computing merkle tree hash')
        for m in sorted(file_hashes):
            blocks.append(m)   
        list_len=len(blocks)
        while list_len%2!=0:
            blocks.extend(blocks[-1:])
            list_len=len(blocks)  
        secondary=[]
        for k in [blocks[x:x+2] for x in range(0,len(blocks),2)]:
            hasher=hashlib.sha256()
            hasher.update(str(k[0]+k[1]).encode('utf-8'))
            secondary.append(hasher.hexdigest())
        if len(secondary)==1:
            return secondary[0][0:64]
        else :
            return self.find_merkle_hash(secondary)
        
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
     
if __name__=='__main__':
    import uuid
    file_hashes=[]
    
    for i in range(0,5):
        file_hashes.append(str(uuid.uuid4().hex))
        
    print ('Finding the merkle tree hash of {0} random hashes'.format(len(file_hashes)))
    
    cls=MerkleTreeHash()
    mk=cls.find_merkle_hash(file_hashes)
    print ('The merkle tree hash of the hashes below is : {0}'.format(mk))
    print ('....')
    print (file_hashes)
    