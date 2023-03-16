'''
{
  "arrayOne": [-1, 5, 10, 20, 28, 3],
  "arrayTwo": [26, 134, 135, 15, 17]
} ->
[26,28]
'''
def smallestDifference(arrayOne, arrayTwo):
	arrayOne.sort()
	arrayTwo.sort()
	minCombination=[float("inf"),"inf","inf"]
	index1=0
	index2=0
	while index1<len(arrayOne) and index2<len(arrayTwo):
		diff = arrayOne[index1]-arrayTwo[index2]
		absdiff = abs(diff)
		if diff==0:
			return [arrayOne[index1],arrayTwo[index2]]
		if absdiff < minCombination[0]:
			minCombination=[absdiff, arrayOne[index1],arrayTwo[index2]]
		if diff>0:
			index2+=1
		elif diff<0:
			index1+=1
		
	return minCombination[1:]
