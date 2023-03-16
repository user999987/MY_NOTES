class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        def dfs(m,n,i,j):
            if i>=m or j>=n or i<0 or j<0:
                return 0
            if grid[i][j]==0:
                return 0
            grid[i][j]=0
            ans=dfs(m,n,i+1,j)+dfs(m,n,i-1,j)+dfs(m,n,i,j+1)+dfs(m,n,i,j-1)+1
            return ans
        m=len(grid)
        n=len(grid[0])
        res=0
        for i in range(m):
            for j in range(n):
                if grid[i][j]==1:
                    res=max(res,dfs(m,n,i,j))
        return res