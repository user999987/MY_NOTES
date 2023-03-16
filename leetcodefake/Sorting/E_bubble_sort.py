def bubbleSort(array):
    for i in reversed(range(len(array))):
        for j in range(i):
            if array[j]>array[j+1]:
                array[j],array[j+1] = array[j+1],array[j]
    return array