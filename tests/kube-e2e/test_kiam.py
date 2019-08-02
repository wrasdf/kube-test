# import unittest
# import time
# import requests
# from kube.utils.exec import EXEC
#
# class TestKiam(unittest.TestCase):
#
#     def setUp(self):
#         self.exec = EXEC()
#         self.bucket = 'myob-test-kube-app'
#         self.key = 'test.txt'
#         self.content = 'Send Data By API'
#         self.dns_name = 'kube-app.svc.dev-green.k8s.platform.myobdev.com'
#
#     def test_simple_app(self):
#         self.exec.exec_sh('kubectl apply --dry-run -f _build/onboarding/')
#         self.exec.exec_sh('kubectl apply -f _build/onboarding/')
#
#         # wait for 60 seconds cert-manager to generate tls certs
#         time.sleep(60)
#
#         createBucketRes = requests.post("https://{0}/s3/v1/{1}".format(self.dns_name, self.bucket))
#         putBucketObjectRes = requests.put("https://{0}/s3/v1/{1}/{2}".format(self.dns_name, self.bucket, self.key), data={'data':'{0}'.format(self.content)})
#         bucket = self.exec.sh('aws s3 ls | grep %s | awk "{print $3}"' % self.bucket)
#         # TODO
#         # Need to get data
#         self.exec.sh('aws s3api get-object --bucket {0} --key {1} {2}'.format(self.bucket, self.key, self.key))
#         content = self.exec.sh('cat {0}'.format(self.key))
#         self.assertEqual(200, createBucket.status_code)
#         self.assertEqual(200, putBucketObject.status_code)
#         self.assertEqual(bucket, self.bucket)
#         self.assertEqual(content, self.content)
#
#     def tearDown(self):
#         self.exec.sh('echo 123456')
#         # self.exec.sh('kubectl delete -f _build/onboarding/')
#         #
#         # # Delete s3 bucket
#         # self.exec.sh('aws s3api delete-bucket --bucket {0} --region ap-southeast-2'.format(self.bucket))
#
# if __name__ == '__main__':
#     unittest.main()
