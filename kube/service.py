from kubernetes import client, config

class ServiceManager:

    def __init__(self):
        config.load_kube_config()
        self.api = client.CoreV1Api()

    def list_namespaced_service(self, namespace):
        return self.api.list_namespaced_service(namespace, watch=False).items
