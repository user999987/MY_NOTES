'''
2,3,1,-4,-4,2 TRUE
'''
def hasSingleCycle(array):
	# Write your code here.
	n=len(array)
	i=0
	idx=0
	while i < n-1:
		idx=getIndex(idx,array)
		
		if idx==0:
			return False
		i+=1
	
	idx=getIndex(idx,array)
	
	if idx!=0:
		return False
	return True
# -2%9 = 1*(-9) + 7 = 7
def getIndex(idx, array):
	a=array[idx]
	n=(idx+a)%len(array)
	print(idx+a,n)
	return n
