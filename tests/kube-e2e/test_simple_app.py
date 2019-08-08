import unittest
import time
import requests
import os
import uuid
from kube.utils.exec import EXEC

class TestSimpleApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.exec = EXEC()
        cls.exec.sh('kubectl apply --dry-run -f _build/onboarding/')
        cls.exec.sh('kubectl apply -f _build/onboarding/')

        # wait for 60 seconds cert-manager to generate tls certs
        time.sleep(60)


    def setUp(self):
        self.dns_name = os.getenv('dns_name', 'kube-app.svc.europa-stg.jupiter.myobdev.com').strip()

    def test_simple_app(self):
        # when
        response = requests.get(f"https://{self.dns_name}/health")

        # then
        self.assertEqual(200, response.status_code)
        self.assertEqual('OK!', response.text)

    def test_simple_app_with_kiam(self):
        # given
        uuid4 = uuid.uuid4()
        bucket = f'myob-test-kube-app-{uuid4}'
        key = f'test-{uuid4}.txt'
        content = f'Send Data By API - {uuid4}'

        # when
        createBucketRes = requests.post(f"https://{self.dns_name}/s3/v1/{bucket}")
        putObjectRes = requests.put(f"https://{self.dns_name}/s3/v1/{bucket}/{key}", data={'data':f'{content}'})
        getObjectRes = requests.get(f"https://{self.dns_name}/s3/v1/{bucket}/{key}")

        # then
        self.assertEqual(200, createBucketRes.status_code)
        self.assertEqual(200, putObjectRes.status_code)
        self.assertEqual(getObjectRes.json()["data"], content)

        # clean
        requests.delete(f"https://{self.dns_name}/s3/v1/{bucket}/{key}")
        requests.delete(f"https://{self.dns_name}/s3/v1/{bucket}")

    @classmethod
    def tearDownClass(cls):
        # delete app
        cls.exec.sh('kubectl delete -f _build/onboarding/')

if __name__ == '__main__':
    unittest.main()
