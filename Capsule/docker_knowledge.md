Docker镜像是由特殊的文件系统叠加而成，最底端是 bootfs，并使用宿主机的bootfs；第二层是 root文件系统rootfs，称为base image；然后再往上可以叠加其他的镜像文件。
(1). docker 镜像的本质是什么？

答：是一个分层的文件系统。

(2). docker中一个centos镜像大约200M左右，为什么一个centos系统的iso安装文件要好几个G？

答：centos的iso文件包括bootfs和rootfs，而docker的centos镜像复用操作系统的bootfs。

(3). docker中一个tomcat镜像大约500M左右，为什么一个tomcat安装包不足100M呢？

答：docker中的镜像是分层的，tomcat虽然只有70多M，但是它需要依赖父镜像和基础镜像，所有整个对外暴露的tomcat镜像大约500M左右。

Dokcer file
```docker
FROM 指定基础镜像
MAINTAINER  指定维护者信息
RUN run命令 比如 apt-get
ADD COPY文件
WORKDIR 设置当前工作目录
VOLUME 设置卷，挂载主机目录
EXPOSE 开放端口
CMD 容器启动后要干的事情
```
镜像- 一堆 read-only layer<br>
容器- 在镜像上面加一个 read-write layer<br>
container = image + read-write layer<br>
running container = 一个可读写的统一文件系统加上隔离的进程空间和包含其中的进程<br>
```docker
docekr create \<image-id\>: 为 image 添加了一个可读写层, 构成了一个新的容器,但是这个容器并没有运行.
docker start \<container-id\>: 为容器文件系统创建了一个进程隔离空间。注意，每一个容器只能够有一个进程隔离空间

docker run = docker create + docker start

docker ps [-a]
docker images [-a]
docker history <image-id> (show all layers under the image)
docker stop/kill <container-id>
docker rm <container-id> (对非运行态容器使用 移除 read-write layer)
docker rmi <image-id> (移除构成镜像的一个只读层 也可使用 -f 强制移除中间read only layer)
docker commit <container-id> (把一个 read write layer 转成 read only layer)
docker build (build命令根据Dockerfile文件中的FROM指令获取到镜像，然后重复地1）run（create和start）、2）修改、3）commit。在循环中的每一步都会生成一个新的层，因此许多新的层会被创建。)
docker exec <running-container-id> (容器中新建一个 shell 进程)
docker inspect <container-id> or <image-id> (提取出容器或者镜像最顶层的元数据)
docker save <image-id> (会创建一个镜像的压缩文件)
docker export <container-id> (docker export命令创建一个tar文件，并且移除了元数据和不必要的层，将多个层整合成了一个层. expoxt后的容器再import到Docker中，通过docker images –tree命令只能看到一个镜像；而save后的镜像则不同，它能够看到这个镜像的历史镜像)
```

