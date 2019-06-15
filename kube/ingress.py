from config_manager import ConfigManager
import os
import importlib
from kubernetes import client, config
from kubernetes.client.rest import ApiException

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(
    current_dir, "config_manager.py")).load_module()


class IngressManager:

    def __init__(self):
        ConfigManager()
        self.extensionApi = client.ExtensionsV1beta1Api()

    def list_namespaced_ingress(self, namespace):
        return list(map(lambda x: x.metadata.name, self.extensionApi.list_namespaced_ingress(namespace).items))

    def get_metadata(self, params):
        return client.V1ObjectMeta(
            name=params['name'],
            namespace=params['namespace'],
            labels={
                'app': params['name'],
                'purpose': 'test'
            },
            annotations={
                "kubernetes.io/tls-acme": "true"
            }
        )

    def get_spec(self, params):
        return client.ExtensionsV1beta1IngressSpec(
            tls=[
                client.ExtensionsV1beta1IngressTLS(
                    hosts=[
                        params['dns_name']
                    ],
                    secret_name='{0}-tls'.format(params['name'])
                )
            ],
            rules=[
                client.ExtensionsV1beta1IngressRule(
                    host=params['dns_name'],
                    http=client.ExtensionsV1beta1HTTPIngressRuleValue(
                        paths=[
                            client.ExtensionsV1beta1HTTPIngressPath(
                                path='/',
                                backend=client.ExtensionsV1beta1IngressBackend(
                                    service_name=params['name'],
                                    service_port=params['container_port']
                                )
                            )
                        ]
                    )
                )
            ]
        )

    def create_ingress(self, params):
        defaultValue = {
            'name': 'test-deployment',
            'namespace': 'platform-enablement',
        }
        results = dict(defaultValue, **params)

        try:
            return self.extensionApi.create_namespaced_ingress(
                results['namespace'],
                client.ExtensionsV1beta1Ingress(
                    api_version='extensions/v1beta1',
                    kind='Ingress',
                    metadata=self.get_metadata(results),
                    spec=self.get_spec(results)
                )
            )
        except ApiException as e:
            print(
                "Exception when calling ExtensionsV1beta1Api->create_namespaced_ingress: %s\n" % e)

    def replace_ingress(self, params):
        defaultValue = {
            'name': 'test-deployment',
            'namespace': 'platform-enablement',
        }
        results = dict(defaultValue, **params)

        try:
            return self.extensionApi.replace_namespaced_ingress(
                results['name'],
                results['namespace'],
                client.ExtensionsV1beta1Ingress(
                    api_version='extensions/v1beta1',
                    kind='Ingress',
                    metadata=self.get_metadata(results),
                    spec=self.get_spec(results)
                )
            )
        except ApiException as e:
            print(
                "Exception when calling ExtensionsV1beta1Api->replace_namespaced_ingress: %s\n" % e)

    def apply_ingress(self, params):
        if params['name'] in self.list_namespaced_ingress(params['namespace']):
            self.replace_ingress(params)
        else:
            self.create_ingress(params)
        pass
