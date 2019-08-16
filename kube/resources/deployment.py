import os
import importlib
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
from kube.utils.kube_manager import KubeManager

class DeploymentManager:

    def __init__(self):
        KubeManager()
        self.appApi = client.AppsV1Api()

    def list(self, namespace):
        return list(map(lambda x: x.metadata.name, self.appApi.list_namespaced_deployment(namespace).items))

    def delete(self, name, namespace):
        # No deployment
        if name not in self.list_namespaced_deployments(namespace):
            print("No deployment resource {0} in namespace {1}".format(name, namespace))
            return True

        try:
            return self.appApi.delete_namespaced_deployment(name, namespace)
        except ApiException as e:
            print("Exception when calling AppsV1Api -> delete_namespaced_deployment: %s\n" % e)
