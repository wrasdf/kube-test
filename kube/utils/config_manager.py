import os
from kubernetes import client, config

class ConfigManager:

    def __init__(self, env=None):
        if "KUBERNETES_SERVICE_HOST" in os.environ:
            config.load_incluster_config()
        else:
            config.load_kube_config()
