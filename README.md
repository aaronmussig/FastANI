# FastANI

![PyPI](https://img.shields.io/pypi/v/fastani)


This package has been developed to provide a Python interface to the
[FastANI](https://github.com/ParBLiSS/FastANI) tool.

## Installation

Note: You must install the FastANI binaries yourself for this package to work.

This package only has standard dependencies and works for Python versions >=3.6.

```shell
pip install fastani
```

## Basic Usage

Note: All features except for the matrix and visualization method have been implemented.

To use this package, simply call the `fastani` method, all parameters except for the
`query` and `reference` arguments are optional, and in this case the FastANI default values are used.

The `query` and `reference` arguments can either be a string, or collection of strings that point to the fasta file(s).

```python
from fastani import fastani

result = fastani(query='query.fna', reference='reference.fna')
dict_results = result.as_dict()

# Accessing results
print(dict_results['query.fna']['reference.fna'].ani)         # 89.1234
print(dict_results['query.fna']['reference.fna'].n_frag)      # 50
print(dict_results['query.fna']['reference.fna'].total_frag)  # 100
print(dict_results['query.fna']['reference.fna'].align_frac)  # 0.5

# Writing results to disk
result.to_file('results.txt')
```

The FastANI default parameters can be overridden by passing the following arguments:

* `exe`: The path to the FastANI binary.
* `k`: The kmer size to use.
* `cpus`: The number of CPUs to use.
* `frag_len`: Fragment length to use.
* `min_frac`: Minimum fraction of genome shared.
* `min_frag`: Minimum number of aligned fragments `(version < 1.3)`.

## Advanced Usage

There are two additional arguments that can be supplied to the `fastani` method:

* `single_execution`: If set to `True` (default), FastANI will use the query and reference list parameters. If set
  to `False`, then each genome will be analysed individually.
* `bidirectional`: If set to `False` (default), FastANI will only perform a `query -> reference` comparison. If set
  to `True`, then a `reference -> query` comparison will also be performed.
