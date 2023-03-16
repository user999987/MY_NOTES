'''
2个数组代表2排人的身高 排队
后面的人必须必前面的人 严格 高 不然排队失败
a=[5,8,1,3,4] b=[6,9,2,4,5]

'''
def classPhotos(redShirtHeights, blueShirtHeights):
	# Write your code here.
	redShirtHeights.sort()
	blueShirtHeights.sort()
	if redShirtHeights[0] == blueShirtHeights[0]:
		return False
	else:
		flag = -1 if redShirtHeights[0] > blueShirtHeights[0] else 1
	for i in range(1,len(redShirtHeights)):
		if flag == -1:
			if redShirtHeights[i]<blueShirtHeights[i]:
				return False
		else:
			if redShirtHeights[i]>blueShirtHeights[i]:
				return False
	return True
