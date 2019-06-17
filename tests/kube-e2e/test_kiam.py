import unittest
import time
import requests
from kube.ingress import IngressManager
from kube.deployment import DeploymentManager
from kube.service import ServiceManager
from kube.secret import SecretManager

class TestKiam(unittest.TestCase):

    def setUp(self):
        self.deployment = DeploymentManager()
        self.config = {
            'name': 'kiam-deployment',
            'namespace': 'platform-enablement',
            'replicas': 1,
            'version': 'v0.1.1',
            'container': 'ikerry/kube-app',
            'container_port': 8080,
            'specAnnotaions': {
                "iam.amazonaws.com/role": "arn:aws:iam::885232114932:role/k8s/-s3-role-dev"
            }
        }

    def test_simple_app(self):
        self.deployment.apply_namespaced_deployment(self.config)

        # wait for pods running ...
        time.sleep(20)

        # TODO
        # Trigger api to put data into s3
        # awscli get s3 data
        # assertEqual

    def tearDown(self):
        self.deployment.delete_namespaced_deployment(self.config)

if __name__ == '__main__':
    unittest.main()
