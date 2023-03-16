class BST:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def validateBst(tree):
    def validateTree(tree, minVal, maxVal):
        if tree is None:
            return True
        if tree.value < minVal or tree.value >= maxVal:
            return False
        left = validateTree(tree.left, minVal, tree.value)
        right = validateTree(tree.right, tree.value, maxVal)
        return left and right
    return validateTree(tree, float('-inf'), float('inf'))
