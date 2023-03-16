'''
先排序
4数和 确定 第一层循环 确定第二层循环 收尾指针中间移动
然后移动第二层循环 +1 继续收尾指针中间移动
etc 然后第一层循环+1 继续执行
优化在于 最左4数和大于目标值 continue 或者 break
i和最右3数和小于 目标值 则 i需要+1 然后继续
去重主要在于 判断当前值和之前的值是否相等 相等的话等于这个数已经用过了 不需要再计算
直接continue跳过
'''
def fourNumberSum(array, targetSum):
    	
    n = len(array)
    if not array or n < 4:
        return None
    array.sort()
    r = []

    for i in range(n-3):
        if i > 0 and array[i] == array[i-1]:
            continue
        min1 = array[i]+array[i+1]+array[i+2]+array[i+3]
        if min1 > targetSum:
            break
        max1 = array[i]+array[n-1]+array[n-2]+array[n-3]
        if max1 < targetSum:
            continue
        for j in range(i+1, n-2):
            if j > 1+i and array[j] == array[j-1]:
                continue
            min2 = array[i]+array[j]+array[j+1]+array[j+2]
            if min2 > targetSum:
                break
            max2 = array[i]+array[j]+array[n-2]+array[n-1]
            if max2 < targetSum:
                continue
            k = j+1
            h = n-1
            while k < h:
                curSum = array[i]+array[j]+array[k]+array[h]
                if curSum == targetSum:
                    r.append([array[i], array[j], array[k], array[h]])
                    k += 1
                    while k < h and array[k] == array[k-1]:
                        k += 1
                    h -= 1
                    while k < h and array[h] == array[h+1]:
                        h -= 1
                elif curSum > targetSum:
                    h -= 1
                elif curSum < targetSum:
                    k += 1
    return r
