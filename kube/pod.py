from kubernetes import client, config
from .config_manager import ConfigManager

class PodManager:

    def __init__(self):
        ConfigManager()
        self.api = client.CoreV1Api()

    def list_namespaced_pods(self, namespace):
        return self.api.list_namespaced_pod(namespace, watch=False).items
