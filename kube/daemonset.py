from kubernetes import client, config
from .config_manager import ConfigManager

class DaemonsetManager:

    def __init__(self):
        ConfigManager()
        self.api = client.ExtensionsV1beta1Api()

    def list_namespaced_daemonsets(self, namespace):
        daemonsets = []
        api_response = self.api.list_namespaced_daemon_set(namespace).items
        for item in api_response:
            daemonsets.append(item.metadata.name)
        return daemonsets
