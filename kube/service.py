from kubernetes import client, config
from .config_manager import ConfigManager

class ServiceManager:

    def __init__(self):
        ConfigManager()
        self.api = client.CoreV1Api()

    def list_namespaced_service(self, namespace):
        return self.api.list_namespaced_service(namespace, watch=False).items
