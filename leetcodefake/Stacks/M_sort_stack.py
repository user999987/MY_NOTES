'''
[-5,2,-2,4,3,1]->
[-5,-2,1,2,3,4]

only allow pop and append operations
recursively sorts the stack in place
'''
def sortStack(stack):
    if len(stack) == 0:
        return stack
    
    top = stack.pop()
    sortStack(stack)

    partialSort(stack, top)
    return stack
def partialSort(stack, value):
    if len(stack)==0 or stack[-1]<=value:
        stack.append(value)
        return
    top = stack.pop()
    partialSort(stack,value)
    stack.append(top)