class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        def process(m,n,i,j):
            if i>m-1 or j>n-1 or i<0 or j<0:
                return
            # 重点在于如果遇到岛屿直接加1然后把和他相临的岛全部淹没避免重复计算 line9
            if grid[i][j]=='0':
                return
            grid[i][j]='0'
            process(m,n,i+1,j)
            process(m,n,i-1,j)
            process(m,n,i,j+1)
            process(m,n,i,j-1)
        m=len(grid)
        n=len(grid[0])
        res=0
        for i in range(m):
            for j in range(n):
                if grid[i][j]=='1':
                    res+=1
                    process(m,n,i,j)
        return res