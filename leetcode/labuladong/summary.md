单链表 常考点 双指针

数组常用技巧也是双指针 

什么是双指针？ 一快一慢(滑动窗口), 左右到中间, 中间到两边

前缀和 和 差分数组比较特殊的一类

二叉树 有 两类思路: 
1. 遍历得到答案 - 回溯
2. 分解问题得到答案 - 动态规划

遍历: 
```python
# 二叉树最大深度
class Solution:
    def __init__(self):
        self.res=0
        self.depth=0
def max_depth(self, root: TreeNode)->int:
    self.traverse(root)
    return self.res
def traverse(self, root: TreeNode)->None:
    if not root:
        self.res=max(self.res,self.depth)
        return
    self.depth+=1
    self.traverse(root.left)
    self.traverse(root.right)
    self.depth-=1

# 不重复数字全排列 回溯框架
from typing import List
class Solution:
    def __init__(self):
        self.res=[]
        self.track=[]
    def permute(self, nums: List[int])->List[List[int]]:
        self.backtrack(nums)
        return self.res
    def backtrack(self,nums:List[int]):
        if len(self.track)==len(nums):
            self.res.append(self.track[:])
            return

        for i in range(len(nums)):
            if nums[i] in self.track:
                continue
            self.track.append(nums[i])
            self.backtrack(nums)
            self.track.pop()

# 有重复数字的 新增两个剪枝条件 并且排序
    if self.used[i]:
        continue
    if i > 0 && nums[i]==nums[i-1] && not self.used[i-1]:
        continue
```

分解问题:
```python
# 二叉树最大深度
def max_depth(root: TreeNode) -> int:
    if root is None:
        return 0
    left_max=max_depth(root.left)
    right_max=max_depth(root.right)
    res=max(left_max,right_max)+1

    return res
# 最少硬币凑出amount 动态规划框架
def coin_change(coins:List[int], amount:int)->int:
    if amount==0:
        return 0
    if amount<0:
        return -1
    
    res=float('inf')
    for coin in coins:
        sub=coin_change(coins, amount-coin)
        if sub==-1:
            continue
        res=min(res,sub+1)
    return -1 if res==float('inf') else res
# 这个暴力解法加个 memo 备忘录就是自顶向下的动态规划解法
```

前序遍历子问题解法
```python
# 1 2 5 4 6 7 3 8 9
# 1 root
# 2-7 root.left
# 3-9 root.right

from typing import List
def preorder(root: RootNode)->List[int]:
    res=[]
    if not root:
        return res
    res.append(root.val)

    res.extend(preorder(root.left))
    res.extend(preorder(root.right))
    
    return res
```

BFS 框架
```python
# 层序遍历二叉树
class Solution:
    def bfs(self, root: Treenode) -> List[List[int]]:
        if not root:
            return []
        q=collections.deque()
        q.append(root)
        res=[]
        while q:
            size=len(q)
            tmp=[]
            for i in range(size):
                cur = q.popleft()
                tmp.append(cur.val)
                if cur.left:
                    q.append(cur.left)
                if cur.right:
                    q.append(cur.right)
            res.append(tmp)
        return res
```

更进一步，图论相关的算法也是二叉树算法的延续。

比如 图论基础，环判断和拓扑排序 和 二分图判定算法 就用到了 DFS 算法；再比如 Dijkstra 算法模板，就是改造版 BFS 算法加上一个类似 dp table 的数组。