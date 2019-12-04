# This is just a Kubernetes learning project

```
cd project_manifests
kubectl apply -f ./
```

Find out an ingress IP:
 - Minikube:
```
$ minikube addons enable ingress
ingress was successfully enabled

$ kubectl get ingress
NAME                 HOSTS   ADDRESS          PORTS   AGE
apache-php-api       *       192.168.99.106   80      14m
apache-php-related   *       192.168.99.106   80      14m
apache-php-root      *       192.168.99.106   80      14m
apache-php-www       *       192.168.99.106   80      14m
kibana               *       192.168.99.106   80      14m
web-server           *       192.168.99.106   80      14m
```
Open the http://192.168.99.106 link in a browser.

 - Some cloud provider (tested on MCS https://mcs.mail.ru):
```
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/mandatory.yaml
namespace/ingress-nginx created
configmap/nginx-configuration created
configmap/tcp-services created
configmap/udp-services created
serviceaccount/nginx-ingress-serviceaccount created
clusterrole.rbac.authorization.k8s.io/nginx-ingress-clusterrole created
role.rbac.authorization.k8s.io/nginx-ingress-role created
rolebinding.rbac.authorization.k8s.io/nginx-ingress-role-nisa-binding created
clusterrolebinding.rbac.authorization.k8s.io/nginx-ingress-clusterrole-nisa-binding created
deployment.apps/nginx-ingress-controller created

$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/cloud-generic.yaml
service/ingress-nginx created

$ kubectl get svc -A | grep ingress-nginx | grep LoadBalancer
ingress-nginx   ingress-nginx                      LoadBalancer   10.254.58.66     <pending>     80:31818/TCP,443:31932/TCP   58s

$ sleep 30s

$ kubectl get svc -A | grep ingress-nginx | grep LoadBalancer
ingress-nginx   ingress-nginx                      LoadBalancer   10.254.58.66     89.208.221.10   80:31818/TCP,443:31932/TCP   2m29s
```
Open the http://89.208.221.10 link in a browser.

Redis communicator reader/writer logs example (locally):
```
$ MAX_TIME=9 REDIS_HOST=192.168.99.104 REDIS_PORT=30379 APP_ROLE=reader python3 redis_communicator.py
2019-12-02 16:53:38,043 - INFO - Role: reader
2019-12-02 16:53:38,043 - INFO - Max working time: 9
2019-12-02 16:53:38,043 - INFO - Connecting to Redis: 192.168.99.104:30379
2019-12-02 16:53:39,059 - INFO - Got message: {'type': 'psubscribe', 'pattern': None, 'channel': b'*', 'data': 1}
2019-12-02 16:53:42,073 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'__keyspace@0__:mac', 'data': b'set'}
2019-12-02 16:53:42,074 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'__keyevent@0__:set', 'data': b'mac'}
2019-12-02 16:53:42,074 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"mac": "2019-12-02 16:53:41.257012"}'}
2019-12-02 16:53:43,078 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"mac": "2019-12-02 16:53:42.262515"}'}
2019-12-02 16:53:44,083 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"mac": "2019-12-02 16:53:43.270370"}'}
2019-12-02 16:53:44,083 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'__keyspace@0__:mac', 'data': b'set'}
2019-12-02 16:53:44,083 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'__keyevent@0__:set', 'data': b'mac'}
2019-12-02 16:53:44,084 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'__keyspace@0__:mac', 'data': b'del'}
2019-12-02 16:53:44,084 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'__keyevent@0__:del', 'data': b'mac'}
2019-12-02 16:53:47,100 - INFO - Reader completed after '9' seconds
2019-12-02 16:53:47,101 - INFO - Finish

$ MAX_TIME=2 REDIS_HOST=192.168.99.104 REDIS_PORT=30379 APP_ROLE=writer python3 redis_communicator.py
2019-12-02 16:53:41,244 - INFO - Role: writer
2019-12-02 16:53:41,245 - INFO - Max working time: 2
2019-12-02 16:53:41,245 - INFO - Connecting to Redis: 192.168.99.104:30379
2019-12-02 16:53:41,245 - INFO - Set key/value: mac/Up
2019-12-02 16:53:41,257 - INFO - Publish message to 'nodes' channel: {"mac": "2019-12-02 16:53:41.257012"}
2019-12-02 16:53:42,262 - INFO - Publish message to 'nodes' channel: {"mac": "2019-12-02 16:53:42.262515"}
2019-12-02 16:53:43,270 - INFO - Publish message to 'nodes' channel: {"mac": "2019-12-02 16:53:43.270370"}
2019-12-02 16:53:43,275 - INFO - Writer completed after '2' seconds
2019-12-02 16:53:43,275 - INFO - Set key/value: mac/Down
2019-12-02 16:53:43,278 - INFO - Delete key: mac
2019-12-02 16:53:43,281 - INFO - Finish
```

The same, but in Kubernetes (Minikube, 1 worker node):
```
$ kubectl logs communicator-reader-cb7d6766d-rrk8q
2019-12-02 13:02:47,282 - INFO - Role: reader
2019-12-02 13:02:47,283 - INFO - Max working time: 0
2019-12-02 13:02:47,283 - INFO - Connecting to Redis: redis-slave:6379
2019-12-02 13:02:48,374 - INFO - Got message: {'type': 'psubscribe', 'pattern': None, 'channel': b'*', 'data': 1}
2019-12-02 13:02:49,376 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'__keyspace@0__:communicator-writer-w48fg', 'data': b'set'}
2019-12-02 13:02:49,376 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'__keyevent@0__:set', 'data': b'communicator-writer-w48fg'}
2019-12-02 13:02:49,376 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-w48fg": "2019-12-02 13:02:48.922594"}'}
2019-12-02 13:02:50,377 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-w48fg": "2019-12-02 13:02:49.926337"}'}
2019-12-02 13:02:51,380 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-w48fg": "2019-12-02 13:02:50.929149"}'}
2019-12-02 13:02:52,382 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-w48fg": "2019-12-02 13:02:51.931579"}'}
...

$ kubectl logs communicator-writer-w48fg
2019-12-02 13:02:48,916 - INFO - Role: writer
2019-12-02 13:02:48,916 - INFO - Max working time: 0
2019-12-02 13:02:48,916 - INFO - Connecting to Redis: redis-master:6379
2019-12-02 13:02:48,916 - INFO - Set key/value: communicator-writer-w48fg/Up
2019-12-02 13:02:48,922 - INFO - Publish message to 'nodes' channel: {"communicator-writer-w48fg": "2019-12-02 13:02:48.922594"}
2019-12-02 13:02:49,926 - INFO - Publish message to 'nodes' channel: {"communicator-writer-w48fg": "2019-12-02 13:02:49.926337"}
2019-12-02 13:02:50,929 - INFO - Publish message to 'nodes' channel: {"communicator-writer-w48fg": "2019-12-02 13:02:50.929149"}
2019-12-02 13:02:51,931 - INFO - Publish message to 'nodes' channel: {"communicator-writer-w48fg": "2019-12-02 13:02:51.931579"}
...
```

Kubernetes (MCS, 2 worker nodes):
```
$ kubectl get nodes
NAME                                      STATUS   ROLES    AGE     VERSION
kubernetes-cluster-3151-default-group-0   Ready    <none>   5m19s   v1.15.3
kubernetes-cluster-3151-default-group-1   Ready    <none>   5m42s   v1.15.3
kubernetes-cluster-3151-master-0          Ready    master   8m34s   v1.15.3

$ kubectl get pods
NAME                                  READY   STATUS    RESTARTS   AGE
apache-php-5499dddcc6-5276b           1/1     Running   0          6m23s
communicator-reader-8f88fddf6-vdn29   1/1     Running   1          6m22s
communicator-writer-4zqft             1/1     Running   0          6m23s
communicator-writer-mlj5w             1/1     Running   1          6m23s
elasticsearch-0                       1/1     Running   0          6m22s
elasticsearch-1                       1/1     Running   0          6m22s
elasticsearch-2                       1/1     Running   0          6m22s
kibana-7868d89fc4-8ctnf               1/1     Running   0          6m22s
redis-master-986cfd7f8-25t98          1/1     Running   0          6m21s
redis-slave-7794cd69d8-8schw          1/1     Running   0          6m20s
redis-slave-7794cd69d8-l7kw4          1/1     Running   0          6m20s
web-server-f5f685dd8-p5gkz            1/1     Running   0          6m19s

$ kubectl logs -f communicator-reader-8f88fddf6-vdn29
2019-12-04 11:56:25,561 - INFO - Role: reader
2019-12-04 11:56:25,563 - INFO - Max working time: 0
2019-12-04 11:56:25,565 - INFO - Connecting to Redis: redis-slave:6379
2019-12-04 11:56:26,594 - INFO - Got message: {'type': 'psubscribe', 'pattern': None, 'channel': b'*', 'data': 1}
2019-12-04 11:56:26,596 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-mlj5w": "2019-12-04 11:56:25.966882"}'}
2019-12-04 11:56:26,598 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-4zqft": "2019-12-04 11:56:26.390189"}'}
2019-12-04 11:56:27,600 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-mlj5w": "2019-12-04 11:56:26.978571"}'}
2019-12-04 11:56:27,603 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-4zqft": "2019-12-04 11:56:27.402190"}'}
2019-12-04 11:56:28,606 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-mlj5w": "2019-12-04 11:56:27.983834"}'}
2019-12-04 11:56:28,606 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-4zqft": "2019-12-04 11:56:28.408106"}'}
2019-12-04 11:56:29,615 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-mlj5w": "2019-12-04 11:56:28.994569"}'}
2019-12-04 11:56:29,618 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-4zqft": "2019-12-04 11:56:29.415702"}'}
2019-12-04 11:56:30,621 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-mlj5w": "2019-12-04 11:56:29.999658"}'}
2019-12-04 11:56:30,622 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-4zqft": "2019-12-04 11:56:30.422066"}'}
2019-12-04 11:56:31,622 - INFO - Got message: {'type': 'pmessage', 'pattern': b'*', 'channel': b'nodes', 'data': b'{"communicator-writer-mlj5w": "2019-12-04 11:56:31.003537"}'}
...

$ kubectl logs -f communicator-writer-4zqft
2019-12-04 11:54:27,397 - INFO - Role: writer
2019-12-04 11:54:27,397 - INFO - Max working time: 0
2019-12-04 11:54:27,397 - INFO - Connecting to Redis: redis-master:6379
2019-12-04 11:54:27,398 - INFO - Set key/value: communicator-writer-4zqft/Up
2019-12-04 11:54:27,414 - INFO - Publish message to 'nodes' channel: {"communicator-writer-4zqft": "2019-12-04 11:54:27.414783"}
2019-12-04 11:54:28,418 - INFO - Publish message to 'nodes' channel: {"communicator-writer-4zqft": "2019-12-04 11:54:28.417014"}
2019-12-04 11:54:29,423 - INFO - Publish message to 'nodes' channel: {"communicator-writer-4zqft": "2019-12-04 11:54:29.423111"}
2019-12-04 11:54:30,426 - INFO - Publish message to 'nodes' channel: {"communicator-writer-4zqft": "2019-12-04 11:54:30.426091"}
2019-12-04 11:54:31,432 - INFO - Publish message to 'nodes' channel: {"communicator-writer-4zqft": "2019-12-04 11:54:31.432074"}
2019-12-04 11:54:32,434 - INFO - Publish message to 'nodes' channel: {"communicator-writer-4zqft": "2019-12-04 11:54:32.434407"}
2019-12-04 11:54:33,436 - INFO - Publish message to 'nodes' channel: {"communicator-writer-4zqft": "2019-12-04 11:54:33.436297"}
2019-12-04 11:54:34,439 - INFO - Publish message to 'nodes' channel: {"communicator-writer-4zqft": "2019-12-04 11:54:34.439084"}
2019-12-04 11:54:35,441 - INFO - Publish message to 'nodes' channel: {"communicator-writer-4zqft": "2019-12-04 11:54:35.441071"}
2019-12-04 11:54:36,443 - INFO - Publish message to 'nodes' channel: {"communicator-writer-4zqft": "2019-12-04 11:54:36.443264"}
...

$ kubectl logs -f communicator-writer-mlj5w
2019-12-04 11:56:23,914 - INFO - Role: writer
2019-12-04 11:56:23,916 - INFO - Max working time: 0
2019-12-04 11:56:23,916 - INFO - Connecting to Redis: redis-master:6379
2019-12-04 11:56:23,917 - INFO - Set key/value: communicator-writer-mlj5w/Up
2019-12-04 11:56:23,958 - INFO - Publish message to 'nodes' channel: {"communicator-writer-mlj5w": "2019-12-04 11:56:23.958644"}
2019-12-04 11:56:24,963 - INFO - Publish message to 'nodes' channel: {"communicator-writer-mlj5w": "2019-12-04 11:56:24.963232"}
2019-12-04 11:56:25,969 - INFO - Publish message to 'nodes' channel: {"communicator-writer-mlj5w": "2019-12-04 11:56:25.966882"}
2019-12-04 11:56:26,978 - INFO - Publish message to 'nodes' channel: {"communicator-writer-mlj5w": "2019-12-04 11:56:26.978571"}
2019-12-04 11:56:27,986 - INFO - Publish message to 'nodes' channel: {"communicator-writer-mlj5w": "2019-12-04 11:56:27.983834"}
2019-12-04 11:56:28,994 - INFO - Publish message to 'nodes' channel: {"communicator-writer-mlj5w": "2019-12-04 11:56:28.994569"}
2019-12-04 11:56:29,999 - INFO - Publish message to 'nodes' channel: {"communicator-writer-mlj5w": "2019-12-04 11:56:29.999658"}
2019-12-04 11:56:31,003 - INFO - Publish message to 'nodes' channel: {"communicator-writer-mlj5w": "2019-12-04 11:56:31.003537"}
2019-12-04 11:56:32,006 - INFO - Publish message to 'nodes' channel: {"communicator-writer-mlj5w": "2019-12-04 11:56:32.005897"}
...
```
---
\
\
Good luck!  
Alexey Tsarev, Tsarev.Alexey at gmail.com
