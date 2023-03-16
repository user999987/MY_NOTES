# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        res=[]
        def process(root,ans):
            if root.left is None and root.right is None:
                res.append(ans*10+root.val)
            if root.left:
                process(root.left,ans*10+root.val)
            if root.right:
                process(root.right,ans*10+root.val)
        process(root,0)
        return sum(res)
            