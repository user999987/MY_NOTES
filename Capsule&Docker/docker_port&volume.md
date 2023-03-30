```bash
docker run -p 8080(宿主):80(container) myimage
```

```dockerfile
FROM myimage

# 创建一个数据卷
VOLUME /myvolume

# 指定容器的工作目录
WORKDIR /app

# 将本地的文件复制到容器中
COPY . .

# 暴露端口
EXPOSE 8080

# 启动容器时执行的命令
CMD ["./myapp"]
```
```bash
docker run -v /path/on/host:/myvolume myimage
```
端口和数据卷都是容器相关的东西 dockerfile是镜像 所以在dockerfile中定义不可以

```bash
docker volume create mydata
docker run -v mydata:/path/to/container/dir myimage
```
VOLUME 声明容器挂载的目录，docker volume create 命令创建一个独立于容器的数据卷，两者可以搭配使用。


```bash
docker run -d -p 8686:8686 -v /Users/vvayne/xcloud/paymentchannel/logs:/app/logs --name pc pc
-d 后台运行 第一个8686是宿主机 第二个8686是容器 -v目录挂载  第一个路径宿主机 第二个路径容器 第一个pc是容器名 第二个是镜像名
```