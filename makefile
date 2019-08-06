cfn:
	@docker-compose run --rm ctpl validate -n test-role-for-kube-app -c role
	@docker-compose run --rm ctpl apply -n test-role-for-kube-app -c role

sh-%:
	@docker-compose build sh
	@docker-compose run sh

test-%:
	./bin/e2e_test.sh $(*) onboarding

test_in:
	green ./tests/cluster
	green ./tests/system
	green ./tests/kube-e2e
