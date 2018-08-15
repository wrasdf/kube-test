from kubernetes import client, config

class PodManager:

    def __init__(self):
        config.load_kube_config()
        self.api = client.CoreV1Api()

    def list_namespaced_pods(self, namespace):
        return self.api.list_namespaced_pod(namespace, watch=False).items
