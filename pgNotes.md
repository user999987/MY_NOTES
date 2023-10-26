## Project Code Structure
项目目录结构参考: https://github.com/golang-standards/project-layout/blob/master/README_zh.md

程序整体分两块:
1. 请求进来之前
    *  router 注册路径 并分配处理函数(处理函数由controller实现)
    *  controller结构体包含3个field 分别为 payin/payout/credit_card services. 每个services为一个 map, key是provider id or bank channel, value为对应service的对象. 每个service对象是一个接口定义了需要实现的方法. 在new controller的时候, 注册所有渠道到对应的map中. 
    *   注册的渠道对象通过new service实现, new service的时候也会new一个相应的client, client包含所有该渠道需要的一系列配置和参数.
    *   至此注册完成
2. 请求进来之后
    *   找到对应处理函数 函数中会根据provider id或者bank channel获取对应的服务, 因为该服务已实现了接口定义的所有方法, 所以可以放心调用相应方法. 
    *   相应方法均表示为一个business logic, 如果实现这个业务逻辑需要多个步骤, 则具体步骤写入 相应client并实现. 然后组装成 类似 client.step1 client.step2 client.step3 然后做出相应处理并返回
## Docker operation
```
docker build --platform linux/amd64 -t cc:amd .
docker build --platform linux/arm64 -t cc:arm .
// cc.tar is target name
// cc:latest is source name
docker save -o cc.tar cc:latest                                    
docker load -i cc.tar
```

## ENV
```
ENV=dev
PAYOUT_APP_ID=xxx
PAYOUT_APP_KEY=xxxx
LUCKY_KEY=1234567890123456
RDS_HOST=localhost
RDS_PASSWORD=xxxxxx
RDS_USERNAME=bankapi
REDIS_HOST=127.0.0.1

```

## Add a new Channel
1. Go to internal/common/in (or out ) to add your channel name
2. Go to internal/controller/transaction, follow the existing pattern to register your channel to corresponding service (you will see a lot of warnings from your IDE, just ignore them for now)
3. Go to internal/channels, create a new folder XXX, then 2 sub-folders: client and service. Service is responsible for processing business logic. Client is responsible for interacting with Channels' endpoints.
4. Under the service folder, usually you will have 3 files: 
    * payin: responsible for payin business logic
    * payout: responsible for payout business logic
    * service: responsible for some common definition and service initialization. You can implement NewPayinService and NewPayoutService here
5. Under the client folder, usually you will have 4 files:
    * payin: interact with channel endpoints about payin service
    * payout: interact with channel endpoints about payout service
    * channelname.go: this file will include some client level definitions and payin/payout client initialization (Attention: payin/payout client is a Singleton instance that stores all related config info like key, secret, api url etc. )
    * channlename.pb.go: protobuff generated file. it defines all the structs that you need when interact with channels' endpoints