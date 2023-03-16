'''
A binary tree is height balanced if for each node in the tree, the difference between 
the height of its left subtree and the height of its right subtree is at most 1.
'''
class BinaryTree:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def heightBalancedBinaryTree(tree):
    flag=True
    def helper(tree):
        nonlocal flag
        if tree is None:
            return 0
        left = helper(tree.left)
        right = helper(tree.right)
        if abs(left-right)>1:
            flag=False
        return max(left,right)+1
    helper(tree)
    return flag