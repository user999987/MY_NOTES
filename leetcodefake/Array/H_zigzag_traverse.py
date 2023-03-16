'''
此题重点在于4条边上 遍历遇到左右两边向下 遇到上下两边向右 同时碰到右上或者左下 2边时候
有不同优先级 右上要先往下即先判断右边 左下要先向右 即先判断底边 不然会有越界结果
还要有辅助的 goindDown=True 帮助解决移动问题遇到边时 goingDown 的值会 not 一下
"array": [
    [1, 3, 4, 10],
    [2, 5, 9, 11],
    [6, 8, 12, 15],
    [7, 13, 14, 16]
  ]->
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

"array": [
    [1, 3],
    [2, 4],
    [5, 7],
    [6, 8],
    [9, 10]
  ]->
  [1,2,3,4,5,6,7,8,9,10]
'''
def zigzagTraverse(array):
    rows = len(array)-1
    coloumns=len(array[0])-1
    totalElements = (rows+1)*(coloumns+1)
    i = 0
    row,col = 0,0
    goingDown = True
    r=[]
    while i < totalElements:
        r.append(array[row][col])
        if goingDown:
            
            if row==rows:
                col+=1
                goingDown=False
            elif col==0:
                row+=1
                goingDown=False
            else:
                col-=1
                row+=1
        else:
        
            if col == coloumns:
                row+=1
                goingDown=True
            elif row==0:
                col+=1
                goingDown=True
            else:
                col+=1
                row-=1
        i+=1
		
    return r
           