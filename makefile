
build:
	docker build -t kube-test:latest .

sh: build
	docker run --rm -it -v $(HOME)/.aws:/root/.aws -v $(HOME)/.kube:/root/.kube kube-test:latest /bin/sh
