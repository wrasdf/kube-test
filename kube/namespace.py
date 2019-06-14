import os
import importlib
from kubernetes import client, config

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "config_manager.py")).load_module()
from config_manager import ConfigManager


class NamespaceManager:

    def __init__(self):
        ConfigManager()
        self.api = client.CoreV1Api()

    def list_all_namespaces(self):
        namespaces = []
        api_response = self.api.list_namespace().items
        for item in api_response:
            namespaces.append(item.metadata.name)
        return namespaces
