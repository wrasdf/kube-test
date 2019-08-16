import unittest
import os
from kube.utils.util import Utils

class TestDeploymentsManager(unittest.TestCase):

    def setUp(self):
        self.util = Utils()
        self.current_dir = os.path.dirname(__file__)

    def test_merge(self):
        baseYamlPath = '{0}/files/base.yaml'.format(self.current_dir)
        envYamlPath = '{0}/files/dev-green.yaml'.format(self.current_dir)
        result = self.util.merge([baseYamlPath, envYamlPath])
        self.assertEqual(result['onboarding']['dns_name'], 'kube-app.svc.dev-green.k8s.platform.myobdev.com')
        self.assertEqual(result['onboarding']['hpa']['enable'], False)

if __name__ == '__main__':
    unittest.main()
