'''

'''
def tandemBicycle(redShirtSpeeds, blueShirtSpeeds, fastest):
    # Write your code here.
    a= redShirtSpeeds
    b= blueShirtSpeeds
    result = 0
    if fastest:
        a.sort()
        b.sort(reverse=True)
        for i in range(len(a)):
            result+=max(a[i],b[i])
    else:
        a.sort()
        b.sort()
        for i in range(len(a)):
            result+=max(a[i],b[i])
    return result