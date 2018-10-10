from kubernetes import client, config
from .config_manager import ConfigManager

class ConfigMapManager:

    def __init__(self):
        ConfigManager()
        self.api = client.CoreV1Api()

    def list_namespaced_configMaps(self, namespace):
        configMaps = []
        api_response = self.api.list_namespaced_config_map(namespace).items
        for item in api_response:
            configMaps.append(item.metadata.name)
        return configMaps

    def read_namespaced_configMap(self, name, namespace):
        return self.api.read_namespaced_config_map(name, namespace)
