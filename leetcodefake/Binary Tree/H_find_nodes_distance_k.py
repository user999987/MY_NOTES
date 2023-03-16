class BinaryTree:
	def __init__(self, value, left=None, right=None):
		self.value = value
		self.left = left
		self.right = right
		self.coordinates = []

# method 1
# 1 坐标化 标记 level 和 总的 index 根据index得出所在层数的位置 root 位置为 0，0
# 2 计算 结点 和 目标结点 的距离 (不在同层 就先移动到同层 每次移动距离+1 移动到同层之后 
# 	向上移动知道碰面每次 移动 距离+2)
# 3 距离为 k 的放入 result 列表

def calculateDistance(target,node):
	distance = 0
	
	x0,tindex = target.coordinates
	y0=tindex-(2**(x0+1)-1)
	

	x1,nindex = node.coordinates
	y1=nindex-(2**(x1+1)-1)
			   
	print(node.value,node.coordinates)
	print(x0,y0,tindex,x1,y1,nindex)
	while x0>x1:
		x0-=1
		y0//=2
		distance+=1
	while x0<x1:
		x1-=1
		y1//=2
		distance+=1
	while y0!=y1:
		y0//=2
		y1//=2
		distance+=2
	return distance
def findNodesDistanceK(tree, target, k):
	target_node = None
	nodes =[]
	
	def markIndex(tree,level,position):
		nonlocal target_node 
		nonlocal nodes
		if tree is None:
			return
		
		tree.coordinates =[level,position]
		if tree.value == target:
			target_node = tree
		nodes.append(tree)
		markIndex(tree.left,level+1,position*2+1)
		markIndex(tree.right,level+1,position*2+2)
	
	markIndex(tree,0,0)
	if target_node is None:
		return []
	result = [node.value for node in nodes if calculateDistance(target_node,node)==k]
	return result

# method 2 
# 1 遍历 树 给所有节点找 父节点
# 2 遍历 目标结点的 左/右/父节点 直到k=0 需要辅助set 帮助避免重复访问结点
def buildParentsMap(tree, parent,target):
	parentsMap = {}
	targetNode = None
	def parentHelper(tree, parent, target):
		nonlocal targetNode
		if tree is None:
			return
		parentsMap[tree.value] = parent
		if tree.value == target:
			targetNode = tree
		parentHelper(tree.left, tree, target)
		parentHelper(tree.right, tree, target)
	parentHelper(tree, None, target)
	return parentsMap, targetNode

def findNodesDistanceK(tree, target, k):
	parentsMap, targetNode = buildParentsMap(tree, None,target)
	seen = set()
	result = []
	def findNodes(tree, k):
		if tree is None or k < 0 or tree in seen:
			return
		seen.add(tree)
		if k==0:
			result.append(tree.value)
		findNodes(tree.left, k-1)
		findNodes(tree.right, k-1)
		findNodes(parentsMap[tree.value],k-1)
	findNodes(targetNode, k)
	return result

# method 3
# 1 找到目标结点 距离 根节点的距离 X 然后 找到 和目标节点另一侧 深度K-X的结点 
# 和同一侧 则以 目标节点为 根节点 向下遍历找到深度为 k 的结点
