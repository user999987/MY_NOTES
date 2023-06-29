1. fix the version
```dockerfile
FROM node:17.0.1
```
2. leaner and smaller OS distro 
reduce the image size and security issue
3. optimize caching image layers
each command will add a new layer, sometimes switch the command, you will boost the build speed
```dockerfile
COPY package.json package-lock.json .
RUN npm install --production
COPY myapp /app
```
When you update the code, layer package.json and npm install will reuse the from the cache. Order Dockerfile commands from least to most frequently changing, take advantage of caching. You will get faster image building and fetching.
4. use .dockerignore file
5. make usage of multi-stage builds
like you have build stage and run stage for Golang project. 
6. use the least privileged user
```dockerfile
RUN groupadd -r tom && useradd -g tom tom 
RUN chown -R tom:tom /app
USER tom
CMD node index.js
```
7. scan your images for vulnerabilities
```bash
docker scout cves image-name
``` 