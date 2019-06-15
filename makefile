
build:
	docker build -t kube-test:latest .

sh: build
	docker run --rm -it -v $(HOME)/.aws:/root/.aws -v $(HOME)/.kube:/root/.kube -v $$(pwd):/app kube-test:latest /bin/sh

test: build
	docker run --rm -w /app -v $(HOME)/.aws:/root/.aws -v $(HOME)/.kube:/root/.kube -v $$(pwd):/app kube-test:latest make test_in

test_in:
	green ./tests/cluster
	green ./tests/kube-system
	green ./tests/kube-e2e
