from kubernetes import client, config

class NamespaceManager:

    def __init__(self):
        config.load_kube_config()
        self.api = client.CoreV1Api()

    def list_all_namespaces(self):
        namespaces = []
        api_response = self.api.list_namespace().items
        for item in api_response:
            namespaces.append(item.metadata.name)
        return namespaces
