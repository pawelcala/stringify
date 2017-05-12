import unittest
from unittest import TestLoader, TestSuite

from tests import dictionary_tests, test_formatters

if __name__ == '__main__':
    testcases = list()
    testcases.append(dictionary_tests.DictionaryTests)
    testcases.append(dictionary_tests.AndroidStringsLoaderTests)
    testcases.append(dictionary_tests.IOSStringsLoaderTests)
    testcases.append(test_formatters.TestAndroidFormatter)
    testcases.append(test_formatters.TestSwiftFormatter)
    testcases.append(test_formatters.TestAndroidToDictionary)
    testcases.append(test_formatters.SwiftToDictionaryTests)

    test_loader = TestLoader()
    test_suite = TestSuite()
    for case in testcases:
        test = test_loader.loadTestsFromTestCase(case)
        test_suite.addTest(test)

    runner = unittest.TextTestRunner()
    runner.run(test_suite)
