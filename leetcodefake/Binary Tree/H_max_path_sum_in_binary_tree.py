'''
write a function that takes in a Binary Tree and returns its max path sum
                  1
            2           3
        4       5   6       7
-> 18 //5+2+1+3+7

    a
  b   c
当取 bac的时候 这是一个完整路径 和当前最大路径相比 
当取ba 或者ca的时候就是以a的父节点 的左边/右边最大路径的一部分
'''
class BinaryTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def maxPathSum(tree):
    max_path_sum = float('-inf')
    def helper(node):
        nonlocal max_path_sum
        if node is None:
            return 0
        left = helper(node.left)
        right = helper(node.right)
        max_path_sum_candidate = node.value + max(left,0) + max(right,0)
        max_path_sum = max( max_path_sum, max_path_sum_candidate)
        return node.value+max(max(left,right), 0 )
    helper(tree)
    return max_path_sum