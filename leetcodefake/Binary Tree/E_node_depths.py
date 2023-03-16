'''
       1
    2     3
  4   5 6   7
8  9

-> 16
2 depth is 1
3 depth is 1
4 depth is 2
...
sum of all depth is 16
'''


class BinaryTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# 1
def nodeDepths1(root):
    stack = [{'node': root, 'depth': 0}]
    depthSum = 0
    while stack:
        node_map = stack.pop()
        node, depth = node_map['node'], node_map['depth']
        if node is None:
            continue
        depthSum += depth
        stack.append({'node': node.left, 'depth': depth + 1})
        stack.append({'node': node.right, 'depth': depth + 1})
    return depthSum


# 2
def nodeDepths2(root, depth=0):
    if root is None:
        return 0
    return depth + nodeDepths2(root.left, depth + 1) + nodeDepths2(
        root.right, depth + 1)


# 3
def nodeDepths3(root):
    depthSum = 0
    depth = 0

    def helper(node, depth):
        nonlocal depthSum
        if node.left is None and node.right is None:
            depthSum += depth
            return
        depthSum += depth
        if node.left:
            helper(node.left, depth + 1)
        if node.right:
            helper(node.right, depth + 1)

    helper(root, depth)
    return depthSum
