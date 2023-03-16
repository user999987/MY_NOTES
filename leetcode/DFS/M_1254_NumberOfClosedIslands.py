class Solution:
    def closedIsland(self, grid: List[List[int]]) -> int:
        def dfs(m,n,i,j):
            if i>=m or j>=n or i <0 or j<0:
                return
            if grid[i][j]==1:
                return
            grid[i][j]=1
            dfs(m,n,i-1,j)
            dfs(m,n,i+1,j)
            dfs(m,n,i,j-1)
            dfs(m,n,i,j+1)

        m=len(grid)
        n=len(grid[0])
        for i in range(m):
            dfs(m,n,i,0)
            dfs(m,n,i,n-1)
        print(grid)
        for j in range(n):
            dfs(m,n,0,j)
            dfs(m,n,m-1,j)
        res=0

        
        for i in range(m):
            for j in range(n):
                if grid[i][j]==0:
                    res+=1
                    dfs(m,n,i,j)
        return res