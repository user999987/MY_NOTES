# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def swapPairs(self, head: ListNode) -> ListNode:
        def process(head):
            if head and head.next:
                newHead=head.next
                head.next=process(newHead.next)
                newHead.next=head
                return newHead
            else:
                return head
        return process(head)