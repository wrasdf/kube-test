import unittest
import time
import requests
from kube.utils.exec import EXEC

class TestSimpleApp(unittest.TestCase):

    def setUp(self):
        self.exec = EXEC()

    def test_simple_app(self):
        self.exec.sh('kubectl apply -f _build/onboarding/')
        # wait for 60 seconds cert-manager to generate tls certs
        time.sleep(60)

        response = requests.get("https://kube-app.svc.dev-green.k8s.platform.myobdev.com/health")
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK!', response.text)

    def tearDown(self):
        self.exec.sh('kubectl delete -f _build/onboarding/')

if __name__ == '__main__':
    unittest.main()
