from kubernetes import client, config

class DaemonsetManager:

    def __init__(self):
        config.load_kube_config()
        self.api = client.ExtensionsV1beta1Api()

    def get_namespaced_daemonset(self, namespace):
        daemonsets = []
        api_response = self.api.list_namespaced_daemon_set(namespace).items
        for item in api_response:
            daemonsets.append(item.metadata.name)
        return daemonsets
