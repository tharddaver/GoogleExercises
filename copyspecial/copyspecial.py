#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""


# Write functions and modify main() to call them
def get_special_paths(dirname):
    files = os.listdir(dirname)
    paths = []
    for filename in files:
        if re.search(r'__\w+__', filename):
            paths.append(os.path.abspath(os.path.join(dirname, filename)))

    return paths


def print_paths(paths):
    print '\n'.join(paths)


def copy_to(paths, todir):
    if not paths:
        return

    if not os.path.exists(todir):
        os.mkdir(todir)

    for path in paths:
        shutil.copy(os.path.basename(path), todir)


def zip_to(paths, zipfile):
    if not paths:
        return

    (status, output) = commands.getstatusoutput(
        'zip -j %s %s' % (zipfile, ' '.join(paths))
    )
    if status:
        sys.stderr.write(output)
        sys.exit(1)


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print "error: must specify one or more dirs"
        sys.exit(1)

    special_paths = []
    for dirname in args:
        special_paths += get_special_paths(dirname)

    print_paths(special_paths)

    if todir:
        copy_to(special_paths, todir)

    if tozip:
        zip_to(special_paths, tozip)


if __name__ == "__main__":
    main()
