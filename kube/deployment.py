import os
import importlib
from kubernetes import client, config

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "config_manager.py")).load_module()
from config_manager import ConfigManager


class DeploymentManager:

    def __init__(self):
        ConfigManager()
        self.api = client.ExtensionsV1beta1Api()

    def list_namespaced_deployments(self, namespace):
        deployments = []
        api_response = self.api.list_namespaced_deployment(namespace).items
        for item in api_response:
            deployments.append(item.metadata.name)
        return deployments
