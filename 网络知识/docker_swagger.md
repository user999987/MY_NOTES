docker run -p 8080:8080 -e SWAGGER_JSON=/foo/Sypi-Swagger-Spec.json -v /Users/waynewu/Desktop/:/foo swaggerapi/swagger-ui

-v 把 path1  (本机) 挂载到 docker中 path2 
SWAGGER_JSON 中 路径为 path2