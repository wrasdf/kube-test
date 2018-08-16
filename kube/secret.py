from kubernetes import client, config

class SecretManager:

    def __init__(self):
        config.load_kube_config()
        self.api = client.CoreV1Api()

    def list_namespaced_secret(self, namespace):
        return self.api.list_namespaced_secret(namespace, watch=False).items
