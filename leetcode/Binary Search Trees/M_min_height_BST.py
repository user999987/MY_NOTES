'''
input is non-empty sorted array of distinct integers
'''
class BST:
	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None

# method 1
def minHeightBst(array):
	
	def buildBST(array):
		end = len(array)
		if end<=0:
			return None
		elif end==1:
			return BST(array[0])
		mid = end//2
		root = BST(array[mid])
		root.left = buildBST(array[0:mid])
		root.right = buildBST(array[mid+1:])
		return root
	
	return buildBST(array)

# method 2
def minHeightBst(array):
		
	def buildBST(array, start, end):
		if start>end:
			return None
		mid = (start+end)//2
		root = BST(array[mid])
		root.left = buildBST(array, start,mid-1)
		root.right = buildBST(array, mid+1, end)
		return root
	
	return buildBST(array, 0, len(array)-1)