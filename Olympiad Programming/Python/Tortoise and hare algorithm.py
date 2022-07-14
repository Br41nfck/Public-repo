# "Tortoise and hare" algorithm

class Solution:

    def __init__(self, x):
        self.val = x
        self.next = None
        
    def hasCycle(self, head):
        try:
            s = head # Slow
            f = head.next # Fast
            
            while s is not f:
                s = s.next
                f = f.next.next
            return True
        except:
            return False