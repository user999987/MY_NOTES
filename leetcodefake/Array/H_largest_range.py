'''
 "array": [0, -5, 9, 19, -1, 18, 17, 2, -4, -3, 10, 3, 12, 5, 16, 4, 11, 7, -6, -7, 6, 15, 12, 12, 2, 1, 6, 13, 14, -2]
-> [-7, 7]
拿到一个数组 返回最大 range
range的定义是 [1,5] 当[1,2,3,4,5]or [1,1,2,2,3,4,5,3,2,3,4,2,5]
'''
# method 1
def largestRange(array):
	new_array = sorted(array)
	result =[0,0]
	temp = [0,0]
	n = len(new_array)
	if n ==1:
		return [array[0],array[0]]
	prev = new_array[0]
	recordSwitch = 0
	for i in range(1,n):
		if new_array[i]-1==prev:
			if recordSwitch ==0:
				recordSwitch=1
				temp[0]=prev

		elif new_array[i]==prev:
			pass
		else:
			if recordSwitch == 1:
				temp[1] = prev
				recordSwitch=0
		prev = new_array[i]
		result = max(result[:],temp[:],key=lambda x:x[1]-x[0])
	if recordSwitch==1:
		temp[1] = prev
		result = max(result[:],temp[:],key=lambda x:x[1]-x[0])
	return result

# method 2
def largestRange(array):
	longestLength = 0
	result = []
	dmap = {}
	for v in array:
		dmap[v] = True
	for v in array:
		currentLength = 1
		left = v-1
		right = v+1
		while left in dmap:
			currentLength+=1
			left-=1
		while right in dmap:
			currentLength+=1
			right+=1
		if currentLength>longestLength:
			longestLength = currentLength
			result = [left+1,right-1]
	return result