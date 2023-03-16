
# method 1
def sameBsts(arrayOne, arrayTwo):
	return bstCheck(arrayOne[:], arrayTwo[:])

def bstCheck(arr1,arr2):
	if len(arr1)==0:
		return True
	elif arr1[0]!=arr2[0] or len(arr2)!=len(arr1):
		return False
	
	arr1map = {'L':[],'R':[]}
	arr2map = {'L':[],'R':[]}
	for i in range(1,len(arr1)):
		if arr1[i] < arr1[0]:
			arr1map['L'].append(arr1[i])
		else:
			arr1map['R'].append(arr1[i])
		if arr2[i] < arr2[0]:
			arr2map['L'].append(arr2[i])
		else:
			arr2map['R'].append(arr2[i])
	left = bstCheck(arr1map['L'][:], arr2map['L'][:])
	right = bstCheck(arr1map['R'][:], arr2map['R'][:])
	return left and right

# method 2
def sameBsts(arrayOne, arrayTwo):
	return bstCheck(arrayOne, arrayTwo, 0, 0, float('-inf'), float('inf'))

def bstCheck(arr1,arr2, root1Index, root2Index, minValue, maxValue):
	
	if root1Index==-1 or root2Index==-1:
		return root1Index == root2Index
	elif arr1[root1Index]!=arr2[root2Index]:
		return False
	
	left1Idx = getLeftIdx(arr1, root1Index, minValue)
	right1Idx = getRightIdx(arr1, root1Index, maxValue)
	
	left2Idx = getLeftIdx(arr2, root2Index, minValue)
	right2Idx = getRightIdx(arr2, root2Index, maxValue)
	
	left = bstCheck(arr1,arr2, left1Idx, left2Idx, minValue, arr1[root1Index])
	right = bstCheck(arr1,arr2, right1Idx, right2Idx,  arr1[root1Index], maxValue)
	
	return left and right

def getLeftIdx(array, rootIdx, minValue):
	for i in range(rootIdx+1, len(array)):
		if array[i]<array[rootIdx] and array[i]>=minValue:
			return i
	return -1

def getRightIdx(array, rootIdx, maxValue):
	for i in range(rootIdx+1, len(array)):
		if array[i]>=array[rootIdx] and array[i]<maxValue:
			return i
	return -1