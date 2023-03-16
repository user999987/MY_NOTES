# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        counter =0
        dummy=ListNode()
        dummy.next=head
        prev=dummy
        slow=head
        fast=head
        stack=[]
        while fast:
            tnode=ListNode(fast.val)
            stack.append(tnode)
            fast=fast.next
            counter+=1
            if counter==k:
                counter=0
                while stack:
                    slow=slow.next
                    temp=stack.pop()
                    prev.next=temp
                    prev=temp
        
        if stack:
            prev.next=slow
        return dummy.next
        
    
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head is None:
            return None
        a=b=head
        for i in range(k):
                if b is None:
                    return head
                b=b.next
                
        
        def reverseNodes(a,b):
            prev=None
            cur=a
            nxt=a
            while cur!=b:
                nxt=cur.next
                cur.next=prev
                prev=cur
                cur=nxt
            return prev
        
        newHead=reverseNodes(a,b)
        a.next=self.reverseKGroup(b,k)

        return newHead