from fickling.analysis import check_safety
from fickling import pickle, tracing

import pickletools
import zipfile
import sys
import io

if sys.version_info >= (3, 9):
    from ast import unparse
else:
    from astunparse import unparse

def check(file_or_buf, options={}):
    pickled = pickle.Pickled.load(file_or_buf)
    if 'trace' in options:
        trace = tracing.Trace(pickle.Interpreter(pickled))
        print(unparse(trace.run()))
    result = check_safety(pickled)
    if 'dump' in options:
        f = io.BytesIO()
        pickled.dump(f)
        f.seek(0)
        pickletools.dis(f)
    return result

def check_pytorch(filename, options={}):
    result = True
    with zipfile.ZipFile(filename, 'r') as zipped:
        for filename in zipped.namelist():
            if filename.endswith('.pkl') or filename.endswith('.debug_pkl'):
                print(f'Embedded pickle file {filename}')
                with zipped.open(filename, 'r') as file:
                    if not check(file.read(), options):
                        result = False
            elif filename.endswith('.py'):
                # Not sure if this is used or just included for reference?!
                print(f'Embedded Python file {filename}')
            else:
                # Just ignore any data files for now
                pass
    return result

def check_file(filename, options={}):
    try:
        ext = filename.split('.')[-1].lower()
        if ext in ['pkl', 'pickle']:
            # If it's a .pkl/.pickle file, check it directly
            return check(open(filename, 'rb'), options)
        else:
            # Otherwise assume it's a PyTorch model file
            return check_pytorch(filename, options)
    except Exception as e:
        print(f'Exception {e} while checking {filename}')
        return False
