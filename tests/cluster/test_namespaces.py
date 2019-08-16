import unittest
from kube.resources.namespace import NamespaceManager

must_have_namespaces = [
    'default',
    'kube-public',
    'kube-system'
]

class TestNamespaceManager(unittest.TestCase):

    def setUp(self):
        self.ns_manager = NamespaceManager()

    def test_get_namespaces(self):
        self.cluster_namespaces = self.ns_manager.list()
        for namespace in must_have_namespaces:
            self.assertIn(namespace, self.cluster_namespaces)

if __name__ == '__main__':
    unittest.main()
