import os
import importlib
from kubernetes import client, config
from kubernetes.client.rest import ApiException

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "config_manager.py")).load_module()
from config_manager import ConfigManager


class SecretManager:

    def __init__(self):
        ConfigManager()
        self.coreApi = client.CoreV1Api()

    def get_metadata(self, params):
        return client.V1ObjectMeta(
            name=params['name'],
            namespace=params['namespace'],
            labels={
                'app': params['name'],
                'purpose': 'test'
            }
        )

    def list_namespaced_secret(self, namespace):
        return list(map(lambda x: x.metadata.name, self.coreApi.list_namespaced_secret(namespace).items))

    def read_namespaced_secret(self, params):
        return self.coreApi.read_namespaced_secret(params['name'], params['namespace'])

    def create_namespaced_secret(self, params):
        try:
            self.coreApi.create_namespaced_secret(params['namespace'], client.V1Secret(
                api_version="v1",
                kind="Secret",
                metadata=self.get_metadata(params),
                data=params['data'],
                type="Opaque"
            ))
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_secret: %s\n" % e)

    def patch_namespaced_secret(self, params):
        try:
            self.coreApi.patch_namespaced_secret(params['namespace'], client.V1Secret(
                api_version="v1",
                kind="Secret",
                metadata=self.get_metadata(params),
                data=params['data'],
                type="Opaque"
            ))
        except ApiException as e:
            print("Exception when calling CoreV1Api->patch_namespaced_secret: %s\n" % e)

    def apply_namespaced_secret(self, params):
        if params['name'] in self.list_namespaced_secret(params['namespace']):
            self.patch_namespaced_secret(params)
        else:
            self.create_namespaced_secret(params)

    def delete_namespaced_secret(self, params):
        if params['name'] not in self.list_namespaced_secret(params['namespace']):
            print("No secret resource {0} in namespace {1}".format(params['name'], params['namespace']))
            return True
        return self.coreApi.delete_namespaced_secret(params['name'], params['namespace'])
