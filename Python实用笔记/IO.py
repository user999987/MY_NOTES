# mode has w,r,a
# write will overwrite
# r will read and a will append
# if file do not exist a and w will create a new one
# if you want to read and write the file at the same time use r+ or w+ or a+
# difference between r+ and a+ is the location of file pointer
# r+ file pointer points to the begining of the file
# a+ file pointer points to the end of the file
import json
x=[{"name":"job","action":"slepp"},{"name":"job","action":"slepp"}]
with open('filename','a+') as f:
    json_string = json.dumps(x)
    f.write(json_string)
# 本质上 json 是一个字符串 所以你如果 使用 f.read 读取file内容 你的得到的就是一个字符串 
# 你可以把他转换成 python object 在操作

