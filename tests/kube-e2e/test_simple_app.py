import unittest
import time
import requests
from kube.ingress import IngressManager
from kube.deployment import DeploymentManager
from kube.service import ServiceManager
from kube.secret import SecretManager

class TestSimpleApp(unittest.TestCase):

    def setUp(self):
        self.deployment = DeploymentManager()
        self.ingress = IngressManager()
        self.service = ServiceManager()
        self.secret = SecretManager()
        self.config = {
            'name': 'simple-app',
            'namespace': 'platform-enablement',
            'replicas': 1,
            'version': 'v0.1.6',
            'container': 'ikerry/kube-app',
            'container_port': 8080,
            'dns_name': 'simple.svc.platform.myobdev.com'
        }

    def test_simple_app(self):
        self.deployment.apply_namespaced_deployment(self.config)
        self.ingress.apply_namespaced_ingress(self.config)
        self.service.apply_namesapced_service(self.config)

        # wait for 60 seconds cert-manager to generate tls certs
        time.sleep(60)

        response = requests.get("https://{0}/health".format(self.config['dns_name']))
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK!', response.text)

    def tearDown(self):
        self.deployment.delete_namespaced_deployment(self.config)
        self.ingress.delete_namespaced_ingress(self.config)
        self.service.delete_namespaced_service(self.config)

        # Delete tls secret
        self.secret.delete_namespaced_secret({
            'name': '{0}-tls'.format(self.config['name']),
            'namespace': self.config['namespace']
        })

if __name__ == '__main__':
    unittest.main()
