'''
radix排序思想 从左到右遍历数组 个位数为 0,1,2,3,4,5,6...9 的数分别放入 对应的桶
第二次遍历 十位数 为0,1,2,3,4,5...9的数分别放入对应的桶 以此类推
如果要算负数的话 则在加10个桶
'''
def radixSort(array):
    n=len(array)
    if n<2:
        return array
    mmax=max(array)
    exp=1
    while mmax//exp > 0:
        array=processRadixSort(array,exp)
        exp*=10
    return array

def processRadixSort(array, exp):
    r=[]
    counter = [[] for _ in range(10)]
    for i in range(len(array)):
        row = array[i]%(exp*10)//exp
        counter[row].append(array[i])
    for x in counter:
        r+=x
        print(r)
    return r