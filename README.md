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

The same, but in Kubernetes:
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


---
Good luck!  
Alexey Tsarev, Tsarev.Alexey at gmail.com
