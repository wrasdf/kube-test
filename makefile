# App
build-node:
	cd ./app && docker build -t kube-test:latest .

stop:
	@docker stop $(shell docker ps -qa)

run-node: stop
	@docker-compose build node
	@docker-compose run --rm -d -p 8080:8080 node

sh-node: stop
	@docker-compose build sh-node
	@docker-compose run sh-node

push-node-%: build-node
	@docker tag kube-app:latest ikerry/kube-app:$(*)
	@docker push ikerry/kube-app:$(*)


# python test
build:
	@docker build -t kube-test:latest .

sh:
	@docker-compose build sh
	@docker-compose run sh

test:
	@docker-compose build pytest
	@docker-compose run --rm pytest

test_in:
	green ./tests/cluster
	green ./tests/kube-system
	# green ./tests/kube-e2e
