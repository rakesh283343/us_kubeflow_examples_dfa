### Pushing the docker registry to Docker Registry

```
docker build -t examples-word-count . --no-cache
docker tag examples-word-count localhost:5005/examples-word-count
docker push localhost:5005/examples-word-count
```
