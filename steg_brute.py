#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from progressbar import ProgressBar, Percentage, Bar
from argparse import ArgumentParser
import commands
import os


class color:
    FAIL = '\033[91m'
    BLUE = '\033[94m'
    BLUE2 = '\033[1;36m'
    INFO = '\033[93m'
    ENDC = '\033[0m'
    GREEN = '\033[1;32m'

    
VERSION = "1.0"

SAMPLES = """
Type ./steg_brute.py -h to show help

Command line examples:

    1- Get info of file
    ./steg_brute.py -i -f <file>

    2- Extract hide info of file with password
    ./steg_brute.py -e -p <password> -f <file>

    3- Brute force attack with dictionary to
       extract hide info of file
    ./steg_brute.py -b -d <dictionary> -f <file>

    """


def Steg_brute(ifile, dicc):
    with open(dicc, 'r') as passFile:
        for line in passFile.readlines():
            passwd = line.strip('\n')
            if (steghide(ifile, passwd)):
                break

def get_info(ifile, passwd, ofile):
    # Execute steghide 
    r = commands.getoutput("steghide extract -sf %s -p '%s' -xf %s -f" % (ifile, passwd, ofile))
    if not "no pude extraer" in r and not "could not extract" in r:
        return True
    else:
        return False


def steghide(ifile, passwd):
    # Output file name
    ofile = ifile.split('.')[0] + "_flag.txt"
    if get_info(ifile, passwd, ofile):
        print("\n\n [+] " + color.INFO + "Information obtained with password: " + color.GREEN + passwd + color.ENDC)
        return True
    else:
        print("\n\n [+] " + color.INFO  + "No info obtained with password: " + color.FAIL + passwd + color.ENDC)
        return False


def main():
    argp = ArgumentParser(
            description="Steghide Brute Force Tool",
            usage="./steg_brute.py [options] [-f image_file]",
            version="Steghide Brute Force Tool v" + VERSION)

    argp.add_argument('-i', '--info', dest='info', action='store_true',
                      help='Get info of file')

    argp.add_argument('-f', '--file', dest='file', required=True,
                      help='Path of file')

    argp.add_argument('-e', '--extract', dest='extract', action='store_true',
                      help='Extract hide info with password')

    argp.add_argument('-p', '--password', dest='password',
                      help='Password to extract hide info')

    argp.add_argument('-b', '--brute', dest='brute', action='store_true',
                      help='Brute force attack with dictionary')

    argp.add_argument('-d', '--dictionary', dest='dicc',
                      help='Path of dictionary to brute force attack')

    args = argp.parse_args()

    if args.info and not args.extract and not args.brute:
        os.system("steghide info %s" % (args.file))

    elif args.extract and not args.info and not args.brute:
        steghide(args.file, args.password)

    elif args.brute and not args.info and not args.extract:
        print("\n [i] " + color.INFO + "Searching..." + color.ENDC)
        Steg_brute(args.file, args.dicc)

    else:
        print(SAMPLES)


if __name__ == "__main__":
    main()
