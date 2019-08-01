import unittest
import time
import requests
from kube.ingress import IngressManager
from kube.deployment import DeploymentManager
from kube.service import ServiceManager
from kube.secret import SecretManager
from kube.exec import EXEC

class TestKiam(unittest.TestCase):

    def setUp(self):
        self.deployment = DeploymentManager()
        self.ingress = IngressManager()
        self.service = ServiceManager()
        self.secret = SecretManager()
        self.exec = EXEC()
        self.config = {
            'name': 'simple-app',
            'namespace': 'platform-enablement',
            'replicas': 1,
            'version': 'v0.1.6',
            'container': 'ikerry/kube-app',
            'container_port': 8080,
            'dns_name': 'simple.svc.platform.myobdev.com'
        }
        self.bucket = 'myob-test-kube-app'
        self.key = 'test.txt'
        self.content = 'Send Data By API'

    def test_simple_app(self):
        self.deployment.apply_namespaced_deployment(self.config)
        self.ingress.apply_namespaced_ingress(self.config)
        self.service.apply_namesapced_service(self.config)

        # wait for 60 seconds cert-manager to generate tls certs
        time.sleep(60)

        createBucketRes = requests.post("https://{0}/s3/v1/{1}".format(self.config['dns_name'], self.bucket))
        putBucketObjectRes = requests.put("https://{0}/s3/v1/{1}/{2}".format(self.config['dns_name'], self.bucket, self.key), data={'data':'{0}'.format(self.content)})
        bucket = self.exec('aws s3 ls | grep %s | awk "{print $3}"' % self.bucket)
        # TODO
        # Need to get data
        self.exec('aws s3api get-object --bucket {0} --key {1} {2}'.format(self.bucket, self.key, self.key))
        content = self.exec('cat {0}'.format(self.key))
        self.assertEqual(200, createBucket.status_code)
        self.assertEqual(200, putBucketObject.status_code)
        self.assertEqual(bucket, self.bucket)
        self.assertEqual(content, self.content)

    def tearDown(self):
        self.deployment.delete_namespaced_deployment(self.config)
        self.ingress.delete_namespaced_ingress(self.config)
        self.service.delete_namespaced_service(self.config)

        # Delete tls secret
        self.secret.delete_namespaced_secret({
            'name': '{0}-tls'.format(self.config['name']),
            'namespace': self.config['namespace']
        })

        # Delete s3 bucket
        self.exec('aws s3api delete-bucket --bucket {0} --region ap-southeast-2'.format(self.bucket))

if __name__ == '__main__':
    unittest.main()
