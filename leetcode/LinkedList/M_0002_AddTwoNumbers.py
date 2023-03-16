# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy=head=ListNode()
        bit=0
        while l1 or l2:
            lv1= l1.val if l1 else 0
            lv2= l2.val if l2 else 0
            he=lv1+lv2+bit
            if he<10:
                value=he
                bit=0
            else:
                value=he-10
                bit=1
            dummy.next=ListNode(value)
            dummy=dummy.next
            l1=l1.next if l1 else None
            l2=l2.next if l2 else None
        if bit==1:
            dummy.next=ListNode(1)
        return head.next
            