cfn:
	@docker-compose run --rm ctpl validate -n test-role-for-kube-app -c role
	@docker-compose run --rm ctpl apply -n test-role-for-kube-app -c role

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
