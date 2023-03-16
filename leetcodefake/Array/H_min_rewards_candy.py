'''
老师想给孩子们分发糖果，有 N 个孩子站成了一条直线，老师会根据每个孩子的表现，预先给他们评分。

你需要按照以下要求，帮助老师给这些孩子分发糖果：

每个孩子至少分配到 1 个糖果。
评分更高的孩子必须比他两侧的邻位孩子获得更多的糖果。
那么这样下来，老师至少需要准备多少颗糖果呢？
[1,0,2] - > [2 1 2] 5
[1,2,2] -> [1 2 1] 4
'''

# 从左到右遍历  操作使右边比左边大
# 在从右到左遍历 操作使左边比右边大 重复元素则取最大的因为要满足两侧情况
def minRewards(scores):
    rewards = [1 for _ in scores]
    for i in range(1, len(scores)):
        if scores[i] > scores[i-1]:
            rewards[i] = rewards[i-1]+1
    for i in range(len(scores)-2, -1, -1):
        if scores[i] > scores[i+1]:
            rewards[i] = max(rewards[i], rewards[i+1]+1)
    return sum(rewards)

# inc 和 des 为升降序列长度 prev 为前一个同学糖果数
# inc时 则简单 prev+1 des时 可以用des 本身计数 比如 des为1 prev=1 r+=des
# des为2 r+=des (10,11,12,9,8,7)-[1 2 4 3 2 1]虽然当v=12 时候我们加了 1 而不是4 但是总数是一样的
# 算到最后我们其实相当于 [1 2 4 1 2 3] -> [1 2 4 3 2 1]
def minRewards(scores):
    r=1
    prev=1
    des=0
    inc=1
    for i in range(1, len(scores)):
        if scores[i] >= scores[i-1]:
            prev = 1 if scores[i]==scores[i-1] else prev+1
            inc = prev
            r+=prev
            des = 0
        else:
            des +=1
            if inc==des:
                des+=1
            r+=des
            prev=1
    return r