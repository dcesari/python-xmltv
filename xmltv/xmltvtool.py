#!/usr/bin/python3

from xmltv import *
import datetime
import sys
import argparse


def read_filtered(filein, filt):
    if filein == "-":
        fd = sys.stdin
    else:
        fd = open(filein)

    df, ch, pr = read_stream(fd, filt)

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
    filt = InputFilter()
    if args.back is not None:
        filt.add(minstart=int((datetime.datetime.now() - datetime.timedelta(days=args.back)).timestamp()))
    elif args.start is not None:
        filt.add(minstart=timestamp_from_xmltvtime(str(args.start)))

    if len(args.ch_list) > 0:
        filt.add(chlist=args.ch_list.split(","))

    ch = {}
    pr = {}
    # read, filter and merge input
    for infile in args.files[:-1]:
        if args.verbose:
            print(f"reading and filtering "+infile)
        df, ch1, pr1 = read_filtered(infile, filt)
        if args.verbose:
            print(f"{len(ch1)} channels and {len(pr1)} programmes filtered from {infile}")
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
