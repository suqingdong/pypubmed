import os


def show_args(args):
    msg = []
    for k, v in args.items():
        msg += ['{:15}:\t{}'.format(k, v)]
    return '\n'.join(msg)


def safe_open(filename, mode='r'):
    if 'w' in mode:
        dirname = os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

    if filename.endswith('.gz'):
        import gzip
        return gzip.open(filename, mode=mode)

    return open(filename, mode=mode)
