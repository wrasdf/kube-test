import os
import importlib
from kubernetes import client, config
from kube.utils.kube_manager import KubeManager

class DaemonsetManager:

    def __init__(self):
        KubeManager()
        self.api = client.ExtensionsV1beta1Api()

    def list(self, namespace):
        return list(map(lambda x: x.metadata.name, self.api.list_namespaced_daemon_set(namespace).items))
