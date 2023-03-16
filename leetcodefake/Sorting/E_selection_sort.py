def selectionSort(array):
    for i in range(len(array)-1,-1,-1):
        for j in range(i):
            if array[j]>array[i]:
                array[j],array[i]=array[i],array[j]
    return array