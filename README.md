### Goal of this repo

- Check if all the pods are running in namespace
- Detect the existence of any Crash Loops
- Look at the health of the various Master Components
  - Scheduler
  - Controller
  - Kubelet
  - Kube-Proxy
  - Pods

### ToDo scenario:

- Verify simple app deploy successful
  - Deploy a pod with ingress
  - The cert-manager could generate cert for app
  - The url works
  - TTL secrets generate

- Verify kube2iam works
  - Deploy a pod with IAM role,
  - The pod could put data into s3 bucket

### How to debug and run in container

- $ make sh

### How to run the tests

- $ make test
