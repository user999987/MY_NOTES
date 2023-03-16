docker file - build image
```
From xxx as newxxx
WORKDIR path/to/workdir
COPY 
RUN java etc
FROM xxx as nnewxxx
ARG if neceessary
LABEL equivalent to add nick name
USER if necessary
ENV 
WORKDIR
COPY --from=newxx path/to/workdir(old) ./(new)
COPY path/file(folder) newpath/file(folder)

ENTRYPOINT ["command","para1","para2"]
```


docker compose - config ports, dependency relationship, healthcheck, env virable

helm chars deploy the k8s





```typescript
import * as md5 from 'md5';

function bytesToHex(bytes: any) {
    for (var hex = [], i = 0; i < bytes.length; i++) {
      hex.push((bytes[i] >>> 4).toString(16));
      hex.push((bytes[i] & 0xF).toString(16));
    }
    return hex.join('');
  }

function stringToBytes(str: string) {
    str = unescape(encodeURIComponent(str)); // UTF8 escape

    const bytes = [];

    for (let i = 0; i < str.length; ++i) {
        bytes.push(str.charCodeAt(i));
    }

    return bytes;
}

function generateSku(value: string) {
    // string to bytes
    const bytes = stringToBytes(value);
    // hash the value
    var hashed = md5(bytes, { asBytes: true });
    // bit operation, operation is from uuid package
    hashed[6] = hashed[6] & 0x0f | 0x30;
    hashed[8] = hashed[8] & 0x3f | 0x80;

    const hexResult = bytesToHex(hashed);
    const result = `${hexResult.slice(0, 8)}-${hexResult.slice(8, 12)}-${hexResult.slice(12, 16)}-${hexResult.slice(16, 20)}-${hexResult.slice(20)}`;

    return result

}
const value='ndccode-RX-facode'
const sku=generateSku(value)
console.log(sku=="f269d2ec-ff47-37b3-b14f-c7217ca0c40f")
```