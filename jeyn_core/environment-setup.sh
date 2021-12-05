#!/usr/bin/env bash

echo "Initializing Dapr..."
dapr status -k &>/dev/null
if [ $? -eq 0 ]; then
  echo "Dapr already running"
else
  echo "Dapr not running. Starting Dapr system..."
  dapr init -k
fi

echo "Initializing Argo..."
kubectl create namespace argo &>/dev/null
kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo-workflows/master/manifests/quick-start-postgres.yaml

echo "Initializing redis..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install --namespace "dapr-system" redis bitnami/redis

echo "Installing jeyn core systems..."
helm upgrade --install jeyn-core ./jeyn_core_charts --set redis.auth.password==$(kubectl get secret --namespace "dapr-system" jeyn-core-redis -o jsonpath="{.data.redis-password}" | base64 --decode)

