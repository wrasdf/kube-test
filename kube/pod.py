import os
import importlib
from kubernetes import client, config

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "config_manager.py")).load_module()
from config_manager import ConfigManager


class PodManager:

    def __init__(self):
        ConfigManager()
        self.api = client.CoreV1Api()

    def list_namespaced_pods(self, namespace):
        return self.api.list_namespaced_pod(namespace, watch=False).items
