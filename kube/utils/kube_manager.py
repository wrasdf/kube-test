import os
from kubernetes import client, config

# from os import path, getenv
#
# from kubernetes.client import api_client, CustomObjectsApi
# from kubernetes.client.rest import ApiException
# from kubernetes.config import kube_config, incluster_config, new_client_from_config

class KubeManager:

    def __init__(self):
        if "KUBERNETES_SERVICE_HOST" in os.environ:
            config.load_incluster_config()
        else:
            config.load_kube_config()

        self.client =  client

    def apply(self):
        pass

    def delete(self):
        pass

    def get(self):
        pass
