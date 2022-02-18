from typing import Collection, Dict, FrozenSet, Iterator, Tuple, Optional

from fastani.config import VERSIONS
from fastani.logger import log


class FastANIParameters:
    __slots__ = ('version', 'exe', 'single_execution', 'k', 'cpus', 'frag_len',
                 'min_frac', 'min_frag', 'bidirectional')

    def __init__(self, version: int, exe: str,
                 single_execution: bool = True,
                 bidirectional: bool = False,
                 k: Optional[int] = None,
                 cpus: Optional[int] = None,
                 frag_len: Optional[int] = None,
                 min_frac: Optional[float] = None,
                 min_frag: Optional[int] = None):

        # Nullify parameters not specific to the current version
        if cpus is not None and version == VERSIONS.index('1.0'):
            cpus = None
            log.warning('Multi-threading is not supported in this version and will be ignored')
        if min_frac is not None and version < VERSIONS.index('1.3'):
            min_frac = None
            log.warning('Minimum fraction is not supported in this version and will be ignored')
        if min_frag is not None and version > VERSIONS.index('1.1 or 1.2'):
            min_frag = None
            log.warning('Minimum fragments is not supported in this version and will be ignored')

        # Validate the parameters
        cpus = max(1, cpus) if cpus is not None else None
        self.validate(k=k, frag_len=frag_len, min_frac=min_frac, min_frag=min_frag)

        # Set the parameters
        self.version = version
        self.exe = exe
        self.k = k
        self.cpus = cpus
        self.frag_len = frag_len
        self.min_frac = min_frac
        self.min_frag = min_frag

        self.single_execution = single_execution
        self.bidirectional = bidirectional

    @property
    def k_cmd(self):
        return ('-k', str(self.k)) if self.k is not None else tuple()

    @property
    def cpu_cmd(self):
        return ('-t', str(self.cpus)) if self.cpus is not None else tuple()

    @property
    def frag_len_cmd(self):
        return ('--fragLen', str(self.frag_len)) if self.frag_len is not None else tuple()

    @property
    def min_frac_cmd(self):
        return ('--minFraction', str(self.min_frac)) if self.min_frac is not None else tuple()

    @property
    def min_frag_cmd(self):
        return ('--minFrag', str(self.min_frag)) if self.min_frag is not None else tuple()

    @staticmethod
    def validate(k: Optional[int], frag_len: Optional[int],
                 min_frac: Optional[float], min_frag: Optional[int]):
        errors = list()
        # kmer size
        if k is not None and (k > 16 or k < 1):
            errors.append('kmer size must be between 1 and 16')
        # fragment length
        if frag_len is not None and frag_len < 1:
            errors.append('fragment length must be greater than 0')
        # minimum fraction size
        if min_frac is not None and (min_frac > 1.0 or min_frac < 0):
            errors.append('minimum fraction must be between 0 and 1')
        # minimum fragment size
        if min_frag is not None and min_frag < 0:
            errors.append('minimum fragments must be greater than 0')
        # report errors
        if len(errors) > 0:
            raise ValueError('\n'.join(errors))


class FastANIExecution:
    """The input, output and logs of a single FastANI execution."""

    __slots__ = ('cmd', 'stdout', 'stderr', 'return_code', 'output')

    def __init__(self, cmd: str, stdout: str, stderr: str, return_code: int,
                 output: str):
        self.cmd: str = cmd
        self.stdout: Optional[str] = stdout if stdout else None
        self.stderr: Optional[str] = stderr if stderr else None
        self.return_code: int = return_code
        self.output: Optional[ResultFile] = ResultFile(output) if output else None


class FastANIResult:
    __slots__ = ('ani', 'n_frag', 'total_frag', 'align_frac')

    def __init__(self, ani: float, n_frag: int, total_frag: int):
        self.ani: float = ani
        self.n_frag: int = n_frag
        self.total_frag: int = total_frag
        self.align_frac: float = n_frag / total_frag

    def __repr__(self):
        return f'ANI={self.ani}, AF={self.align_frac:.4f}'

    def __eq__(self, other):
        return isinstance(other, FastANIResult) and \
               self.ani == other.ani and \
               self.n_frag == other.n_frag and \
               self.total_frag == other.total_frag

    def to_delimited_str(self, delimiter: str = '\t') -> str:
        return delimiter.join(map(str, (self.ani, self.n_frag, self.total_frag,
                                        round(self.align_frac, 4))))


class FastANIResults:
    """The summary of a FastANI method request."""

    __slots__ = ('query', 'reference', 'params', 'executions')

    def __init__(self, query: FrozenSet[str], reference: FrozenSet[str],
                 executions: Tuple[FastANIExecution], params: FastANIParameters):
        self.query = query
        self.reference = reference
        self.params = params
        self.executions: Tuple[FastANIExecution] = executions

    def iter_results(self) -> Iterator[Tuple[str, str, Optional[FastANIResult]]]:
        """Returns an iterator of the query, reference, and results.
        NOTE: This will only return those which had >=80% ANI."""
        for execution in self.executions:
            if execution.output:
                for (qry, ref), result in execution.output.data.items():
                    yield qry, ref, result

    def as_dict(self) -> Dict[str, Dict[str, Optional[FastANIResult]]]:
        """Returns the results as a dictionary of query -> reference values."""

        # The output dictionary must be seeded with the query/reference genomes
        out = dict()
        for q in self.query:
            out[q] = dict()
            for r in self.reference:
                out[q][r] = None
                # Bidirectional case
                if self.params.bidirectional:
                    if r not in out:
                        out[r] = dict()
                    out[r][q] = None

        # Process the executions
        error = False
        for qry, ref, result in self.iter_results():
            out_result = out[qry][ref]
            if out_result is not None and out_result != result:
                error = True
                log.error(f'Duplicate and differing values, data is corrupt: {qry, ref, result, out_result}')
            else:
                out[qry][ref] = result
        if error:
            raise ValueError('Corrupt data')

        return out

    def to_file(self, path: str):
        with open(path, 'w') as f:
            for qry, ref_dict in sorted(self.as_dict().items(), key=lambda x: x[0]):
                for ref, result in sorted(ref_dict.items(), key=lambda x: x[0]):
                    cols = [qry, ref]
                    if result is not None:
                        cols.extend([result.ani, result.n_frag, result.total_frag,
                                     round(result.align_frac, 4)])
                    else:
                        cols.extend(['<80%', 'n/a', 'n/a', 'n/a'])
                    f.write('\t'.join(map(str, cols)) + '\n')
        log.info(f'Wrote results to {path}')


class ResultFile:
    """A wrapper to the FastANI output file."""

    __slots__ = ('data',)

    def __init__(self, path):
        self.data: Dict[Tuple[str, str], FastANIResult] = self.read(path)

    def __repr__(self):
        if len(self.data) == 0:
            return 'N/A'
        else:
            return f'{len(self.data):,} comparisons'

    @staticmethod
    def read(path):
        out = dict()
        with open(path) as f:
            for line in f.readlines():
                data = line.strip().split()
                if len(data) != 5:
                    raise Exception(f'Malformed output file: {line}')
                out[(data[0], data[1])] = FastANIResult(float(data[2]), int(data[3]), int(data[4]))
        return out


def write_genome_list(genomes: Collection[str], path: str):
    """Write a collection of genome names to the query/reference list file."""
    with open(path, 'w') as f:
        for genome_path in genomes:
            f.write(f'{genome_path}\n')
