'''
A node's successor is the next node to be vistied (immediately after the given node)
when traversing its tree using the in-order tree-traversal technique
'''
class BinaryTree:
	def __init__(self, value, left=None, right=None, parent=None):
		self.value = value
		self.left = left
		self.right = right
		self.parent = parent

# 1
def findSuccessor(tree, node):
	# Write your code here.
	nodes=[]
	helper(tree,nodes)
	index=-1
	for i,v in enumerate(nodes):
		if v.value==node.value:
			index=i
			break
	if index!=-1:
		if index!=len(nodes)-1:
			return nodes[index+1]
	return None 

def helper(tree,nodes):
	if tree is None:
		return
	helper(tree.left,nodes)
	nodes.append(tree)
	helper(tree.right,nodes)

# 2
def findSuccessor2(tree,node):
	x=None
	if node.right:
    	# condition1 node has right child
		x=getMostLeft(node.right)
	elif node.parent:
    	# condition2 node has parent
		# subcondition2 node's parent has right node which is itself
		if node.parent.right == node:
			node=node.parent
			if node.parent:
				x=node.parent
		else:
    		# subcondition2 node's parent do not has right child which means successor it
			# is node's parent
			x=node.parent
	return x

def getMostLeft(node):
	
	while node.left:
		node = node.left
	return node