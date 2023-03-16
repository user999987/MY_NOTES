'''
"array": [
	[1, 2, 3, 4],
	[12, 13, 14, 5],
	[11, 16, 15, 6],
	[10, 9, 8, 7]
  ]->
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
'''
def spiralTraverse(array):
	r=[]
	rows= len(array)
	columns=len(array[0])
	startR=0
	endR=rows-1
	startC=0
	endC=columns-1
	while startR<endR and startC<endC:
		
		for column in range(startC,endC):
			r.append(array[startR][column])
		
		for row in range(startR, endR):
			r.append(array[row][endC])
		
		for column in range(endC,startC,-1):
			r.append(array[endR][column])
		
		for row in range(endR, startR, -1):
			r.append(array[row][startC])
		startC+=1
		startR+=1
		endR-=1
		endC-=1
	if startR==endR and startC==endC:
		r.append(array[startR][startC])
	elif startR==endR:
		r+=array[startR][startC:endC+1]
	elif startC==endC:
		
		for row in range(startR,endR+1):
			print(row)
			print(array[row])
			r.append(array[row][endC])
			
	return r