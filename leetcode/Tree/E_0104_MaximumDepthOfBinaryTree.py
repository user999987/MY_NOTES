# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def process(root):
            if root==None:
                return 0
            leftD=process(root.left)
            rightD=process(root.right)
            return max(leftD,rightD)+1
        return process(root)
            