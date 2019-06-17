# App
build-node:
	@docker build -t kube-app:latest -f Dockerfile_Node .

run-node: build-node
	@docker run --rm -d \
	 	-p 8080:8080 \
	  -v $(HOME)/.aws:/root/.aws \
    kube-app:latest

sh-node: build-node
	@docker run --rm -it \
		-p 8080:8080 \
		-v $(HOME)/.aws:/root/.aws \
		-v app:/app \
		-v app/node_modules:/app/node_modules \
		--entrypoint "sh" \
		kube-app:latest

push-node-%: build-node
	@docker tag kube-app:latest ikerry/kube-app:$(*)
	@docker push ikerry/kube-app:$(*)

# python test
build:
	@docker build -t kube-test:latest .

sh: build
	@docker run --rm -it -v $(HOME)/.aws:/root/.aws -v $(HOME)/.kube:/root/.kube -v $$(pwd):/app kube-test:latest /bin/sh

test: build
	@docker run --rm -w /app -v $(HOME)/.aws:/root/.aws -v $(HOME)/.kube:/root/.kube -v $$(pwd):/app kube-test:latest make test_in

test_in:
	green ./tests/cluster
	green ./tests/kube-system
	# green ./tests/kube-e2e
