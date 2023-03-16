'''
{
  "array": [2, 1, 2, 2, 2, 3, 4, 2],
  "toMove": 2
}->
[4, 1, 3, 2, 2, 2, 2, 2]
'''

def moveElementToEnd(array, toMove):
	
	n=len(array)
	left=0
	right=n-1
	while left<right:
		if array[right] == toMove:
			right-=1
			continue
		if array[left] !=toMove:
			left+=1
			continue
		array[left],array[right] = array[right],array[left]
		left+=1
		right-=1
	return array
