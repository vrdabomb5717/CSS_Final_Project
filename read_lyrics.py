#1/usr/bin/env python3

import argparse
import csv
import pdb

import lyrics_to_bow as ltb


class CommentedFile:
    def __init__(self, f, commentstring="#"):
        self.f = f
        self.commentstring = commentstring

    def __next__(self):
        line = next(self.f)

        while line.startswith(self.commentstring):
            line = next(self.f)
        return line

    def __iter__(self):
        return self


def read_lyrics_file(infile):
    """Read lyrics file.

    File is formatted as:

    # - comment, ignore
    %word1,word2,... - list of top words, in popularity order
    TID,MXMID,idx:cnt,idx:cnt,... - track ID from MSD, track ID from musiXmatch,
    then word index : word count (word index starts at 1!)

    """
    with infile:
        lyrics_reader = csv.reader(CommentedFile(infile), delimiter=',')
        words = next(lyrics_reader)

        # Remove % that begins the string.
        first_word = words[0]
        first_word = first_word.replace("%", "")
        words[0] = first_word

        for line in lyrics_reader:
            tid, mxmid, *counts = line
            split_counts = [i.split(":") for i in counts]
            pdb.set_trace()

        return words


def stuff(word, words):
    stemmed_word = ltb.lyrics_to_bow(word).keys()

    try:
        index = words.index(stemmed_word)
    except ValueError:
        print("Word could not be found.")


def main():
    parser = argparse.ArgumentParser(description="""Compute most frequent
                                     lyrics for each song.""")
    parser.add_argument("infilename", "--input", "-i", dest="infile",
                        help="Read from this file.", type=open)
    args = parser.parse_args()

    infile = args.infile
    words = read_lyrics_file(infile)


if __name__ == '__main__':
    main()
