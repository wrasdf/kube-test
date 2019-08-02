import unittest
import time
import requests
from kube.utils.exec import EXEC

class TestSimpleApp(unittest.TestCase):

    def setUp(self):
        self.exec = EXEC()
        # self.dns_name = 'kube-app.svc.dev-green.k8s.platform.myobdev.com'
        self.dns_name = 'kube-app.svc.europa-stg.jupiter.myobdev.com'

    def test_simple_app(self):
        # given
        self.exec.sh('kubectl apply --dry-run -f _build/onboarding/')
        self.exec.sh('kubectl apply -f _build/onboarding/')
        # wait for 60 seconds cert-manager to generate tls certs
        time.sleep(60)

        # when
        response = requests.get(f"https://{self.dns_name}/health")

        # then
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK!', response.text)

    def tearDown(self):
        # delete app
        self.exec.sh('kubectl delete -f _build/onboarding/')

if __name__ == '__main__':
    unittest.main()
