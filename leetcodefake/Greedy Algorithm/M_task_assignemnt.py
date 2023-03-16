'''
k=3
tasks=[1,3,5,3,1,4]
number of tasks always equal 2*k
[
	[0,2]// tasks[0]=1,tasks[2]=5 | 1+5=6
	[4,5]
	[1,3]
] // fastest time to complete all tasks is 6
'''
def taskAssignment(k, tasks):
	maps1 = {k:v for k,v in enumerate(tasks)}
	lists=list(sorted(maps1.items(),key=lambda item:item[1]))
	print(lists)
	result =[]
	i,j=0,len(tasks)-1
	while i<j:
		result.append([lists[i][0],lists[j][0]])
		i+=1
		j-=1
	return result