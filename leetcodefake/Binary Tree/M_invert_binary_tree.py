class BinaryTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# 1
def invertBinaryTree(tree):
    if tree is None:
        return
    tree.left, tree.right = tree.right, tree.left
    invertBinaryTree(tree.left)
    invertBinaryTree(tree.right)

# 2
def invertBinaryTree2(tree):
    stack = [tree]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        node.left, node.right = node.right, node.left
        stack.append(node.left)
        stack.append(node.right)
    