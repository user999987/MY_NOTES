'''
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

According to the definition of LCA on Wikipedia: “The lowest common 
ancestor is defined between two nodes p and q as the lowest node in T 
that has both p and q as descendants (where we allow a node to be a descendant of itself).”
						3
			5                       1
		6       2               0        8
			  7    4
root=3, p=5, q=1
output is 3
root=3, p=5, q=4
output is 5

换种思路 不找祖先 找结点子树是否包含 目标结点 p q
DFS 后序遍历 找不到目标结点返回 None 找到则返回 目标结点 

'''

# method 1
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode):
	if root is None:
		return None
	if root == p or root ==q :
		return root
	left= lowestCommonAncestor(root.left, p, q)
	right = lowestCommonAncestor(root.right, p, q)
	if left is None and right is None:
		return None
	if left and right:
		print(root.val)
		return root
	if left:
		return left
	if right:
		return right

# method 2 
# store parent and level 
# parentHelper(tree, parent, target):
# 		tree.parent = parent