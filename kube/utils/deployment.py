import os
import importlib
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(
    current_dir, "./config_manager.py")).load_module()
from config_manager import ConfigManager

# example of params:
# {
#     'name': 'test-deployment',
#     'namespace': 'platform-enablement',
#     'replicas': 2,
#     'version: v0.1.6',
#     'container': 'ikerry/metrics-node',
#     'container_port': '8080',
#     'dns_name': 'nodet.svc.platform.myobdev.com',
#     'developmentAnnotatins': {
#          "sidecar.istio.io/inject": "true"
#      },
#     'specAnnotaions': : {
#          "iam.amazonaws.com/role": "arn:aws:iam::<id>:role/k8s/<your-iam-role>"
#      },
# }

class DeploymentManager:

    def __init__(self):
        ConfigManager()
        self.appApi = client.AppsV1Api()

    def list(self, namespace):
        return list(map(lambda x: x.metadata.name, self.appApi.list_namespaced_deployment(namespace).items))

    def apply(self, path):
        utils.create_from_yaml(k8s_client, path)

    def delete(self, name, namespace):
        # No deployment
        if name not in self.list_namespaced_deployments(namespace):
            print("No deployment resource {0} in namespace {1}".format(name, namespace))
            return True

        try:
            return self.appApi.delete_namespaced_deployment(name, namespace)
        except ApiException as e:
            print("Exception when calling AppsV1Api -> delete_namespaced_deployment: %s\n" % e)
