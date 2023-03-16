'''
matrix = [
    [1,0,0,1,0],
    [1,0,1,0,0],
    [0,0,1,0,1],
    [1,0,1,0,1],
    [1,0,1,1,0]
]

DFS 通常是在树和图上进行除此之外 也可以在网格上进行 岛屿问题就是网格DFS典型代表

binary tree的DFS结构
def traverse(root):
    // base case
    if root is None:
        return 
    // access adjacent nodes
    traverse(root.left)
    traverse(root.right)

同样思想到网格
adjacent node是
(r-1,j)(r+1,j) (r,j-1)(r,j+1)
base case 超出网格范围

def dfs(grid, r, c):
    // base case
    if not inArea(grid, r, c):
        return 
    // 不是河或者不是岛
    if grid[r][c] != 1:
        return
    // 标记访问过得岛或者河
    grid[r][c] = 2

    dfs(grid,r-1,c)
    dfs(grid,r+1,c)
    dfs(grid,r,c+1)
    dfs(grid,r,c-1)
def inArea(grid, r, c):
    return r>=0 and r<len(grid) and c>=0 and c<len(grid[0])
'''
def riverSizes(matrix):
    # Write your code here.
	result = []
	for row in range(0,len(matrix)):
		for col in range(0,len(matrix[0])):
			val = dfs(matrix,row,col)
			if val!=0:
				result.append(val)
	return result

def dfs(matrix, row, col):
	width = len(matrix[0])
	height = len(matrix)
	if not inArea(row,col,width,height):
		return 0
	
	if matrix[row][col]!=1:
		return 0
	matrix[row][col]=2
	up=dfs(matrix,row-1,col)
	down=dfs(matrix,row+1,col)
	right=dfs(matrix,row,col+1)
	left=dfs(matrix,row,col-1)
	re = 1+ up+down+left+right
	print('row,col.',row,col,up,down,left,right)
	return re

def inArea(i,j,width,height):
	if i>=height or i <0 or j >=width or j<0:
		return False
	else:
		return True