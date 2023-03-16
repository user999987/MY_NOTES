# CA证书
CA = certificate authority\
CA是专门签发证书的权威机构，处于证书的最顶端。自签是用自己的私钥给证书签名，CA签发则是用CA的私钥给自己的证书签名来保证证书的可靠性
## 自签名
### 常规情况
1. 生成私钥
    ```bash
    openssl genrsa -out ca.key 2048 #(by default 512)
    ```
2. 生成证书请求
    ```bash
    openssl req -new -key ca.key -out ca.csr
    ```
3. 自签名
    ```bash
    openssl x509 -req -days 3650 -in ca.csr -signkey ca.key -out ca.crt
    ```
### 3合1
以上3个命令可以合并如下:
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ca.key -out ca.crt
```
这种情况并不知道 private key....

### 正常情况合并
```bash
openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 3650 -key ca.key -out ca.crt -subj "/C=CN/ST=mykey/L=mykey/O=mykey/OU=mykey/CN=domain1/CN=domain2/CN=domain3"
```
可以从 crt 中提取 pubkey
```bash
openssl x509 -in ca.crt -pubkey -noout > ca.pem
```
查看自签名CA证书：openssl x509 -text -in ca.crt

## 颁发CA
颁发证书就是用CA的秘钥给其他人签名证书，输入需要证书请求，CA的私钥及CA的证书，输出的是签名好的还给用户的证书.
用户的证书请求信息填写的国家省份等需要与CA配置一致，否则颁发的证书将会无效。

用户证书的生成步骤

生成私钥（.key）-->生成证书请求（.csr）-->CA的私钥及CA的证书签名得到用户证书（.crt）

1. 生成密钥： openssl genrsa -out client.key 2048
2. 生成请求: openssl req -new -subj -key client.key -out client.csr
3. 签发证书: openssl x509 -req -days 3650 -sha1 -extensions v3_req -CA ca.cert -CAkey ca.key -CAserial ca.srl -CAcreateserial -in client.csr -out client.cert
```
req          产生证书签发申请命令
-new         表示新请求。
-key         密钥,这里为client.key文件
-out         输出路径,这里为client.csr文件
-subj        指定用户信息

x509           签发X.509格式证书命令。
-req            表示证书输入请求。
-days          表示有效天数,这里为3650天。
-sha1           表示证书摘要算法,这里为SHA1算法。
-extensions    表示按OpenSSL配置文件v3_req项添加扩展
-CA            表示CA证书,这里为ca.cert
-CAkey         表示CA证书密钥,这里为ca.key
-CAserial      表示CA证书序列号文件,这里为ca.srl
-CAcreateserial表示创建CA证书序列号
-in            表示输入文件,这里为private/server.csr
-out           表示输出文件,这里为certs/server.cer
```

* 验证CA颁发的证书提取的公钥和私钥导出的公钥是否一致 openssl x509 -in server.cert -pubkey
* 验证server证书openssl verify -CAfile ca.cert server.cert
* 生成pem格式证书有时需要用到pem格式的证书，可以用以下方式合并证书文件（crt）和私钥文件（key）来生成 cat client.crt client.key > client.pem
