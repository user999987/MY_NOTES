# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        def process(root,ans):
            if root.left is None and root.right is None:
                if ans+root.val==targetSum:
                    return True
                return False
            
            if root.left and process(root.left,ans+root.val):
                return True
            if root.right and process(root.right,ans+root.val):
                return True
                 
            return False
        if root:
            return process(root,0)
        else:
            return False
                
        