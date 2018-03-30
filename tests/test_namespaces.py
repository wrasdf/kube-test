import os
import sys
import ssl

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, '../kube'))

import unittest
from namespace import NamespaceManager

must_have_namespaces = ['default', 'heptio-ark', 'kube-public', 'kube-system', 'platform-enablement', 'platform-enablement-shadow']

class TestNamespaceManager(unittest.TestCase):

    def setUp(self):
        self.ns_manager = NamespaceManager()

    def test_get_namespaces(self):
        self.cluster_namespaces = self.ns_manager.get_all_namespaces()
        for namespace in must_have_namespaces:
            self.assertIn(namespace, self.cluster_namespaces)

if __name__ == '__main__':
    unittest.main()
