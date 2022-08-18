#!/usr/bin/python3

from xmltv import *
import datetime
import sys
import argparse


def readfiltered(filein, channellist, dateinterval):
    if filein == "-":
        fd = sys.stdin
    else:
        fd = open(filein)

    et = ElementTree()
    tree = et.parse(fd)

    df = read_data(tree=tree)
    ch = read_channels_dict(tree=tree, chfilter=channellist)
    pr = read_programmes_dict(tree=tree, chfilter=channellist, minstart=dateinterval)
    if filein != "-":
        fd.close()

    return df, ch, pr


def main():
    # define argument parser
    parser = argparse.ArgumentParser(description="""
    Filter and merge xmltv files. This program reads one or more xmltv
    files, optionally keeping only channels in a specified list and/or
    programmes starting after a specified date and outputs the results of
    filtering and merging the input. Time zones are ignored at the moment
    in date computations, however they are correctly kept in output.""")

    parser.add_argument("--ch-list", metavar="comma-separated list", type=str, default="",
                        help="list of channels (id's) to keep in output")
    parser.add_argument("--back", metavar="days", type=int, default=None,
                        help="keep programmes starting up to many days back")
    parser.add_argument("--start", metavar="YYYYmmddHHMM", type=int, default=None,
                        help="keep programmes starting after the indicated date, alternative to --back")
    parser.add_argument("--verbose", action="store_true",
                        help="increase verbosity")
    parser.add_argument("files", metavar="file", type=str, nargs="+",
                        help="input files and output file, - for stdin/stdout")

    args = parser.parse_args()

    # process arguments
    if args.back is None and args.start is None:
        minstamp = 0
    elif args.back is not None:
        minstamp = int((datetime.datetime.now() - datetime.timedelta(days=args.back)).timestamp)
    else:
        minstamp = timestamp_from_xmltvtime(str(args.start))

    if args.ch_list == "":
        chfilt = None
    else:
        chfilt = args.ch_list.split(",")

    ch = {}
    pr = {}
    nofilt = minstamp == 0 and chfilt is None
    # read, filter and merge input
    for infile in args.files[:-1]:
        if args.verbose:
            print(f"reading{'' if nofilt else ' and filtering'} "+infile)
        df, ch1, pr1 = readfiltered(infile, chfilt, minstamp)
        if args.verbose:
            print(f"{len(ch1)} channels and {len(pr1)} programmes {'read' if nofilt else 'filtered'} from {infile}")
        ch.update(ch1)
        pr.update(pr1)

    if args.verbose:
        print(f"{len(ch)} channels and {len(pr)} programmes obtained after merging")

    # write the result, df (general data) is ignored for the moment
    w = Writer(encoding="UTF-8")
    for c in ch.values():
        w.addChannel(c)
    for p in pr.values():
        w.addProgramme(p)

    if args.verbose:
        print("writing to "+args.files[-1])
    if args.files[-1] == "-":
        fd = sys.stdout.buffer
    else:
        fd = open(args.files[-1], "wb")
    w.write(fd, pretty_print=True)
    if args.files[-1] != "-":
        fd.close()

if __name__ == '__main__':
	main()
