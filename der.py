#!/usr/bin/env python3.4

# File: main.py
# Author: Zak Walton
# Class: CIS 452
# Project: Experimental Study: File System Metrics

import argparse
import os, sys
import stat
import collections
import math

fileTypeCnt = {}

def traverseFs(path, dirInfo):
    numFiles = 0
    sizeBytes = 0
    # Add size of my file
    sizeBytes += os.lstat(path).st_size
    # loop through each file in this directory
    for f in os.listdir(path):
        pathname = os.path.join(path, f)
        statData = os.lstat(pathname)
        mode = statData.st_mode
        if stat.S_ISLNK(mode):
            # This is a symlink, only add the size
            sizeBytes += statData.st_size
        elif stat.S_ISDIR(mode):
            # It's a directory, recurse into it
            size, num = traverseFs(pathname, dirInfo)
            sizeBytes += size
            numFiles += num
            dirInfo[pathname] = []
            dirInfo[pathname].append(size)
            dirInfo[pathname].append(num)
        elif stat.S_ISREG(mode):
            # Its a file, add size and increment file count
            numFiles += 1
            sizeBytes += statData.st_size
            # Check if file type is in dictionary and increment count
            splitPath = f.split('.')
            if (len(splitPath) > 1):
                type = splitPath[-1]
                if type not in fileTypeCnt:
                    fileTypeCnt[type] = 1
                else:
                    fileTypeCnt[type] += 1
        else:
            # Unknown file type, print a message
            pass

    return (sizeBytes, numFiles)


def readable(num):
    num = int(num)
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if abs(num) < 1024:
            if abs(num) < 9.9:
                num = math.ceil(num*10)/10
                return '{:.1f}{}'.format(num, unit)
            return '{:.0f}{}'.format(num, unit)
        num = num/1024
    return 'Number too big!!'


if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser(description='der.py - \'It\'s Basically du\'', conflict_handler='resolve')
    g = parser.add_mutually_exclusive_group()
    g.add_argument('-h','--human-readable', dest = 'is_human', action = 'store_true')
    g.add_argument('-o','--ordered', dest = 'is_ordered', action = 'store_true')
    g.add_argument('-c','--count', dest = 'is_count', action = 'store_true')
    g.add_argument('-f','--filetype', dest = 'is_filetype', action = 'store_true')
    parser.add_argument('path', nargs='?', default=os.curdir, help='Path to run this utility on')
    args = parser.parse_args()

    # Verify that the path is valid
    if (os.path.exists(args.path) != True):
        print('Ivalid input, try again.')
        sys.exit()

    # Call function to recurse through directory and put results in dictionary
    dirInfo = collections.OrderedDict()
    size, num = traverseFs(args.path, dirInfo)
    dirInfo[args.path] = []
    dirInfo[args.path].append(size)
    dirInfo[args.path].append(num)

    # Print output based on command line arguments
    if args.is_ordered:
        # Print ordered output
        for key,value in sorted(dirInfo.items(), key=lambda e: e[1][0], reverse=True):
            print('{}\t{}'.format(value[0],key))
    elif args.is_human:
        # Print human readable output
        for key,value in dirInfo.items():
            print('{}\t{}'.format(readable(value[0]),key))
    elif args.is_count:
        # Print file count
        for key,value in dirInfo.items():
            print('{}\t{}'.format(value[1],key))
    elif args.is_filetype:
        for key,value in sorted(fileTypeCnt.items(), key=lambda e: e[1], reverse=True)[0:19]:
            print('{},{}'.format(key, value))
    else:
        # Print normal ouput in bytes
        for key,value in dirInfo.items():
            print('{}\t{}'.format(value[0],key))
