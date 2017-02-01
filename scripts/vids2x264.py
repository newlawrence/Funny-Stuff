#!/Users/alberto/anaconda/bin/python

from os import system
import sys
from pathlib import Path


def apply_to_dirs(i_dir, o_dir, function, extensions, tab=0, **kwargs):

    try:
        dirs = [d for d in i_dir.iterdir() if d.is_dir()]
        dirs.reverse()
        dirnames = [d.name for d in dirs]
        files = [f for f in i_dir.iterdir()
                 if f.is_file() and '.' in f.name and
                 f.name[f.name.rindex('.') + 1:].lower() in extensions]
        filenames = [f.name for f in files]
    except PermissionError:
        sys.exit('Error: unable to access subfolder in {}.'
                 .format(i_path))

    print(2 * tab * ' ' + '|-' + i_dir.name)
    while len(dirs) > 0:
        dirname = dirnames.pop()
        dest_dirs = [d.name for d in o_dir.iterdir() if d.is_dir()]
        next_dir = o_dir.joinpath(dirname)
        if dirname not in dest_dirs:
            next_dir.mkdir()
        apply_to_dirs(dirs.pop(), next_dir, function,
                      extensions, tab + 1, **kwargs)

    counter = 0
    for file in filenames:
        counter += 1
        s = (2 * tab * ' ' + '|   ' + '[{} of {}] Processing {}...'
             .format(counter, len(filenames), file))
        print(s, end='\r')
        function(file, i_dir, o_dir, **kwargs)
        print(len(s) * ' ', end='\r')
    if len(filenames) > 0:
        print(2 * tab * ' ' + '|   ' + 'Done!')


def convert_to_mp4(file, i_dir, o_dir, **kwargs):

    scaled = '-vf scale=-1:{} '.format(kwargs['scaled'])
    cheap = '-crf 26 ' if kwargs['cheap'] else ' '
    threaded = '-threads 0 ' if kwargs['threaded'] else ' '
    overwrite = '-y ' if kwargs['overwrite'] else '-n '

    i_file = file
    o_file = file[:file.rindex('.')] + '.mp4'
    i_dir = str(i_dir.joinpath(i_file).absolute())
    o_dir = str(o_dir.joinpath(o_file).absolute())
    system('ffmpeg -i "{}" -c:v libx264 {}-profile:v baseline -acodec '
           'aac -strict -2 -ar 44100 -ac 2 -b:a 128k -movflags faststart '
           '{}{}{}"{}"'.format(i_dir, scaled, threaded,
                               overwrite, cheap, o_dir))


if __name__ == '__main__':

    print('vids2x264 - ffmpeg Python wrapper for recursive x264 encoding')
    usage = ('Usage: vids2x264 <input file/dir> <output dir> '
             '[-t] [-y]\n'
             '    -s<size>: resize video to given vertical size.\n'
             '    -b: reduce bitrate to achieve smaller file size.\n'
             '    -t: enable default multithreading for ffmpeg.\n'
             '    -y: overwrite existing files.')

    extensions = ['avi', 'mpeg', 'mod', 'mkv', 'mp4']
    r = -1
    b = False
    t = False
    y = False

    class IPathError(OSError): pass
    class OPathError(OSError): pass

    try:
        i_path = Path(sys.argv[1])
        if not i_path.is_dir() and not i_path.is_file():
            raise IPathError
        o_path = Path(sys.argv[2])
        if not o_path.is_dir():
            raise OPathError
        if len(sys.argv) > 3:
            b = True if '-b' in sys.argv[3:] else False
            t = True if '-t' in sys.argv[3:] else False
            y = True if '-y' in sys.argv[3:] else False
            for argument in sys.argv[3:]:
                if '-s' in argument:
                    try:
                        r = int(argument[2:])
                    except ValueError:
                        r = -1
    except IndexError:
        print(usage)
        sys.exit('Error: at least two arguments expected.')
    except IPathError:
        print(usage)
        sys.exit('Error: {} invalid input path.'.format(i_path))
    except OPathError:
        print(usage)
        sys.exit('Error: {} invalid output path.'.format(o_path))

    if i_path.is_dir():
        apply_to_dirs(i_path, o_path, convert_to_mp4,
                      extensions, scaled=r, cheap=b, threaded=t, overwrite=y)
    else:
        if i_path.name[i_path.name.rindex('.') + 1:].lower() in extensions:
            s = 'Processing {}...'.format(i_path.name)
            print(s, end='\r')
            convert_to_mp4(i_path.name, i_path.parent, o_path,
                           scaled=r, cheap=b, threaded=t, overwrite=y)
            print(len(s) * ' ', end='\r')
            print('Done!')
