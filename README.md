# ICN-Stage

ICN-stage é um arcabouço para orquestração de avaliações experimentais ICN reprodutiveis e tolerantes a falhas.

# Baixar
```sh
git clone https://github.com/RafaelDBeltran/ICN-Stage_WPEIF-2022.git
```
    
# Instalar
- [Minikube](https://github.com/kubernetes/minikube)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- [Python3](https://python.org.br/instalacao-linux/)

(Zookeeper não é necessário pois é instalado e configurado automaticamente)
## Install Host Requirements
```sh
pip install -r requirements.txt
```

# Deploy
0. Executar o minikube (ou configurar acesso a uma infraestrutura Kubernetes)
```sh
minikube start
```

# Reproduzir experimentos do artigo
```sh
python3 play_ndn.py
```

# Executar novos experimentos

1. Configurar o ambiente Kubernetes
```sh
python3 setup_kubernets.py
```

1.1 Opções para Deploy do Ambiente

- -d: Número de diretores. default: 1
- -a: Número de atores. default: 1


2. Acessar algum diretor
```sh
kubectl exec --stdin --tty director1 -- /bin/bash
```

3. Executar a interface por linha de comando do icn-stage
```sh
python3 icn-stage/cli.py
```
    
## Comandos do ICN-stage 
Listar comandos
```sh
icn-stage>> help
```
Adicionar atores
```sh
icn-stage>> addactors
```
Lista árvore do zookeeper
```sh
icn-stage>> print
```
### Experimento
Realizar teste com cliente-servidor TCP
Peça TCP
```sh
icn-stage>> tcp
```
Realizar teste com NDN peek e poke
Peça NDN
```sh
icn-stage>> ndn
```
Realizar avaliação com produtor e consumidor de trafego NDN
Peça NDN
```sh
icn-stage>> traffic
```


# Parar

Para parar todos os pods, execute:
```sh
kubectl delete pod --all
```

Desligar o minikube
```sh
minikube stop
```

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
