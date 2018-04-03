import unittest
from kube.daemonset import DaemonsetManager

must_have_daemonsets = [
    'canal',
    'kube-logging',
    'kube2iam',
    'prometheus-node-exporter'
]

class TestDaemonsetsManager(unittest.TestCase):

    def setUp(self):
        self.daemonset_manager = DaemonsetManager()

    def test_kube_system_daemonsets(self):
        self.kube_system_daemonsets = self.daemonset_manager.list_namespaced_daemonsets('kube-system')
        for daemonsets in must_have_daemonsets:
            self.assertIn(daemonsets, self.kube_system_daemonsets)

if __name__ == '__main__':
    unittest.main()
