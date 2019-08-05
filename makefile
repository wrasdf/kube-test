# App
build-node:
	cd ./app && docker build -t kube-app:latest .

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

# CFN
cfn:
	@docker-compose run --rm stackup test-role-for-kube-app up -t cfns/template.yaml

# python test
build:
	@docker build -t kube-test:latest .

sh-%:
	./bin/compile.sh $(*) onboarding
	@docker-compose build sh
	@docker-compose run sh

%-europa-stg: dns_name := kube-app.svc.europa-stg.jupiter.myobdev.com
%-dev-green: dns_name := kube-app.svc.dev-green.k8s.platform.myobdev.com

test-%:
	./bin/e2e_test.sh $(*) onboarding $(dns_name)

test_in:
	green ./tests/cluster
	green ./tests/kube-system
	green ./tests/kube-e2e
