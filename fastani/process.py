import os
import re
import subprocess
import tempfile
from multiprocessing import Pool
from typing import Optional, Collection, Tuple, Dict

from tqdm import tqdm

from fastani.model import FastANIParameters, FastANIExecution
from fastani.model import write_genome_list

re_missing_file = re.compile(r'ERROR, skch::validateInputFiles, Could not open (.+)')


def execute_mp_wrapper(args: Tuple[FastANIParameters, Dict[str, str]]) -> FastANIExecution:
    """Required as multiprocessing pool will only allow one argument."""
    return execute(params=args[0], **args[1])


def execute(params: FastANIParameters, q: Optional[str] = None, ql: Optional[Collection[str]] = None,
            r: Optional[str] = None, rl: Optional[Collection[str]] = None) -> FastANIExecution:
    cmd = [params.exe]
    if q is not None:
        cmd.extend(['--query', q])
    if r is not None:
        cmd.extend(['--ref', r])
    cmd.extend(params.k_cmd)
    cmd.extend(params.cpu_cmd)
    cmd.extend(params.frag_len_cmd)
    cmd.extend(params.min_frac_cmd)
    cmd.extend(params.min_frag_cmd)

    with tempfile.TemporaryDirectory(prefix='fastani_') as temp_dir:

        # Set a temporary output file path if output is not set
        out_path = os.path.join(temp_dir, 'output.txt')
        cmd.extend(['--output', out_path])

        # Create a temporary file for the query/ref lists and write to disk
        if ql is not None:
            path_ql = os.path.join(temp_dir, 'query.txt')
            write_genome_list(ql, path_ql)
            cmd.extend(['--queryList', path_ql])
        if rl is not None:
            path_rl = os.path.join(temp_dir, 'reference.txt')
            write_genome_list(rl, path_rl)
            cmd.extend(['--refList', path_rl])

        # Run the proc
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            missing_file = re_missing_file.search(stderr)
            if missing_file:
                raise FileNotFoundError(missing_file.group(1))
            raise Exception(f'Failed to run {params.exe} with error: {stderr}')

        # Package the results and return them
        return FastANIExecution(' '.join(cmd), stdout, stderr, proc.returncode, output=out_path)


def process_queue(params: FastANIParameters, queue) -> Tuple[FastANIExecution]:
    # If only using one CPU, don't create a multiprocessing pool
    if params.cpus == 1 or len(queue) <= 1 or params.single_execution:
        return tuple([execute(params=params, **cmd) for cmd in queue])

    # Do single executions, i.e. force FastANI execution to be single threaded
    else:
        mp_cpus = params.cpus
        params.cpus = 1
        mp_queue = [(params, item) for item in queue]
        with Pool(processes=mp_cpus) as pool:
            return tuple(tqdm(pool.imap_unordered(execute_mp_wrapper, mp_queue), total=len(mp_queue)))
