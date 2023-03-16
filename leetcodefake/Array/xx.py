def fourNumberSum(array, targetSum):
    # Write your code here.
    array.sort()
    r = []
    n = len(array)
    if not array or n < 4:
        return None
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
                continue
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
                    while k < h and h > j and array[h] == array[h+1]:
                        h -= 1
                elif curSum > targetSum:
                    h -= 1
                elif curSum < targetSum:
                    k += 1
        return r
