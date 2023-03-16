'''
{
  "array": [12, 3, 1, 2, -6, 5, -8, 6],
  "targetSum": 0
}->
[
  [-8, 2, 6],
  [-8, 3, 5],
  [-6, 1, 5]
]

array is non-empty array of distinct integers 
'''
def threeNumberSum(array, targetSum):
    array.sort()
    n=len(array)
    result=[]
    for i in range(n-2):
        diff = targetSum - array[i]
        left = i+1
        right = n-1
        while left<right:
            l,r=array[left],array[right]
            if l+r>diff:
                right-=1
            elif l+r<diff:
                left+=1
            elif l+r==diff:
                result.append([array[i],l,r])
                right-=1
                left+=1
    return result