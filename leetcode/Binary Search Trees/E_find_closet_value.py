
'''
Returns a closet value to target value
'''

# This is the class of the input tree. Do not edit.
class BST:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def findClosestValueInBst(tree, target):
    result = None
    result_ref = float('inf')
    def findValue(tree, target):
        nonlocal result, result_ref
        if tree is None:
            return
        value = abs(tree.value-target)    
        if value < result_ref:
            result = tree.value
            result_ref = value
        findValue(tree.left, target)
        findValue(tree.right, target)
        return
    findValue(tree, target)
    return result