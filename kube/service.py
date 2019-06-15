import os
import importlib
from kubernetes import client, config
from kubernetes.client.rest import ApiException

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "config_manager.py")).load_module()
from config_manager import ConfigManager

# example of params:
# {
#     'name': 'test-deployment',
#     'namespace': 'platform-enablement',
#     'replicas': 2,
#     'version: v0.1.6',
#     'container': 'ikerry/metrics-node',
#     'container_port': '8080',
#     'dns_name': 'nodet.svc.platform.myobdev.com',
# }
class ServiceManager:

    def __init__(self):
        ConfigManager()
        self.coreApi = client.CoreV1Api()

    def list_namespaced_service(self, namespace):
        return self.coreApi.list_namespaced_service(namespace, watch=False).items

    def get_metadata(self, params):
        return client.V1ObjectMeta(
            name=params['name'],
            namespace=params['namespace'],
            labels={
                'app': params['name'],
                'purpose': 'test'
            }
        )

    def get_spec(self, params):
        return client.V1ServiceSpec(
            ports=[
                client.V1ServicePort(
                    name=params['name'],
                    protocol='TCP',
                    port=80,
                    target_port=params['container_port']
                )
            ],
            selector={
                'app': params['name'],
                'purpose': 'test'
            }
        )

    def create_namespaced_service(self, params):
        try:
            return self.coreApi.create_namespaced_service(
                params['namespace'],
                client.V1Service(
                    api_version='v1',
                    kind='Service',
                    metadata=self.get_metadata(params),
                    spec=self.get_spec(params)
                )
            )
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_service: %s\n" % e)

    def replace_namespaced_service(self, params):
        try:
            return self.coreApi.replace_namespaced_service(
                params['namespace'],
                client.V1Service(
                    api_version='v1',
                    kind='Service',
                    metadata=self.get_metadata(params),
                    spec=self.get_spec(params)
                )
            )
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_service: %s\n" % e)

    def apply_namespaced_service(self, params):
        if params['name'] in self.list_namespaced_service(params['namespace']):
            self.replace_namespaced_service(params)
        else:
            self.create_namespaced_service(params)

    def delete_namespaced_service(self, name, namespace):
        # No service
        if params['name'] not in self.list_namespaced_service(params['namespace']):
            print("No service resource {0} in namespace {1}".format(params['name'], params['namespace']))
            return True

        try:
            return self.coreApi.delete_namespaced_service(
                params['name'],
                params['namespace']
            )
        except ApiException as e:
            print(
                "Exception when calling CoreV1Api->delete_namespaced_service: %s\n" % e)
