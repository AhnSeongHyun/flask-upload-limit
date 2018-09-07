
def get_python_version():
    import sys
    major, minor, _, _, _ = sys.version_info
    return int('{}{}'.format(major, minor))

