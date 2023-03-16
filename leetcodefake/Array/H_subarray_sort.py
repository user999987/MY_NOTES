'''
"array": [1, 2, 4, 7, 10, 11, 7, 12, 6, 7, 16, 18, 19]-> (最少2个元素的数组)
[3,9]
返回 最小的使整个数组有序的 起始和最终 index 如果数组有序 则返回[-1,-1]
'''

# 排序找最前端和最后端的不同
def subarraySort(array):
	st_array = sorted(array)
	i = 0
	j = len(array)-1
	x_found, y_found = None, None
	while i < j:
		if st_array[i] == array[i]:
			i += 1
		else:
			x_found = i
		if st_array[j] == array[j]:
			j -= 1
		else:
			y_found = j
		if x_found is not None and y_found is not None:
			break

	return [x_found, y_found] if x_found is not None and y_found is not None else [-1, -1]

'''
"array": [1, 2, 4, 7, 10, 11, 7, 12, 6, 7, 16, 18, 19]-> (最少2个元素的数组)
[3,9]
返回 最小的使整个数组有序的 起始和最终 index 如果数组有序 则返回[-1,-1]
'''
# 找出未排序的最大和最小元素然后找到在数组中应该在的位置
def subarraySort(array):
	small = float("inf")
	large = float("-inf")
	for i, v in enumerate(array):
		if not isSortedElement(array, i):
			small = min(small, v)
			large = max(large, v)
	if small == float('inf'):
    		return [-1,-1]
	i=0
	n=len(array)-1
	while array[i]<=small:
    		i+=1
	while array[n]>=large:
    		n-=1
	
	return [i,n]

def isSortedElement(array, i):
	if i == 0:
		return array[i] <= array[i+1]
	elif i == len(array)-1:
		return array[i] >= array[i-1]
	else:
		return array[i-1] <= array[i] and array[i] <= array[i+1]
