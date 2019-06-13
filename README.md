### Goal of this repo

- Test kube-system namespace
  - Check the pods are running
  - Detect the existence of any Crash Loops

- Test the health of the various Master Components
  - kube-scheduler
  - kube-controller-manager
  - kube-proxy
  - coredns  

- E2E Cluster tests
  - istio app in cluster
  - kiam functionality
  - operators tests (?)

### ToDo scenario:

- Verify Istio app
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

- Verify Kiam works
  - Deploy a pod with IAM role
  - The pod could put data into s3 bucket
  - Use AWS SDK check s3 bucket content
  - Then
    - teardown the app

### How to run the tests

- $ make test

### How to debug and run in container

- $ make sh
