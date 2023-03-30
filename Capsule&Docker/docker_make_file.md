```docker
DOCKER_BUILDKIT=1 docker build --progress=plain --target=insula --build-arg=SOURCE_COMMIT=`git rev-parse HEAD` --build-arg=BRANCH=`git rev-parse --abbrev-ref HEAD` $(additional_build_args) -t insula-dev:1.0.0 .

docker-compose $(all) build  $(additional_build_args) $(args) insula-db
```

`progress`: Set type of progress output (auto, plain, tty). Use plain to show container output
`target`: Set the target build stage to build.
`build-arg`: Set build time variables
`--tag` or `-t`: Name and optionally a tag in the 'name:tag' format



Makefile 文件由一系列规则(rules)构成. 每条规则形式如下:
```
<target>: <prerequisites>
[tab] <commands> ([tab]表示是一个tab键)

//Make命令直接就是要做出某个文件
a.txt: b.txt c.txt
    cat b.txt c.txt > a.txt
```
target是必须的, prerequisite 和 commands 是可选的,但是必须存在其中之一<br>
但是也可以不是文件名 
```docker
clean:
    rm * .o
```
此时 clean是一个 phony target. 但是如果当前目录中正好有一个叫 clean 的文件, 这个命令就不会执行. 因为Make发现clean文件已经存在, 就认为没有必要重新构建了, 就不会执行指定的rm命令.<br>
To avoid this
```docker
.PHONY: clean
clean:
    rm *.o temp
```
声明clean是"伪目标"之后，make就不会去检查是否存在一个叫做clean的文件.如果Make命令运行时没有指定目标，默认会执行Makefile文件的第一个目标。
如果需要生成多个文件，往往采用下面的写法。
```docker
source: file1 file2 file3
```


```make
aws_cli_major_version = $(shell aws --version 2>&1 | sed -E -e 's@^aws-cli/([^.]*)\..*$$@\1@')
```
shell function: 
```make
srcfiles := $(shell echo src/{00..99}.txt)
```