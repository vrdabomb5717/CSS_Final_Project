#1/usr/bin/env python3

import argparse
import csv
import heapq
import pdb

import nltk
import numpy as np

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


def read_lyrics_file(infile, add_one=True):
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
        word_counts = np.zeros(len(words), dtype=np.uint64)
        num_songs = 0

        for line in lyrics_reader:
            tid, mxmid, *counts = line
            num_songs += 1
            split_counts = [i.split(":") for i in counts]

            for i in split_counts:
                try:
                    word, count = i
                except ValueError:
                    pdb.set_trace()

                try:
                    # Words are one-indexed
                    word = int(word) - 1
                    count = int(count)
                    increment = 1 if add_one else count
                    word_counts[word] += increment
                except ValueError:
                    print("Number could not be converted.")

        return word_counts, words, num_songs


def get_word_index(word, words):
    stemmed_word = list(ltb.lyrics_to_bow(word).keys())
    stemmed_word = stemmed_word[0]

    try:
        index = words.index(stemmed_word)
        return index
    except ValueError:
        print("Word could not be found.")
        return None


def main():
    parser = argparse.ArgumentParser(description="""Compute most frequent
                                     lyrics for each song.""")
    parser.add_argument("infilename", "--input", "-i", dest="infile",
                        help="Read from this file.", type=open)
    args = parser.parse_args()

    infile = args.infile
    word_counts, words, num_songs = read_lyrics_file(infile)
    top_counts = [(x, i) for i, x in enumerate(word_counts)]
    heapq.heapify(top_counts)

    print("Number of songs: {}".format(num_songs))
    idx = get_word_index("baby", words)
    print("Percent of songs with baby: {}".format(word_counts[idx] / num_songs))

    idx = get_word_index("love", words)
    print("Percent of songs with love: {}".format(word_counts[idx] / num_songs))

    top_10 = heapq.nlargest(10, top_counts)

    print("Top 10 Words:")
    for i, (count, word) in enumerate(top_10):
        print("\tRank {}: {}".format(i + 1, words[word]))

    # print("Top 10 Words that are not Stopwords:")

if __name__ == '__main__':
    main()
