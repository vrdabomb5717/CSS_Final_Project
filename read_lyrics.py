#!/usr/bin/env python3

import argparse
import csv

from nltk.corpus import stopwords
import numpy as np
from matplotlib import pyplot as plt, rc

import lyrics_to_bow as ltb


class CommentedFile:
    """Decorator to skip commented lines (start with #) in a CSV."""
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
                word, count = i

                try:
                    # Words are one-indexed
                    word = int(word) - 1
                    count = int(count)
                    increment = 1 if add_one else count
                    word_counts[word] += increment
                except ValueError:
                    print("Number could not be converted.")

        return word_counts, words, num_songs


def stem_word(word):
    """Use modified Porter-Stemmer to stem a given word."""
    stemmed_word = list(ltb.lyrics_to_bow(word).keys())
    stemmed_word = stemmed_word[0]
    return stemmed_word


def get_word_index(word, words):
    """Return the index that a word occurs in, or None if it's not there."""
    stemmed_word = stem_word(word)

    try:
        index = words.index(stemmed_word)
        return index
    except ValueError:
        print("Word could not be found.")
        return None


def plot_histogram(top_counts, words):
    """Plot lyrics distribution and save plots to disk."""
    counts = [count for count, word in top_counts]
    words = [words[word] for count, word in top_counts]

    rc('text', usetex=True)
    plt.hist(counts, bins=20)
    plt.title('Lyrics Distribution for 237,662 Tracks')
    plt.xlabel('Ranking of Word')
    plt.ylabel('Number of Tracks')
    plt.savefig('lyrics_histogram_10_bins.png')
    plt.clf()

    rc('text', usetex=True)
    plt.hist(counts, bins=len(words))
    plt.title('Lyrics Distribution of All {} Words'.format(len(words)))
    plt.xlabel('Ranking of Word')
    plt.ylabel('Number of Tracks')
    plt.savefig('lyrics_histogram_all_bins.png')
    plt.clf()


def bad_statistics(badfile, words, top_counts, num_songs):
    a = [count for count, word in top_counts]
    b = [words[word] for count, word in top_counts]

    bads = open(badfile)
    bads = bads.readlines()
    bads = list(map(lambda x: x.strip(), bads))
    bads = [x for x in bads if x.isalpha()]
    bad1 = list(map(stem_word, bads))
    bad2 = {(x, b.index(x)) for x in bad1 if x in words}
    bad2 = sorted(list(bad2), key=lambda x: x[1])

    print("Some statistics on swear words:")

    for word, rank in bad2:
        percentage = a[rank] / num_songs
        print("\tRank {}: {}, with {}%".format(rank, word, percentage * 100))


def main():
    parser = argparse.ArgumentParser(description="""Compute most frequent
                                     lyrics for each song.""")
    parser.add_argument("infilename",
                        help="Read from this file.", type=open)
    args = parser.parse_args()

    infile = args.infilename
    word_counts, words, num_songs = read_lyrics_file(infile)
    top_counts = [(x, i) for i, x in enumerate(word_counts)]
    top_counts = sorted(top_counts, key=lambda x: x[0], reverse=True)

    print("Number of songs: {}".format(num_songs))
    idx = get_word_index("baby", words)
    print("Percent of songs with baby: {}".format(word_counts[idx] / num_songs))

    idx = get_word_index("love", words)
    print("Percent of songs with love: {}".format(word_counts[idx] / num_songs))

    top_10 = top_counts[0:10]

    print("Top 10 Words:")
    for i, (count, word) in enumerate(top_10):
        percentage = count / num_songs
        print("\tRank {}: {} with {}%".format(i + 1, words[word], percentage * 100))

    print()
    stemmed_stopwords = list(map(stem_word, stopwords.words('english')))
    print("Top 10 Words that are not Stopwords:")

    words_printed = 0
    for count, word in top_counts:
        if words_printed < 10:
            if words[word] not in stemmed_stopwords:
                percentage = count / num_songs
                print("\tRank {}: {} with {}%".format(i + 1, words[word], percentage * 100))
                words_printed += 1

    plot_histogram(top_counts, words)

    print()
    bad_statistics("data/bad.txt", words, top_counts, num_songs)


if __name__ == '__main__':
    main()
