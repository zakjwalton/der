#!/usr/bin/env python3.4

# File: main.py
# Author: Zak Walton
# Class: CIS 452
# Project: Experimental Study: File System Metrics

import argparse
import os, sys
import stat
import collections

def traverseFs(path, dirInfo):
    numFiles = 0
    sizeBytes = 0
    # loop through each file in this directory
    for f in os.listdir(path):
        pathname = os.path.join(path, f)
        statData = os.lstat(pathname)
        mode = statData.st_mode
        if stat.S_ISLNK(mode):
            # This is a symlink, only add the size
            sizeBytes += statData.st_size
        if stat.S_ISDIR(mode):
            # It's a directory, recurse into it
            dirInfo[pathname] = []
            size, num = traverseFs(pathname, dirInfo)
            sizeBytes += size
            numFiles += num
            dirInfo[pathname].append(size)
            dirInfo[pathname].append(numFiles)
        elif stat.S_ISREG(mode):
            # Its a file, add size and increment file count
            numFiles += 1
            sizeBytes += statData.st_size
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)

    return (sizeBytes, numFiles)

if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser(description='der.py - \'It\'s Basically du\'', conflict_handler='resolve')
    parser.add_argument('-h','--human-readable', dest = 'is_human', action = 'store_true')
    parser.add_argument('-o','--ordered', dest = 'is_ordered', action = 'store_true')
    parser.add_argument('path', nargs='?', default=os.curdir, help='Path to run this utility on')
    args = parser.parse_args()

    if args.is_human:
        print('This bitch is human')
    if args.path != None:
        print('Path is: ' + args.path)
        print(os.stat(args.path))
    # Call function to recurse through directory and put results in dictionary
    dirInfo = collections.OrderedDict()
    dirInfo[args.path] = []
    size, num = traverseFs(args.path, dirInfo)
    dirInfo[args.path].append(size)
    dirInfo[args.path].append(num)

    # Print output based on command line arguments
    print(dirInfo)
