import os
import importlib
from kubernetes import client, config

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "config_manager.py")).load_module()
from config_manager import ConfigManager


class ConfigMapManager:

    def __init__(self):
        ConfigManager()
        self.api = client.CoreV1Api()

    def list_namespaced_configMaps(self, namespace):
        return list(map(lambda x: x.metadata.name, self.api.list_namespaced_config_map(namespace).items))

    def read_namespaced_configMap(self, name, namespace):
        return self.api.read_namespaced_config_map(name, namespace)
