'''
非空 正数 数组 每个元素代表需要执行的时间
[5,4,1]
每次只有一个任务可以在执行
总等待时间为 0+(5+0)+(5+4+0) = 14
求最小等待时间
'''
def minimumWaitingTime(queries):
	queries = sorted(queries)
	single_wait_time,result=0,0
	print(queries)
	for i in range(1,len(queries)):
		single_wait_time+=queries[i-1]
		result+=single_wait_time
	return result