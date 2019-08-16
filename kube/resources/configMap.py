import os
import importlib
from kubernetes import client, config
from kube.utils.kube_manager import KubeManager


class ConfigMapManager:

    def __init__(self):
        KubeManager()
        self.api = client.CoreV1Api()

    def list(self, namespace):
        return list(map(lambda x: x.metadata.name, self.api.list_namespaced_config_map(namespace).items))

    def read(self, name, namespace):
        return self.api.read_namespaced_config_map(name, namespace)
