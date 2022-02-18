from unittest import TestCase

from fastani.util import validate_paths


class TestValidate(TestCase):

    def test_transform_input_string(self):
        self.assertSetEqual(frozenset(['/tmp/a.txt']), validate_paths('/tmp/a.txt'))

    def test_transform_input_collection(self):
        data = ['/tmp/a.txt', '/tmp/b.txt', '/tmp/a.txt']
        self.assertSetEqual(frozenset(data), validate_paths(data))
