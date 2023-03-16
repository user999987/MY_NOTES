# method 1 space(O(1))
# 最后需要多遍历一次把2变成1
def removeIslands(matrix):
	# Write your code here.
	
	rows=len(matrix)
	cols=len(matrix[0])
	for i in range(cols):
		dfs(matrix,0,i,2)
		dfs(matrix,rows-1,i,2)
	for i in range(rows):
		dfs(matrix,i,0,2)
		dfs(matrix,i,cols-1,2)
	
	for i in range(rows):
		for j in range(cols):
			dfs(matrix,i,j,0)
	for i in range(rows):
		for j in range(cols):
			if matrix[i][j]!=0:
				matrix[i][j]=1
	return matrix
def dfs(matrix, row, col, val):
		print(row, col)
		if not inArea(matrix, row, col) or matrix[row][col]!=1:
			return
		matrix[row][col]=val
		print(matrix)
		dfs(matrix,row-1,col,val)
		dfs(matrix,row+1,col,val)
		dfs(matrix,row,col+1,val)
		dfs(matrix,row,col-1,val)
		
def inArea(matrix, row, col):
	rows=len(matrix)
	cols=len(matrix[0])
	return row>=0 and row<rows and col >=0 and col < cols



# method 2
# 借助 辅助 T 另一个 matrix 标记 元素 处理完 外围元素之后 
# 处理内圈元素只需要 对未被标记的进行处理即可 减少遍历次数