import os
import importlib
from kubernetes import client, config

from kube.utils.kube_manager import KubeManager

class PodManager:

    def __init__(self):
        KubeManager()
        self.api = client.CoreV1Api()

    def list(self, namespace):
        return self.api.list_namespaced_pod(namespace, watch=False).items
