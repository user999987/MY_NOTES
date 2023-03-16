def nextGreaterElement(nums):
	# Write your code here.
	newArr = nums *2
	result = [-1]*len(nums)
	stack = []
	for i in range(len(newArr)-1,-1,-1):
		
		if len(stack)==0:
			stack.append(newArr[i])
			continue
		
		while stack and stack[-1]<=newArr[i]:
			stack.pop()
		if stack and newArr[i]< stack[-1]:
			result[i%len(nums)] = stack[-1]
		stack.append(newArr[i])
		
	return result

# 优化
def nextGreaterElement(nums):
	newArr = nums *2
	result = [-1]*len(nums)
	stack = []
	for i in range(len(newArr)-1,-1,-1):
		idx = i%len(nums)
		
		while stack:
			if stack[-1] >nums[idx]:
				result[idx] = stack[-1]
				break
			else:
				stack.pop()
		stack.append(nums[idx])
	return result