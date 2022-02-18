from typing import Collection, Union, FrozenSet

from fastani.logger import log


def validate_paths(paths: Union[str, Collection[str]]) -> FrozenSet[str]:
    """Validate the query/reference input."""
    out = set()
    if isinstance(paths, str):
        out.add(paths)
    elif isinstance(paths, Collection):
        for path in paths:
            if path not in out:
                out.add(path)
            else:
                log.warning(f'Duplicate path ignored: {path}')
    else:
        raise ValueError('paths must be a string or a collection of strings')
    return frozenset(out)
