'''
[
	[0,-2,-1],
	[-5,2,0],
	[-6,-2,0],
]
->[
	[0,2,-1],
	[5,2,0],
	[-6,2,0],
] # convert negative to positive 1st pass
->[
	[0,2,1],
	[5,2,0],
	[6,2,0]
] # convert negative to positive 2nd pass

'''
# method 1 support matrix
def minimumPassesOfMatrix(matrix):
	positives=0
	zeros=0
	rows = len(matrix)
	cols = len(matrix[0])
	support_matrix = [[0 for j in range(cols)] for i in range(rows)]
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			if matrix[i][j]>0:
				support_matrix[i][j]=1
				positives+=1
			elif matrix[i][j]==0:
				zeros+=1
	loops=0
	negatives = rows*cols-zeros-positives
	print(negatives)
	while negatives!=0 and loops<rows*cols:
		# update matrix
		for i in range(len(matrix)):
			for j in range(len(matrix[i])):
				if 0==negatives:
					break
				if support_matrix[i][j]==1:
					negatives-=convert(i,j,matrix)
		# update support matrix
		for i in range(len(matrix)):
			for j in range(len(matrix[i])):
				if matrix[i][j]>0:
					support_matrix[i][j]=1
		loops+=1
	
	return loops if negatives==0 else -1
def convert(i,j,matrix):
	counter=0
	rows = len(matrix)
	cols = len(matrix[0])
	if i-1>=0: # up
		if matrix[i-1][j]<0:
			counter+=1
		matrix[i-1][j] = abs(matrix[i-1][j])
	if j+1<cols: # right
		if matrix[i][j+1]<0:
			counter+=1
		matrix[i][j+1] = abs(matrix[i][j+1])
	if i+1<rows: # down
		if matrix[i+1][j]<0:
			counter+=1
		matrix[i+1][j] = abs(matrix[i+1][j])
	if j-1>=0: # left
		if matrix[i][j-1]<0:
			counter+=1
		matrix[i][j-1] = abs(matrix[i][j-1])
	return counter

# method 2 记录 正数位置 使用 convert 并把由负得正的数放入下一个queue备用 循环 
# 最后结果 loops-1 因为 当遍历全正的时候 下一个queue总会放入刚转正的点 在进行一次 convert
def minimumPassesOfMatrix(matrix):
	negatives=0
	zeros=0
	rows = len(matrix)
	cols = len(matrix[0])
	curQueue = []
	
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			if matrix[i][j]>0:
				curQueue.append([i,j])
			elif matrix[i][j]<0:
				negatives+=1
	loops=0
	while curQueue:
		nextQueue = []
		while curQueue:
			node = curQueue.pop(0)
			negatives_converted, nextQueueElement = convert(node[0],node[1],matrix)
			#print(nextQueueElement,negatives_converted)
			nextQueue+=nextQueueElement
			negatives-=negatives_converted
		loops+=1
		curQueue = nextQueue[:]
	if negatives==0:
		return loops-1
	else:
		return -1
def convert(i,j,matrix):
	counter=0
	nextQueue=[]
	rows = len(matrix)
	cols = len(matrix[0])
	if i-1>=0: # up
		if matrix[i-1][j]<0:
			counter+=1
			nextQueue.append([i-1,j])
		matrix[i-1][j] = abs(matrix[i-1][j])
		
	if j+1<cols: # right
		if matrix[i][j+1]<0:
			counter+=1
			nextQueue.append([i,j+1])
		matrix[i][j+1] = abs(matrix[i][j+1])
		
	if i+1<rows: # down
		if matrix[i+1][j]<0:
			counter+=1
			nextQueue.append([i+1,j])
		matrix[i+1][j] = abs(matrix[i+1][j])
		
	if j-1>=0: # left
		if matrix[i][j-1]<0:
			counter+=1
			nextQueue.append([i,j-1])
		matrix[i][j-1] = abs(matrix[i][j-1])
		
	return counter,nextQueue