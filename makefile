
build:
	docker build -t kube-test:latest .

sh: build
	docker run --rm -it -v $(HOME)/.aws:/root/.aws -v $(HOME)/.kube:/root/.kube -v $$(pwd):/app kube-test:latest /bin/sh

test: build
	docker run --rm -w /app -v $(HOME)/.aws:/root/.aws -v $(HOME)/.kube:/root/.kube -v $$(pwd):/app kube-test:latest green ./tests

test_in:
	green ./tests
