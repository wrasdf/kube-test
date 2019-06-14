import os
import importlib
from kubernetes import client, config

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "config_manager.py")).load_module()
from config_manager import ConfigManager


class SecretManager:

    def __init__(self):
        ConfigManager()
        self.api = client.CoreV1Api()

    def list_namespaced_secret(self, namespace):
        return self.api.list_namespaced_secret(namespace, watch=False).items
