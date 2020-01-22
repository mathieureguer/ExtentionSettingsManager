import sys
import unittest
from unittest.mock import MagicMock, patch

sys.modules['mojo.extensions'] = MagicMock()
sys.modules['vanilla'] = MagicMock()

from ExtentionSettingsManager import ExtentionSettingsManager


KEY_PREFIX = "com.mathieureguer.test."
TEST_DATA = {"hello": "world",
             "foo": "bar",
             }

TEST_DATA_PREFIXED = {KEY_PREFIX + "hello": "world",
                      KEY_PREFIX + "foo": "bar",
                      }


class TestExtentionSettingManager(unittest.TestCase):

    def test_dict_input(self):
        """
        Test that it can sum a list of integers
        """
        manager = ExtentionSettingsManager(KEY_PREFIX)
        for k, v in TEST_DATA.items():
            manager[k] = v
        self.assertEqual(manager.data, TEST_DATA)

    def test_dict_update(self):
        """
        Test that it can sum a list of integers
        """
        manager = ExtentionSettingsManager(KEY_PREFIX)
        manager.update(TEST_DATA)
        self.assertEqual(manager.data, TEST_DATA)

    def test_dict_get(self):
        """
        Test that it can sum a list of integers
        """
        manager = ExtentionSettingsManager(KEY_PREFIX)
        manager.update(TEST_DATA)
        for k in manager.keys():
            self.assertEqual(manager[k], TEST_DATA[k])

    def test_dict_prefix(self):
        """
        Test that it can sum a list of integers
        """
        manager = ExtentionSettingsManager(KEY_PREFIX)
        manager.update(TEST_DATA)

        self.assertEqual(manager.data_with_prefix, TEST_DATA_PREFIXED)

    def test_dict_cleaner(self):
        """
        Test that it can sum a list of integers
        """
        manager = ExtentionSettingsManager(KEY_PREFIX)
        manager.data_from_prefix(TEST_DATA_PREFIXED)
        self.assertEqual(manager.data, TEST_DATA)


if __name__ == '__main__':
    unittest.main()
