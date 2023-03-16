# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        res=[]
        def process(root,track):
            
            if root is None:
                return
            track.append(root.val)
            if root.left is None and root.right is None:
               if sum(track)==targetSum:
                    res.append(track[:])
                return
            process(root.left,track[:])
            process(root.right,track[:])
            track.pop()
        process(root,[])
        return res