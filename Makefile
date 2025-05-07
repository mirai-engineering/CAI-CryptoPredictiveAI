################################################################################
## Development
################################################################################

# Runs the trades service as a standalone Pyton app (not Dockerized)
dev:
	uv run services/${service}/src/${service}/main.py

# Builds a docker image from a given Dockerfile
#build-for-dev:
#	docker build -t ${service}:dev -f docker/${service}.Dockerfile .

build-for-dev:
	docker build \
		--build-arg SERVICE_NAME=${service} \
		-t ${service}:dev \
		-f docker/${service}.Dockerfile .

# Push the docker image to the docker registry of our kind cluster
push-for-dev:
	kind load docker-image ${service}:dev --name rwml-34fa

# Deploys the docker image to the kind cluster
deploy-for-dev: build-for-dev push-for-dev
	kubectl delete -f deployments/dev/${service}/${service}.yaml --ignore-not-found=true
	kubectl apply -f deployments/dev/${service}/${service}.yaml

# workaround for technical_indicators.yaml
#deploy-for-dev_ti: build-for-dev push-for-dev
#	kubectl delete -f deployments/dev/${service}/technical-indicators.yaml --ignore-not-found=true
#	kubectl apply -f deployments/dev/${service}/technical-indicators.yaml
################################################################################
## Production
################################################################################
build-and-push-for-prod:
	export BUILD_DATE=$(date +%s) && \
	docker buildx build --push --platform linux/amd64,linux/arm64 -t ghcr.io/brunoclbr/${service}:0.1.5-beta.${BUILD_DATE} -f docker/${service}.Dockerfile .

deploy-for-prod:
	kubectl delete -f deployments/prod/${service}/${service}.yaml --ignore-not-found=true
	kubectl apply -f deployments/prod/${service}/${service}.yaml

lint:
	ruff check . --fix