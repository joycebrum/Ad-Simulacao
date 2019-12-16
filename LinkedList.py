
class Node:
    def __init__(self, dataval=None):
        self.dataval = dataval
        self.nextval = None

class SLinkedList:
    def __init__(self):
        self.headval = None
    
    def add(self, element):
        if self.headval == None:
            self.headval = Node(element)
        else:
            novo = Node(element)
            if self.headval.dataval.time >= element.time:
                novo.nextval = self.headval
                self.headval = novo
                return True
            atual = self.headval
            while atual.nextval != None:
                if atual.nextval.dataval.time >= element.time:
                    novo.nextval = atual.nextval
                    atual.nextval = novo
                    return True
                atual = atual.nextval
                    
            if atual.nextval == None:
                atual.nextval = novo
        return False
    
    def console(self):
        atual = self.headval
        while atual != None:
            print(atual.dataval)
            atual = atual.nextval
    
    def pop_front(self):
        if self.headval != None:
            head = self.headval.dataval
            self.headval = self.headval.nextval
            return head
        return None
    
    def getInterruption(self, exitTime, priority):
        atual = self.headval
        
        while atual != None:
            if atual.dataval.time >= exitTime:
                return None
            if atual.dataval.event == "chegada" and atual.dataval.priority < priority:
                return atual.dataval
            atual=atual.nextval
        return None
    
    def empty(self):
        return self.headval == None