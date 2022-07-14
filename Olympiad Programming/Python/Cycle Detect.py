# Cycle Detection in Linked List 

def DetectCycle(head):
    s, f = head, head # s - slow, f - fast 
    while f and f.next:
        s = s.next
        f = f.next.next
        if s == f:
            s = head
            while s != f:
                s = s.next
                f = f.next
            return s