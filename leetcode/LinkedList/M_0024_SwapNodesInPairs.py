# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def swapPairs(self, head: ListNode) -> ListNode:
        def process(head):
            if not head or not head.next:
                return head
            newHead=head.next
            head.next = process(head.next.next)
            newHead.next=head
            return newHead
        return process(head)