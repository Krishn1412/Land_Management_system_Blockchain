import heapq

# class validator:
#     def __init__(self,name,property):
#         self.name=name
#         self.property=property
    # def validate():
        
        
        
    def is_chain_valid(self, chain):
        _prevBlock = ''
        for block in chain:
            if self.is_block_valid(block, prevBlock=_prevBlock):
                _prevBlock = block
            else:
                return False
        return True