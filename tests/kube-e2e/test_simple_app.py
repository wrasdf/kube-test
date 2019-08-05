import unittest
import time
import requests
import os
from kube.utils.exec import EXEC

class TestSimpleApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.exec = EXEC()
        cls.exec.sh('kubectl apply --dry-run -f _build/onboarding/')
        cls.exec.sh('kubectl apply -f _build/onboarding/')

        # # wait for 60 seconds cert-manager to generate tls certs
        time.sleep(60)


    def setUp(self):
        self.bucket = 'myob-test-kube-app'
        self.key = 'test.txt'
        self.content = 'Send Data By API'
        self.dns_name = os.getenv('dns_name', 'kube-app.svc.europa-stg.jupiter.myobdev.com')

    def test_simple_app(self):
        # when
        response = requests.get(f"https://{self.dns_name}/health")

        # then
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK!', response.text)

    def test_simple_app_with_kiam(self):
        # when
        createBucketRes = requests.post(f"https://{self.dns_name}/s3/v1/{self.bucket}")
        putObjectRes = requests.put(f"https://{self.dns_name}/s3/v1/{self.bucket}/{self.key}", data={'data':f'{self.content}'})
        getObjectRes = requests.get(f"https://{self.dns_name}/s3/v1/{self.bucket}/{self.key}")

        # # then
        self.assertEqual(200, createBucketRes.status_code)
        self.assertEqual(200, putObjectRes.status_code)
        self.assertEqual(getObjectRes.json()["data"], self.content)

        # # clean
        requests.delete(f"https://{self.dns_name}/s3/v1/{self.bucket}/{self.key}")
        requests.delete(f"https://{self.dns_name}/s3/v1/{self.bucket}")

    @classmethod
    def tearDownClass(cls):
        # delete app
        cls.exec.sh('kubectl delete -f _build/onboarding/')

if __name__ == '__main__':
    unittest.main()
