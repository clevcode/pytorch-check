#!/usr/bin/env python3

import argparse
import colorama
import sys
import os

from . import check_file

success = True

colorama.init(autoreset=True)

def process(filename, options={}):
    global success
    print(colorama.Style.BRIGHT+f'--- Processing {filename}')
    if not check_file(filename, options):
        success = False
        print(colorama.Fore.RED+f'{filename} is potentially unsafe')

def main():
    global success
    progname = os.path.basename(sys.argv[0])
    parser = \
        argparse.ArgumentParser(
            prog=progname,
            description='Check PyTorch models for (overtly) unsafe code',
            epilog='Copyright (C) Joel Eriksson <je@clevcode.org> 2023')
    parser.add_argument(
        'target',
        metavar='PATH',
        help='Files and/or directories',
        type=str, nargs='+')
    parser.add_argument(
        '-t', '--trace',
        help='Safely trace the Pickle VM execution',
        action='store_true')
    parser.add_argument(
        '-d', '--dump',
        help='Dump the disassembly of all pickled bytecode',
        action='store_true')
    args = parser.parse_args()

    options = {}
    if args.trace:
        options['trace'] = True
    if args.dump:
        options['dump'] = True

    for path in args.target:
        # Check any files that were specified explicitly, since PyTorch
        # models may use any file extension even though .pt and .pth are
        # the ones that are most commonly used.
        if not os.path.exists(path):
            print(colorama.Fore.RED+f'{path} does not exist')
            success = False
        elif os.path.isfile(path):
            process(path, options)
        elif os.path.isdir(path):
            # For directories, just check .pt/.pth and .pkl/.pickle files
            for root, _, files in os.walk(path):
                for file in files:
                    ext = file.split('.')[-1].lower()
                    # NOTE! Other file extensions may be used as well!
                    if ext in ['ckpt', 'pt', 'pth', 'pkl', 'pickle']:
                        process(os.path.join(root, file), options)

if __name__ == '__main__':
    main()
    sys.exit(0 if success else 1)
