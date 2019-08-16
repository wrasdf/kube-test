import os
import importlib
from kubernetes import client, config
from kube.utils.kube_manager import KubeManager

class NamespaceManager:

    def __init__(self):
        KubeManager()
        self.api = client.CoreV1Api()

    def list(self):
        return list(map(lambda x: x.metadata.name, self.api.list_namespace().items))
