import os
import importlib
from kubernetes import client, config
from kubernetes.client.rest import ApiException

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "./config_manager.py")).load_module()
from config_manager import ConfigManager

class ServiceManager:

    def __init__(self):
        ConfigManager()
        self.coreApi = client.CoreV1Api()

    def list(self, namespace):
        return list(map(lambda x: x.metadata.name, self.coreApi.list_namespaced_service(namespace).items))

    def apply(self, path):
        utils.create_from_yaml(k8s_client, path)

    def delete(self, name, namespace):
        # No service
        if name not in self.list_namespaced_service(namespace):
            print("No service resource {0} in namespace {1}".format(name, namespace))
            return True
        return self.coreApi.delete_namespaced_service(name, namespace)
