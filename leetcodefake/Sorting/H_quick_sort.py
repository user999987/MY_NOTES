# 递归
def quickSort(array):
	start = 0
	end=len(array)-1
	startSort(start,end,array)
	return array

def startSort(start, end, array):
	left=start
	right =end
	pillar=left
	if left>=right:
		return
	while left < right:
		if array[pillar]>=array[right]:
			array[right],array[pillar] = array[pillar],array[right]
			pillar=right
			left+=1
		if array[pillar]<=array[left]:
			array[left],array[pillar] = array[pillar],array[left]
			pillar=left
			right-=1
	startSort(start,pillar-1,array)
	startSort(pillar+1,end,array)
# 非递归
def quickSort(array):
	start=0
	end=len(array)-1
	stack=[start,end]
	if start<end:
		while stack:
			r=stack.pop()
			l=stack.pop()
			pillar=partition(array,l,r)
			if l<pillar-1:
				stack.append(l)
				stack.append(pillar-1)
			if pillar+1<r:
				stack.append(pillar+1)
				stack.append(r)
	return array
def partition(array,start,end):
	left=start
	right=end
	pillar=start
	while left < right:
		if array[right]<=array[pillar]:
			swap(right,pillar,array)
			pillar = right
			left+=1
		if array[left]>=array[pillar]:
			swap(left,pillar,array)
			pillar=left
			right-=1
	return pillar
def swap(i,j,array):
	array[i],array[j]=array[j],array[i]