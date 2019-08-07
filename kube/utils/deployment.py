import os
import importlib
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "./config_manager.py")).load_module()
importlib.machinery.SourceFileLoader("exec", os.path.join(current_dir, "./exec.py")).load_module()
from config_manager import ConfigManager
from exec import EXEC


class DeploymentManager:

    def __init__(self):
        ConfigManager()
        self.exec = EXEC()
        self.appApi = client.AppsV1Api()

    def list(self, namespace):
        return list(map(lambda x: x.metadata.name, self.appApi.list_namespaced_deployment(namespace).items))

    def apply(self, path):
        self.exec.sh(f'kubectl apply -f {path}')

    def delete(self, name, namespace):
        # No deployment
        if name not in self.list_namespaced_deployments(namespace):
            print("No deployment resource {0} in namespace {1}".format(name, namespace))
            return True

        try:
            return self.appApi.delete_namespaced_deployment(name, namespace)
        except ApiException as e:
            print("Exception when calling AppsV1Api -> delete_namespaced_deployment: %s\n" % e)
