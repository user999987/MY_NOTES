def insertionSort(array):
    for i in range(1,len(array)):
        for j in range(i,0,-1):
            if array[j]<array[j-1]:
                array[j],array[j-1] = array[j-1],array[j]
    return array