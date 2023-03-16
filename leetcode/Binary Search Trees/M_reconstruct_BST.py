'''
preOrderTraversalValues = [10,4,2,1,5,17,19,18]
'''
class BST:
	def __init__(self, value, left=None, right=None):
		self.value = value
		self.left = left
		self.right = right
# method 1
def reconstructBst(preOrderTraversalValues):
	def buildBST(array):
		if len(array)<=0:
			return None

		root = BST(array[0])
		border=len(array)
		for i in range(1,border):
			if array[i]>=array[0]:
				border = i
				break
		
		root.left = buildBST(array[1:border])
		root.right = buildBST(array[border:])
		return root
	return buildBST(preOrderTraversalValues)




# method 2

def reconstructBst(preOrderTraversalValues):
	def buildBST(array,start,end):
		
		# print('start,end',array[start],array[end])
		if start>end :
			return None
		print('start,end',array[start],array[end])
		root = BST(array[start])
		border = getBorder(array, start,end)
		root.left = buildBST(array, start+1, border-1)
		root.right = buildBST(array, border, end)
		return root
	return buildBST(preOrderTraversalValues, 0, len(preOrderTraversalValues)-1)

def getBorder(array,start,end):
	
	for i in range(start+1, end+1):
		if array[i]>=array[start]:
			return i
	return end+1