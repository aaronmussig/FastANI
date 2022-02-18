from fastani.model import FastANIResult

GENOMES = {'a': '/genomes/GCA_001873845.1.fna.gz',
           'b': '/genomes/GCA_002783845.1.fna.gz',
           'c': '/genomes/GCA_002789105.1.fna.gz',
           'd': '/genomes/GCA_001886815.1.fna.gz'}

KNOWN_ANI = {
    'a': {
        'b': FastANIResult(ani=99.2035, n_frag=249, total_frag=417),
        'c': FastANIResult(ani=98.6394, n_frag=225, total_frag=417),
        'd': None
    },
    'b': {
        'a': FastANIResult(ani=99.5265, n_frag=249, total_frag=282),
    },
    'c': {
        'a': FastANIResult(ani=99.4333, n_frag=224, total_frag=254),
    },
    'd': {
        'a': None,
    }
}

EXE = ('fastANI_1.0', 'fastANI_1.1', 'fastANI_1.2', 'fastANI_1.3',
       'fastANI_1.31', 'fastANI_1.32', 'fastANI_1.33')
