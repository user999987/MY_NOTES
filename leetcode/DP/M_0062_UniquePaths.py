class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        d=[[0]*n for _ in range(m)]
        d[0][0]=1
        for i in range(1,m):
            d[i][0]=1
        for j in range(1,n):
            d[0][j]=1
        for i in range(1,m):
            for j in range(1,n):
                d[i][j]=d[i-1][j]+d[i][j-1]
        return d[m-1][n-1]        
        