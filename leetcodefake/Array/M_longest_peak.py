'''
"array": [1, 2, 3, 3, 4, 0, 10, 6, 5, -1, -3, 2, 3]->
6 // 0, 10, 6, 5, -1, -3

'''
def longestPeak(array):
    # Write your code here.
    if len(array) < 3:
        return 0
    n = len(array)
    mmax = 0
    for i in range(1, n-1):
        left = i-1
        right = i+1
        peak = True if array[right] < array[i] and array[i] > array[left] else False
        if peak:
            while right < n and array[right-1] > array[right]:
                right += 1
            while array[left] < array[left+1] and left >= 0:
                left -= 1
                print(array[i])
                print(right, left)
            mmax = max(right-left - 1, mmax)

    return mmax
