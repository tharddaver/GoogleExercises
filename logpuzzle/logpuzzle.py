#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
import posixpath

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def sorting_function(url):
    matches = re.search('-\w+-(\w+)\.\w+', url)
    if matches:
        return matches.group(1)

    return url


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    if not os.path.exists(filename):
        sys.stderr.write('File does not exist')
        sys.exit(1)

    filename_parts = filename.split('_')
    if len(filename_parts) < 2:
        sys.stderr.write('Cannot get the host')
        sys.exit(1)

    host = filename_parts[1]
    urls = []

    pattern = r'GET\s+([\S]*puzzle[\S]*)\s+HTTP'
    input_file = open(filename)
    for line in input_file:
        matches = re.search(pattern, line)
        if matches:
            image_url = 'http://' + host + matches.group(1)
            if image_url not in urls:
                urls.append('http://' + host + matches.group(1))
    input_file.close()

    return sorted(urls, key=sorting_function)

  

def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if not img_urls:
        sys.stderr.write('No images to load')
        sys.exit(1)

    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    html = '<verbatim><html><body>'

    for img_url in img_urls:
        try:
            filename = posixpath.basename(img_url)
            urllib.urlretrieve(img_url, os.path.join(dest_dir, filename))
            html += '<img src="%s" />' % filename
        except IOError:
            sys.stderr.write('Could not read url' + img_url)

    html += '</body></html>'

    html_file = open(os.path.join(dest_dir, 'index.html'), 'w')
    html_file.write(html)
    html_file.close()


def main():
    args = sys.argv[1:]

    if not args:
        print 'usage: [--todir dir] logfile '
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print '\n'.join(img_urls)


if __name__ == '__main__':
    main()
