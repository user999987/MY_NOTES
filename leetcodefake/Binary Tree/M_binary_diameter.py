'''
				1
			3       2
		7       4
	8               5
9                       6
-> 6 // 9,8,7,3,4,5,6
'''
class BinaryTree:
	def __init__(self, value, left=None, right=None):
		self.value = value
		self.left = left
		self.right = right



def binaryTreeDiameter(tree):
	def helper(tree):
		if tree is None:
			return 0,0
		left_height, left_diameter = helper(tree.left)
		right_height, right_diameter = helper(tree.right)
		diameter = max(left_height+right_height, left_diameter, right_diameter)
		height = max(left_height,right_height)+1
		return height,diameter
	height,diameter = helper(tree)
	print(height,diameter)
	return diameter

		
def binaryTreeDiameter(tree):
	ssum=0
	def helper(node):
		nonlocal ssum
		if node is None:
			return 0
		left = helper(node.left)
		right = helper(node.right)
		ssum=max(left+right,ssum)
		
		return max(left,right)+1
	helper(tree)
	return ssum

'''
深度 depth 递归时每次传入参数 depth+1
recursive(depth+1)
高度 height node是叶子结点(左右子树为空) 返回零 其他返回 高度+1
recursive(node):
	if node.left is None and node.right is None:
    	return 0
	left = recursive(node.left)
	right = recursive(node.right)
	return max(left,right)+1
'''