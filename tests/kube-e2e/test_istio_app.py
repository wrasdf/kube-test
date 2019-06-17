import unittest
import time
import requests
from kube.ingress import IngressManager
from kube.deployment import DeploymentManager
from kube.service import ServiceManager
from kube.secret import SecretManager
from kube.exec import EXEC

class TestIstio(unittest.TestCase):

    def setUp(self):
        self.exec = EXEC()
        self.deployment = DeploymentManager()
        self.ingress = IngressManager()
        self.service = ServiceManager()
        self.secret = SecretManager()
        self.config = {
            'name': 'istio_apps',
            'namespace': 'platform-enablement',
            'replicas': 1,
            'version': 'v0.1.1',
            'container': 'ikerry/kube-app',
            'container_port': 8080,
            'dns_name': 'node1.svc.platform.myobdev.com'
        }

        self.node1Config = dict(self.config)
        self.node2Config = dict(self.config, **{
            'name': 'node2-deployment',
            'dns_name': 'node2.svc.platform.myobdev.com'
        })
        self.node3Config = dict(self.config, **{
            'name': 'node3-deployment',
            'dns_name': 'node3.svc.platform.myobdev.com',
            'developmentAnnotatins': {
                 "sidecar.istio.io/inject": "true"
             }
        })
        self.node4Config = dict(self.config, **{
            'name': 'node4-deployment',
            'dns_name': 'node4.svc.platform.myobdev.com',
            'developmentAnnotatins': {
                 "sidecar.istio.io/inject": "true"
             }
        })

        self.nodesConfig = [
            self.node1Config,
            self.node2Config,
            self.node3Config,
            self.node4Config
        ]

    def test_istio_app(self):

        for item in self.nodesConfig:
            self.deployment.apply_namespaced_deployment(item)
            self.ingress.apply_namespaced_ingress(item)
            self.service.apply_namesapced_service(item)

        # wait for 60 seconds cert-manager to generate tls certs
        time.sleep(60)

        # TODO:
        # with sidecar could talk to with sidecar


        # TODO:
        # with sidecar could talk to without sidecar

        # TODO:
        # without sidecar could talk to with sidecar

        # TODO:
        # without sidecar could talk to without sidecar


        # response = requests.get("https://{0}/api/v1/health".format(self.config['dns_name']))
        # self.assertEqual(200, response.status_code)
        # self.assertEqual('OK!', response.text)

    def tearDown(self):
        for item in self.nodesConfig:
            self.deployment.delete_namespaced_deployment(item)
            self.ingress.delete_namespaced_ingress(item)
            self.service.delete_namespaced_service(item)
            # Delete tls secret
            self.secret.delete_namespaced_secret({
                'name': '{0}-tls'.format(item['name']),
                'namespace': item['namespace']
            })

if __name__ == '__main__':
    unittest.main()
