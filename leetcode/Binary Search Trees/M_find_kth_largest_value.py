'''
中序遍历BST 数组是升序的
'''

class BST:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def findKthLargestValueInBst(tree, k):
    traveral = []
    def inorderTraverse(tree):
        if tree is None:
            return
        inorderTraverse(tree.left)
        traveral.append(tree.value)
        inorderTraverse(tree.right)
    inorderTraverse(tree)
    return traveral[-k] if len(traveral)>=k else -1