import heapq

# class validator:
#     def __init__(self,name,property):
#         self.name=name
#         self.property=property
    # def validate():
        
        
        
def stake():
        st={}
        li = [5, 7, 9, 1, 3]
        heapq.heapify(li)
        print("The created heap is : ", end="")
        print(-1*list(li))
        heapq.heappush(li, 4)
        print("The modified heap after push is : ", end="")
        print(-1*list(li))
        print("The popped and smallest element is : ", end="")
        print(heapq.heappop(li))
if __name__=='__main__':
    stake()