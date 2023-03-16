# method 1
# 遍历直到 根节点 构造数组 在数组上进行操作
class AncestralTree:
    def __init__(self, name):
        self.name = name
        self.ancestor = None


def getYoungestCommonAncestor(topAncestor, descendantOne, descendantTwo):
    # Write your code here.
	
	one = descendantOne
	a1=[]
	l1=0
	while one:
		a1.append(one)
		l1+=1
		one=one.ancestor
	two = descendantTwo
	a2=[]
	l2=0
	while two:
		a2.append(two)
		l2+=1
		two=two.ancestor
	l=min(l1,l2)
	print(a1,a2)
	if a1[-1]!=a2[-1]:
		return topAncestor
	if descendantOne in a2:
		return descendantOne
	if descendantTwo in a1:
		return descendantTwo
	i=-1
	counter=0
	
	while counter<l:
		if a1[i]!=a2[i]:
			print(i,a1[i],a1[i+1])
			return a1[i+1]
		i-=1
		counter+=1
	return topAncestor
	
			

# method 2
# 一样是遍历到根节点 不同的是计算 depth
# 然后将两个节点移动到同一个 level 上 以此查找共同 ancestor