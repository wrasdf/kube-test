cfn:
	@docker-compose run --rm ctpl validate -n test-role-for-kube-app -c role
	@docker-compose run --rm ctpl apply -n test-role-for-kube-app -c role

sh-%:
	./bin/sh.sh $(*) onboarding

test-%:
	./bin/test.sh $(*) onboarding

test_in:
	green ./tests/cluster
	green ./tests/system
	green ./tests/kube-e2e
