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

```dockerfile
FROM golang:1.20-alpine3.17 as build
WORKDIR /app-build
COPY . .
RUN go mod tidy && go build -o paymentchannel ./cmd/main.go
# This means that a1 and a2 are executed in separate layers during the build process, resulting in two separate intermediate images. This can lead to a larger final image size, as each intermediate image must be stored in the Docker image cache.

# files created or copied in stage 1 will still exist in stage 2
FROM build 
WORKDIR /app
COPY --from=build /app-build/paymentchannel /app
COPY --from=build /app-build/configs /app/configs
COPY --from=build /app-build/logs /app/logs
RUN rm -rf /app-build
# RUN mkdir /app/logs
ENV GO_ENV=dev


CMD ["./paymentchannel"]
# CMD ["go", "run","/app/cmd/main.go"]
```