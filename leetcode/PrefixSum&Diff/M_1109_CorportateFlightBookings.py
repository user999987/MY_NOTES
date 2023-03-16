class Solution:
    diff=None
    length=None
    def buildDifferenceArray(self,n):
        self.length=n
        self.diff = n*[0]
        # for i in range(1,n):
        #     self.diff[i]=l[1]-l[i-1]


    def diffMove(self,i,j,value):
        self.diff[i]+=value
        if j <self.length:
            self.diff[j]-=value
     
    
    def revertDiff(self):
        res=self.length*[0]
        res[0]=self.diff[0]
        for i in range(1,self.length):
            res[i]=self.diff[i]+res[i-1]
        return res
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
       
        self.buildDifferenceArray(n)
        for booking in bookings:
            self.diffMove( booking[0]-1,booking[1],booking[2])
        return self.revertDiff()
