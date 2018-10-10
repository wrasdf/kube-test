from kubernetes import client, config
from .config_manager import ConfigManager

class SecretManager:

    def __init__(self):
        ConfigManager()
        self.api = client.CoreV1Api()

    def list_namespaced_secret(self, namespace):
        return self.api.list_namespaced_secret(namespace, watch=False).items
