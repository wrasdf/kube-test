import os
import importlib
from kubernetes import client, config
from kubernetes.client.rest import ApiException

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "./config_manager.py")).load_module()
from config_manager import ConfigManager

class IngressManager:

    def __init__(self):
        ConfigManager()
        self.extensionApi = client.ExtensionsV1beta1Api()

    def list(self, namespace):
        return list(map(lambda x: x.metadata.name, self.extensionApi.list_namespaced_ingress(namespace).items))

    def apply(self, path):
        utils.create_from_yaml(k8s_client, path)

    def delete(self, name, namespace):
        # No ingress
        if name not in self.list_namespaced_ingress(namespace):
            print("No ingress resource {0} in namespace {1}".format(name, namespace))
            return True

        try:
            self.extensionApi.delete_namespaced_ingress(
                name,
                namespace
            )
        except ApiException as e:
            print(
                "Exception when calling ExtensionsV1beta1Api->delete_namespaced_ingress: %s\n" % e)
