from typing import Optional, Collection, Union

from fastani.config import VERSIONS
from fastani.model import FastANIParameters, FastANIResults
from fastani.process import process_queue
from fastani.util import validate_paths
from fastani.version import get_fastani_version


def fastani(query: Union[str, Collection[str]],
            reference: Union[str, Collection[str]],
            k: Optional[int] = None,
            cpus: Optional[int] = None,
            frag_len: Optional[int] = None,
            min_frac: Optional[float] = None,
            min_frag: Optional[int] = None,
            single_execution: bool = True,
            bidirectional: bool = False,
            exe: str = 'fastANI') -> FastANIResults:
    """
    :param query: Path to the query genome(s).
    :param reference: Path to the reference genome(s).
    :param k: kmer size <= 16 (default: 16)
    :param cpus: Number of CPUs to use for parallel execution (default: 1)
    :param frag_len: fragment length (default: 3,000)
    :param min_frac: minimum fraction of genome that must be shared for
                     trusting ANI (default: 0.2) [version >= 1.3]
    :param min_frag: minimum matched fragments for trusting ANI (default: 50)
                     [version <= 1.2].
    :param single_execution: True if --refList and --queryList should be
                  used, otherwise a subprocess will be launched to do 1:1
                  comparisons.
    :param bidirectional: True if the ANI should be calculated for query
                          vs reference and vice-versa.
    :param exe: The path to the execution file.
    """

    # Transform input to a collection
    query = validate_paths(query)
    reference = validate_paths(reference)

    # Nullify version-specific arguments
    version = VERSIONS.index(get_fastani_version(exe))
    params = FastANIParameters(version=version, exe=exe,
                               k=k, cpus=cpus, frag_len=frag_len,
                               min_frac=min_frac, min_frag=min_frag,
                               single_execution=single_execution,
                               bidirectional=bidirectional)

    # Create the queue
    queue = list()

    # Run the single execution (query/reference lists) and return the results
    if params.single_execution:
        queue.append({'ql': query, 'rl': reference})
        if params.bidirectional:
            queue.append({'ql': reference, 'rl': query})

    # Generate a queue of commands
    else:
        for query_path in query:
            for reference_path in reference:
                queue.append({'q': query_path, 'r': reference_path})
                if params.bidirectional:
                    queue.append({'q': reference_path, 'r': query_path})

    # Process the queue and return the result
    executions = process_queue(params, queue)
    return FastANIResults(query=query, reference=reference, executions=executions, params=params)
