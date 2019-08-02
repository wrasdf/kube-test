import unittest
import time
import requests
from kube.utils.exec import EXEC

class TestKiam(unittest.TestCase):

    def setUp(self):
        self.exec = EXEC()
        self.bucket = 'myob-test-kube-app'
        self.key = 'test.txt'
        self.content = 'Send Data By API'
        # self.dns_name = 'kube-app.svc.dev-green.k8s.platform.myobdev.com'
        self.dns_name = 'kube-app.svc.europa-stg.jupiter.myobdev.com'

    def test_simple_app(self):
        # given
        # self.exec.sh('kubectl apply --dry-run -f _build/onboarding/')
        # self.exec.sh('kubectl apply -f _build/onboarding/')
        #
        # # wait for 60 seconds cert-manager to generate tls certs
        # time.sleep(60)

        # when
        # createBucketRes = requests.post(f"https://{self.dns_name}/s3/v1/{self.bucket}")
        # putObjectRes = requests.put(f"https://{self.dns_name}/s3/v1/{self.bucket}/{self.key}", data={'data':f'{self.content}'})
        getObjectRes = requests.get(f"https://{self.dns_name}/s3/v1/{self.bucket}/{self.key}")
        print(getObjectRes.text)
        print(getObjectRes.headers['content-type'])

        # then
        # self.exec.sh(f'aws s3api get-object --bucket {self.bucket} --key {self.key} {self.key}')
        # content = self.exec.sh(f'cat {self.key}')
        # self.assertEqual(200, createBucketRes.status_code)
        # self.assertEqual(200, putObjectRes.status_code)
        # self.assertEqual(content, self.content)

    def tearDown(self):
        # delete key & bucket
        # requests.delete(f"https://{self.dns_name}/s3/v1/{self.bucket}/{self.key}")
        # requests.delete(f"https://{self.dns_name}/s3/v1/{self.bucket}")
        #
        # delete app
        # self.exec.sh('kubectl delete -f _build/onboarding/')
        self.exec.sh('echo 12345')


if __name__ == '__main__':
    unittest.main()
