'''

edges = [
	[1,3],
	[2,3,4],
	[0],
	[],
	[2,5]
	[],
]

'''
def cycleInGraph(edges):
	numOfVertices = len(edges)
	visited = [0]*numOfVertices
	result = False
	def dfs(vertex, seen):
		nonlocal result
		if visited[vertex]==1:
			return
		visited[vertex]=1
		seen.add(vertex)
		for v in edges[vertex]:
			if v in seen:
				result=True
				return 
			else:
				dfs(v,seen)
		seen.remove(vertex)
		
	for vertex in range(numOfVertices):
		if visited[vertex]==1:
			continue
		else:
			dfs(vertex,set())
	return result
