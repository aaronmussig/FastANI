import os
import tempfile
from unittest import TestCase

from fastani import fastani
from test import GENOMES, KNOWN_ANI, EXE


class TestFastANI(TestCase):

    def test_execution_single_execution(self):
        query = GENOMES['a']
        reference = [GENOMES['b'], GENOMES['c'], GENOMES['d']]

        result = fastani(exe='fastANI_1.33', query=query, reference=reference, single_execution=True)
        self.assertEqual(len(result.executions), 1)

        result_dict = result.as_dict()

        self.assertEqual(len(result_dict), 1)
        self.assertEqual(len(result_dict[query]), len(reference))

        self.assertEqual(result_dict[query][GENOMES['b']], KNOWN_ANI['a']['b'])
        self.assertEqual(result_dict[query][GENOMES['c']], KNOWN_ANI['a']['c'])
        self.assertEqual(result_dict[query][GENOMES['d']], KNOWN_ANI['a']['d'])

    def test_execution_single_execution_bidirectional(self):
        query = GENOMES['a']
        reference = [GENOMES['b'], GENOMES['c'], GENOMES['d']]

        result = fastani(exe='fastANI_1.33', query=query, reference=reference, single_execution=True,
                         bidirectional=True)
        self.assertEqual(len(result.executions), 2)

        result_dict = result.as_dict()

        self.assertEqual(len(result_dict), 4)
        self.assertEqual(len(result_dict[query]), len(reference))

        self.assertEqual(result_dict[GENOMES['a']][GENOMES['b']], KNOWN_ANI['a']['b'])
        self.assertEqual(result_dict[GENOMES['a']][GENOMES['c']], KNOWN_ANI['a']['c'])
        self.assertEqual(result_dict[GENOMES['a']][GENOMES['d']], KNOWN_ANI['a']['d'])

        self.assertEqual(result_dict[GENOMES['b']][GENOMES['a']], KNOWN_ANI['b']['a'])
        self.assertEqual(result_dict[GENOMES['c']][GENOMES['a']], KNOWN_ANI['c']['a'])
        self.assertEqual(result_dict[GENOMES['d']][GENOMES['a']], KNOWN_ANI['d']['a'])

    def test_execution_multi(self):
        query = GENOMES['a']
        reference = [GENOMES['b'], GENOMES['c'], GENOMES['d']]

        result = fastani(exe='fastANI_1.33', query=query, reference=reference, single_execution=False)
        self.assertEqual(len(result.executions), 3)

        result_dict = result.as_dict()

        self.assertEqual(len(result_dict), 1)
        self.assertEqual(len(result_dict[query]), len(reference))

        self.assertEqual(result_dict[query][GENOMES['b']], KNOWN_ANI['a']['b'])
        self.assertEqual(result_dict[query][GENOMES['c']], KNOWN_ANI['a']['c'])
        self.assertEqual(result_dict[query][GENOMES['d']], KNOWN_ANI['a']['d'])

    def test_execution_multi_bidirectional(self):
        query = GENOMES['a']
        reference = [GENOMES['b'], GENOMES['c'], GENOMES['d']]

        result = fastani(exe='fastANI_1.33', query=query, reference=reference, single_execution=False,
                         bidirectional=True)
        self.assertEqual(len(result.executions), 6)

        result_dict = result.as_dict()

        self.assertEqual(len(result_dict), 4)
        self.assertEqual(len(result_dict[query]), len(reference))

        self.assertEqual(result_dict[GENOMES['a']][GENOMES['b']], KNOWN_ANI['a']['b'])
        self.assertEqual(result_dict[GENOMES['a']][GENOMES['c']], KNOWN_ANI['a']['c'])
        self.assertEqual(result_dict[GENOMES['a']][GENOMES['d']], KNOWN_ANI['a']['d'])

        self.assertEqual(result_dict[GENOMES['b']][GENOMES['a']], KNOWN_ANI['b']['a'])
        self.assertEqual(result_dict[GENOMES['c']][GENOMES['a']], KNOWN_ANI['c']['a'])
        self.assertEqual(result_dict[GENOMES['d']][GENOMES['a']], KNOWN_ANI['d']['a'])

    def test_fastani_multi_version(self):
        query = GENOMES['a']
        reference = GENOMES['b']

        for exe in EXE:
            result = fastani(exe=exe, query=query, reference=reference, single_execution=True)
            self.assertEqual(len(result.executions), 1)

    def test_fastani_multiprocessing(self):
        query = GENOMES['a']
        reference = [GENOMES['b'], GENOMES['c'], GENOMES['d']]

        result = fastani(exe='fastANI_1.33', query=query, reference=reference,
                         single_execution=False, bidirectional=True, cpus=4)

        result_dict = result.as_dict()
        self.assertEqual(len(result.executions), 6)

        self.assertEqual(len(result_dict), 4)
        self.assertEqual(len(result_dict[query]), len(reference))

        self.assertEqual(result_dict[GENOMES['a']][GENOMES['b']], KNOWN_ANI['a']['b'])
        self.assertEqual(result_dict[GENOMES['a']][GENOMES['c']], KNOWN_ANI['a']['c'])
        self.assertEqual(result_dict[GENOMES['a']][GENOMES['d']], KNOWN_ANI['a']['d'])

        self.assertEqual(result_dict[GENOMES['b']][GENOMES['a']], KNOWN_ANI['b']['a'])
        self.assertEqual(result_dict[GENOMES['c']][GENOMES['a']], KNOWN_ANI['c']['a'])
        self.assertEqual(result_dict[GENOMES['d']][GENOMES['a']], KNOWN_ANI['d']['a'])

    def test_fastani_missing_path(self):
        query = GENOMES['a']
        reference = '/tmp/not-exist'

        for exe in EXE:
            self.assertRaises(FileNotFoundError, fastani, exe=exe, query=query, reference=reference,
                              single_execution=False)
            self.assertRaises(FileNotFoundError, fastani, exe=exe, query=query, reference=reference,
                              single_execution=True)

    def test_fastani_diff_parameters(self):
        query = GENOMES['a']
        reference = GENOMES['b']

        result = fastani(exe='fastANI_1.33', query=query, reference=reference,
                         k=10, frag_len=1000, min_frac=0.7,
                         single_execution=True, bidirectional=False)

        self.assertTrue('-k 10' in result.executions[0].cmd)
        self.assertTrue('--fragLen 1000' in result.executions[0].cmd)
        self.assertTrue('--minFraction 0.7' in result.executions[0].cmd)

    def test_fastani_write_results_to_disk(self):
        query = [GENOMES['a'], GENOMES['b'], GENOMES['c'], GENOMES['d']]
        reference = query

        result = fastani(exe='fastANI_1.33', query=query, reference=reference,
                         single_execution=True, bidirectional=False, cpus=8)

        with tempfile.TemporaryDirectory() as tmpdir:
            path_out = os.path.join(tmpdir, 'results.txt')

            result.to_file(path_out)

            with open(path_out, 'r') as f:
                data = f.read()

            self.assertEqual(len(data.splitlines()), 16)
