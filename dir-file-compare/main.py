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
        print('Usage: ./this.py <dir path>')
        return

    inputPath = argv[1]
    libFlist = get_flist(config.library_path)
    for fl in get_flist(inputPath):
        libFile = list(filter(lambda f: os.path.basename(f) == os.path.basename(fl), libFlist))
        if len(libFile) == 0:
            print('NOT_FOUND: {}'.format(fl))
        elif len(libFile) > 1:
            print('DUPLICATE: Input `{}` has multiple candidate `{}` in library.'.format(fl, libFile))
        else:
            if not fileEq(libFile[0], fl):
                print('NOT_MATCH: {} != {}'.format(fl, libFile[0]))

    input('============== PRESS ENTER TO EXIT =============')





