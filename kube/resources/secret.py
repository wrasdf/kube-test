import os
import importlib
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kube.utils.kube_manager import KubeManager


class SecretManager:

    def __init__(self):
        ConfigManager()
        self.exec = EXEC()
        self.coreApi = client.CoreV1Api()

    def list(self, namespace):
        return list(map(lambda x: x.metadata.name, self.coreApi.list_namespaced_secret(namespace).items))

    def read(self, name, namespace):
        return self.coreApi.read_namespaced_secret(name, namespace)

    def delete(self, name, namespace):
        if name not in self.list_namespaced_secret(namespace):
            print("No secret resource {0} in namespace {1}".format(name, namespace))
            return True
        return self.coreApi.delete_namespaced_secret(name, namespace)
