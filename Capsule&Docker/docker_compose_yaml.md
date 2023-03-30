```yaml
development: &default
  adapter: postgresql
  database: dev_development

test: &test
  <<: *default
  database: test_test
```
& marks an alias for the node, for above example &default aliases the development node as "default"and the * references the aliased node with the name "default". The <<: inserts the content of that node.

就是把 development 起个别名然后放在 test 下面 database 之前

The Compose file is a YAML file defining services, networks and volumes. The default path for a Compose file is ./docker-compose.yml<br>
A service definition contains configuration that is applied to each container started for that service, much like passing command-line parameters to docker run. Likewise, network and volume definitions are analogous to docker network create and docker volume create.

```yaml
version: "3.9"
services:
  webapp:
    build: ./dir
# 一般性 直接在当前目录找 dockerfile 开始 build

version: "3.9"
services:
  webapp:
    build:
      context: ./dir # Either a path to a directory containing a Dockerfile, or a url to a git repository.
      dockerfile: Dockerfile-alternate # Alternate Dockerfile
      args: # Add build arguments, which are environment variables accessible only during the build process.
        buildno: 1 # dockerfile 中 需要 定义 ARG buildno and then use it RUN echo "$buildno"
    #   args:
    #     - buildno=1
    # 第一种形式 mapping 第二种是list
```

Docker for Mac用于 osxfs 将从 macOS 共享的目录和文件传播到 Linux VM。这种传播使这些目录和文件可用于在 Docker for Mac 上运行的 Docker 容器。

默认情况下，这些共享是完全一致的，这意味着每次在 macOS 主机上发生写入或通过容器中的挂载时，都会将更改刷新到磁盘，以便共享中的所有参与者都具有完全一致的视图。在某些情况下，完全一致可能会严重影响性能。Docker 17.05 和更高版本引入了选项来调整一个一个，每个容器的一致性设置。以下选项可用：

consistent 或者 default：完全一致的默认设置，如上所述。
delegated：容器运行时的挂载视图是权威的。在容器中进行的更新可能在主机上可见之前可能会有延迟。
cached：macOS主机的挂载视图是权威的。在主机上进行的更新在容器中可见之前可能会有延迟。
这些选项在除 macOS 以外的所有主机操作系统上完全忽略。

```yaml
volumes:
    - './insula:/app/insula:cached'
    - $HOME/.aws:/home/pyapp/.aws
# above is short syntax volumes:
# [SOURCE:]TARGET[:MODE]
```

典型做法 COPY . /app/ #把整个当前文件夹拷贝到镜像 同时 当前文件夹有一个 dockerignore 文件会无视当中列出的文件<br>
然后用上面的 './insula:/app/insula:cached' 让src挂在本地磁盘 当有更新时running container会自动更新