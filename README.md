### Goal of this repo

- Test kube-system namespace
  - Check the pods are running
  - Detect the existence of any Crash Loops

- Test the health of the various Master Components
  - kube-scheduler
  - kube-controller-manager
  - kube-proxy
  - coredns

- E2E tests
  - Simple app works with cert-manager
  - Kiam functionality

### E2E Test Scenario:

- Verify simple app works with cert-manager
  - deploy 1 simple app
    - 1 deployment
    - 1 ingress with TLS enabled
    - 1 service
  - curl https with endpoints
  - Then
      - teardown apps

- Verify Kiam works
  - Deploy a pod with IAM role
  - The pod could put data into s3 bucket
  - Use AWS SDK check s3 bucket content
  - Then
    - teardown the app
    - delete s3 bucket

### ToDo scenario:

- Verify SQS operator works
  - Apply crd in our cluster
  - app could send message to SQS
  - app could read message from SQS    
  - Then
    - Teardwon the app

- Verify Postgres operator works
  - Apply crd in our cluster
  - wait create the rds in AWS
  - app connect to rds with secret
  - Then
    - teardwon the app    
    - Delete the rds instance

- Verify Istio app ??(Maybe we should trust the istio)
  - deploy 2 simple app without sidecar
  - deploy 2 simple app with sidecar
  - test endpoints work with TLS
  - test services level communication works
    - with sidecar could talk to with sidecar
    - with sidecar could talk to without sidecar
    - without sidecar could talk to with sidecar
    - without sidecar could talk to without sidecar
  - Then
      - teardown apps

### How to run the kube tests for different envs

- $ make test-europa-stg
- $ make test-dev-green

### How to debug and run in container

- $ make sh
