# How to start a local Kubernetes cluster

### Table of contents

- [How to start a local Kubernetes cluster?](#how-to-start-a-local-kubernetes-cluster)
- [Installation checks](#installation-checks)
- [Video lesson](#video-lesson)

## How to start a local Kubernetes cluster?

> #### Before you start, check the docker engine is up and running
>
> ```sh
> docker run hello-world
> ```
>
> If you see the message `Hello from Docker!` then you are good to go.
>
> If you see an error, and you have Docker Desktop installed, make sure it is running.

### TLDR

All the steps to create a local Kubernetes cluster are summarized in the `create_cluster.sh` script, that you can run as follows:

```sh
cd deployments/dev/kind # Go to the kind directory
chmod +x create_cluster.sh # Make the script executable
./create_cluster.sh # Run the script
```

What's happening under the hood?

### Create a docker network

```sh
docker network create --subnet 172.100.0.0/16 rwml-34fa-network
```

### Create and start the kind cluster
We use a basic configuration for the kind cluster, with port mapping enabled, in the `kind-with-portmapping.yaml` file.

```sh
KIND_EXPERIMENTAL_DOCKER_NETWORK=rwml-34fa-network kind create cluster --config ./kind-with-portmapping.yaml
```


## Installation checks
From the command line, you can check `kubectl` and `k9s` can talk to your kubernetes clustesr with the following commands:

- Get nodes
    ```sh
    kubectl get nodes -A
    ```
    ```sh
    NAME                      STATUS   ROLES           AGE   VERSION
    rwml-34fa-control-plane   Ready    control-plane   12m   v1.31.4
    ```

- Open the `k9s` dashboard
    ```sh
    k9s
    ```


## Video lesson

[👉 Link to video](https://www.realworldml.net/products/building-a-real-time-ml-system-together-cohort-4/categories/2157289689/posts/2186425761)

