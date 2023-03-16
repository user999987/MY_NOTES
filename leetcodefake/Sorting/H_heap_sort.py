'''
heap sort思想在于完全二叉树 i 节点的子节点为 2*i+1 and 2*i+2 父节点为 (i-1)//2
注意 思想是二叉树 但是没有用到二叉树 还是数组 数组i在堆上的子和父节点可以由上面得到
'''
def heapSort(arr):

    buildHeap(arr)
    for i in range(len(arr)-1, -1, -1):
        swap(arr, 0, i)
        heapify(arr, end=i, i=0)
    return arr


def buildHeap(arr):
    # last node -1 / 2
    firstParent = (len(arr)-1-1)//2
    for i in range(firstParent, -1, -1):
        heapify(arr, len(arr), i)


def heapify(arr, end, i):
    left = 2*i+1
    right = 2*i+2
    largest = i
    if left < end and arr[left] > arr[largest]:
        largest = left
    if right < end and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        swap(arr, i, largest)
        heapify(arr, end, largest)


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

