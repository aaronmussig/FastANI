from unittest import TestCase

from fastani.config import VERSIONS
from fastani.version import get_fastani_version


class TestVersion(TestCase):

    def test_get_version(self):
        for cur_version in VERSIONS[VERSIONS.index('1.1 or 1.2') + 1:]:
            version = get_fastani_version(f'fastANI_{cur_version}')
            self.assertEqual(version, cur_version)

        self.assertEqual(get_fastani_version(f'fastANI_1.0'), '1.0')
        self.assertEqual(get_fastani_version(f'fastANI_1.1'), '1.1 or 1.2')
        self.assertEqual(get_fastani_version(f'fastANI_1.2'), '1.1 or 1.2')
