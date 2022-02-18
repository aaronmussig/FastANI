import subprocess


def get_fastani_version(exe: str) -> str:
    """Determines the version of FastANI based on the executable help text."""

    proc = subprocess.Popen([exe, '--version'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, encoding='utf-8')
    stdout, stderr = proc.communicate()

    # Not supported, perhaps it's an older version
    if proc.returncode != 0:
        proc = subprocess.Popen([exe, '--help'], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, encoding='utf-8')
        stdout, stderr = proc.communicate()
        if proc.returncode != 0 and not 'fastANI is a fast alignment-free' in stderr:
            raise Exception('Could not determine FastANI version')
        if '--matrix' in stderr:
            return '1.1 or 1.2'
        else:
            return '1.0'
    else:
        return stderr.strip().split()[-1]
