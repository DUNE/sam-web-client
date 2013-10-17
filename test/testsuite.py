#! /usr/bin/env python

import unittest

testmodules = ['test_files', 'test_metadata', 'test_admin', 'test_definition', 'test_project']

if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testmodule in testmodules:
        mod = __import__(testmodule)
        suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(mod))

    unittest.TextTestRunner(verbosity=2).run(suite)
