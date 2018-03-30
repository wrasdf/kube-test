import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, '../kube'))

import unittest
from daemonset import DaemonsetManager

must_have_daemonsets = ['canal', 'kube-logging', 'kube2iam', 'prometheus-node-exporter']

class TestDaemonsetsManager(unittest.TestCase):

    def setUp(self):
        self.daemonset_manager = DaemonsetManager()

    def test_get_kube_system_daemonsets(self):
        self.kube_system_daemonsets = self.daemonset_manager.get_namespaced_daemonset('kube-system')
        for daemonsets in must_have_daemonsets:
            self.assertIn(daemonsets, self.kube_system_daemonsets)

if __name__ == '__main__':
    unittest.main()
