1. sliding window
```python
s='xxxxxxx'
window=set()
left=0
for i, v in enumerate(s):
    if v not in window:
        window.add(v)
    else:
        while v in window:
            window.remove(s[left])
            left+=1
        window.add(v)
```
2. parentheses stack
```python
s='()((((){{}})))'
pairs={
    ')':'(',
    ']':'[',
    '}':'{',
}
result = []
for v in s:
    if v not in pairs:
        result.append(v)
    else:
        if result and result[-1]==v:
            result.pop()
        else:
            return false
return False if result else True
```

3. 二分法
```python
target=10
s=[???]
left=0
right=len(s)-1
while left<right:
    mid = (left+right)//2
    if s[mid]==target:
        return mid
    elif s[mid]>target:
        right=mid-1
    elif s[mid]<target:
        left=mid+1
if target==s[left]:
    return left
elif target<s[left]:
    return left
elif target>s[left]:
    return left+1
```

4. linked list
```python
node is not None
```

5. 递归
```python
# 重点在于什么条件停止 什么时候继续
# traversal
inorderProcess(root):
    # 递归
    if root is not None:
        inorderProcess(root.left)
        print(root)
        inorderProcess(root.right)
    # else 停止

# isSymmetric
isSymmetric(left, right):
    # 停止
    if left is not None and right is  None:
        return False
    elif left is None and right is not None:
        return False
    elif left is None and right is None:
        return True
    
    elif left is not None and right is not None:
        # 递归
        if left.val == right.val:
            p1=process(left.left,right.right)
            p2=process(left.right,right.left)
            return p1 and p2 
        # 停止
        else:
            return False    
```