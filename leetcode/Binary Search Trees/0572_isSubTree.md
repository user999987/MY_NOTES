```python
# if t is subtree of s
class Solution:
    def isSubtree(self, s: TreeNode, t: TreeNode) -> bool:

        def check(cur, t):
            if not cur and not t: return True
            if not cur or not t: return False
            if cur.val != t.val: return False
            return check(cur.left, t.left) and check(cur.right, t.right)

        def dfs(s, t):
            if not s:
                return False
            return check(s, t) or dfs(s.left, t) or dfs(s.right, t)

        return dfs(s, t)
```