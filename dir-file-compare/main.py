import os, filecmp, config

def get_flist(rootdir):
    result = []
    for (dirpath, dirnames, filenames) in os.walk(rootdir):
        result += [dirpath + os.path.sep + fname for fname in filenames]
    return set(result)

def fileEq(fileL, fileR):
    return filecmp.cmp(fileL, fileR)

def fuck(fl):
    return os.path.basename(os.path.splitext(fl)[0])

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
            out_csv.append('未找到,{}'.format(fuck(fl)))
        elif len(libFile) > 1:
            print('DUPLICATE: Input `{}` has multiple candidate `{}` in library.'.format(fl, libFile))
            out_csv.append('库文件重复,{},重名库文件,{}'.format(fuck(fl), libFile))
        else:
            if not fileEq(libFile[0], fl):
                print('NOT_MATCH: {} != {}'.format(fl, libFile[0]))
                out_csv.append('与库文件不匹配,{}'.format(fuck(fl)))

    fname = config.working_dir + os.path.sep + os.path.basename(inputPath) + '.csv'
    with open(fname, 'w+') as f:
        f.write('\n'.join(out_csv)) # Windows M$ excel also not accepting \r\n





