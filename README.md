# Setting up the system

### Por Forwarding
```kubectl port-forward -n istio-system svc/istio-ingressgateway 31380:80```

### Enabling Docker Registry
```
cd ../../docker-registry
docker-compose up
```


