from kubernetes import client, config

class DeploymentManager:

    def __init__(self):
        config.load_kube_config()
        self.api = client.ExtensionsV1beta1Api()

    def get_namespaced_deployment(self, namespace):
        deployments = []
        api_response = self.api.list_namespaced_deployment(namespace).items
        for item in api_response:
            deployments.append(item.metadata.name)
        return deployments
