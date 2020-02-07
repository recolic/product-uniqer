import os, filecmp, config

def get_flist(rootdir):
    result = []
    for (dirpath, dirnames, filenames) in os.walk(rootdir):
        result += [dirpath + os.path.sep + fname for fname in filenames]
    return set(result)

def fileEq(fileL, fileR):
    return filecmp.cmp(fileL, fileR)


def main(argv):
    if len(argv) != 2:
        raise RuntimeError('Missing arg! Usage: ./this.py <dir path>')

    inputPath = argv[1]
    libFlist = get_flist(config.library_path)
    out_csv = []

    for fl in get_flist(inputPath):
        libFile = list(filter(lambda f: os.path.basename(f) == os.path.basename(fl), libFlist))
        if len(libFile) == 0:
            print('NOT_FOUND: {}'.format(fl))
            out_csv.append('未找到,{}'.format(fl))
        elif len(libFile) > 1:
            print('DUPLICATE: Input `{}` has multiple candidate `{}` in library.'.format(fl, libFile))
            out_csv.append('库文件重复,{},重名库文件,{}'.format(fl, libFile))
        else:
            if not fileEq(libFile[0], fl):
                print('NOT_MATCH: {} != {}'.format(fl, libFile[0]))
                out_csv.append('与库文件不匹配,{},!=,{}'.format(fl, libFile[0]))

    fname = os.path.dirname(argv[0]) + os.path.sep + 'out.csv'
    with open(fname, 'w+') as f:
        f.write('\n'.join(out_csv)) # Windows M$ excel also not accepting \r\n





