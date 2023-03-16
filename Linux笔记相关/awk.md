https://www.ruanyifeng.com/blog/2018/11/awk.html


格式<br>
$ awk 动作 文件名 (前面单引号内部有一个大括号，里面就是每一行的处理动作print $0)

$ echo 'this is a test' | awk '{print $0}'<br>
this is a test

$ echo 'this is a test' | awk '{print $3}'<br>
a

$ echo 'root:x:0:0:root:/root:/usr/bin/zsh' | awk -F ':' '{ print $1 }'