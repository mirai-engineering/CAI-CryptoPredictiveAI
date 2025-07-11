#!/bin/bash

echo "If you didn't create the mlflow database with the credentials, this script will fail"

kubectl create namespace mlflow
kubectl apply --recursive -f manifests/mlflow-minio-secret.yaml
helm upgrade --install --create-namespace --wait mlflow oci://registry-1.docker.io/bitnamicharts/mlflow --namespace=mlflow --values manifests/mlflow-values.yaml


