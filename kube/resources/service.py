import os
import importlib
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kube.utils.kube_manager import KubeManager


class ServiceManager:

    def __init__(self):
        KubeManager()
        self.exec = EXEC()
        self.coreApi = client.CoreV1Api()

    def list(self, namespace):
        return list(map(lambda x: x.metadata.name, self.coreApi.list_namespaced_service(namespace).items))

    def delete(self, name, namespace):
        # No service
        if name not in self.list_namespaced_service(namespace):
            print("No service resource {0} in namespace {1}".format(name, namespace))
            return True
        return self.coreApi.delete_namespaced_service(name, namespace)
