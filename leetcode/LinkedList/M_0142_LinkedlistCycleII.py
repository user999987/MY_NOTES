# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fast=slow=head
        m=None
        while fast and fast.next:
            slow=slow.next
            fast=fast.next.next
            if fast==slow:
                m=fast
                break
        if m is None:
            return m
        while head!=m:
            m=m.next
            head=head.next
        return m
        