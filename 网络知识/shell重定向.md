一个命令通常从一个叫标准输入的地方读取输入，默认情况下，这恰好是你的终端。同样，一个命令通常将其输出写入到标准输出，默认情况下，这也是你的终端。
```
command > file # 输出重定向到 file
command >> file # 输出以追加的方式重定向到 file
command < file # 输入重定向到 file
```

1. 文件描述符就是一个整形数字
2. 每个进程默认打开 0、1、2 三个文件描述符， 新的文件描述符都是从 3 开始分配
3. 一个文件描述符被回收后可以再次被分配 (文件描述符并不是递增的)
4. 每个进程单独维护了一个文件描述符的集合


一般情况下，每个 Unix/Linux 命令运行时都会打开三个文件：
* 标准输入文件(stdin)：stdin的文件描述符为0，Unix程序默认从stdin读取数据。
* 标准输出文件(stdout)：stdout 的文件描述符为1，Unix程序默认向stdout输出数据。
* 标准错误文件(stderr)：stderr的文件描述符为2，Unix程序会向stderr流中写入错误信息。

默认情况下:
* command > file 将 stdout 重定向到 file (command 1> file)
* command < file 将stdin 重定向到 file (command 0< file)

``` 
n> file # 文件描述符为 n 的文件重定向到 file
n>> file # 文件描述符为 n 的文件以追加的方式重定向到 file
n>&m # 将输出文件 m 和 n 合并
n<&m # 将出入文件 m 和 n 合并


here document
```bash
command << delimiter
    Here Document Content
delimiter
```
作用就是把 两个 delimiter 之间的内容 (Here Document Content 部分)传递给cmd作为输入参数\
比如在终端中输入cat << EOF ，系统会提示继续进行输入，输入多行信息再输入EOF，中间输入的信息将会显示在屏幕上
1. 例1
```bash
cat << EOF
> First Line
> Second Line
> Third Line EOF
> EOF
First Line
Second Line
Third Line EOF
```
2. 例2
    有个here.sh文件\
    ```bash
    cat << EOF > output.sh
    echo "hello"
    echo "world"
    EOF
    ```
    sh here.sh 运行以上脚本会得到一个新的文件 output.sh其内容是
    ```
    echo "hello"
    echo "world"
    ```