'''
returns a list of its branch sums ordered from leftmost branch sum to rightmost branch sum
'''
class BinaryTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def branchSums(root):
    global result
    result = []
    traverse(root, 0)
    return result


def traverse(node, curSum):
    curSum += node.value
    if node.left is None and node.right is None:
        result.append(curSum)
    if node.left:
        traverse(node.left, curSum)
    if node.right:
        traverse(node.right, curSum)
