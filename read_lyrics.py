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


def plot_histogram(counts):
    """Plot lyrics distribution and save plots to disk."""
    rc('text', usetex=True)
    ind = np.arange(len(counts)) + 1
    plt.bar(ind, counts)
    plt.title('Lyrics Distribution for 237,662 Tracks')
    plt.xlabel('Ranking of Word')
    plt.ylabel('Number of Tracks')
    plt.savefig('data/graphs/lyrics_histogram.png')
    plt.clf()


def bad_statistics(badfile, words, counts, num_songs):
    """Calculate statistics on swear words."""
    bads = open(badfile)
    bads = bads.readlines()
    bads = [x.strip() for x in bads]
    bads = [x for x in bads if x.isalpha()]
    bad1 = list(map(stem_word, bads))
    bad2 = {(x, words.index(x)) for x in bad1 if x in words}
    bad2 = sorted(list(bad2), key=lambda x: x[1])

    print("Some statistics on swear words:")

    for word, rank in bad2:
        percentage = counts[rank] / num_songs
        print("\tRank {}: {}, with {}%".format(rank, word, percentage * 100))


def main():
    parser = argparse.ArgumentParser(description="""Compute most frequent
                                     lyrics for each song.""")
    parser.add_argument("infilename",
                        help="Read from this file.", type=open)
    args = parser.parse_args()

    infile = args.infilename
    word_counts, words, num_songs = read_lyrics_file(infile)
    top_counts = ((x, i) for i, x in enumerate(word_counts))
    top_counts = sorted(top_counts, key=lambda x: x[0], reverse=True)
    b = [words[word] for count, word in top_counts]

    print("Number of songs: {}".format(num_songs))
    idx = get_word_index("baby", words)
    rank = b.index(stem_word("baby"))
    print("baby: Rank {} with {}%".format(rank, (word_counts[idx] / num_songs) * 100))

    idx = get_word_index("love", words)
    rank = b.index(stem_word("love"))
    print("love: Rank {} with {}%".format(rank, (word_counts[idx] / num_songs) * 100))

    top_10 = top_counts[0:10]

    print()
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
                rank = b.index(words[word])
                percentage = count / num_songs
                print("\tRank {}: {} with {}%".format(rank + 1, words[word], percentage * 100))
                words_printed += 1

    counts = np.array([count for count, word in top_counts])

    print()
    print("Statistics on the Distribution:")
    print("\tcount: {}".format(len(counts)))
    print("\tmean: {}".format(np.mean(counts)))
    print("\tstd: {}".format(np.std(counts)))
    print("\tmin: {}".format(np.min(counts)))
    print("\t25%: {}".format(np.percentile(counts, .25)))
    print("\t50%: {}".format(np.percentile(counts, .50)))
    print("\t75%: {}".format(np.percentile(counts, .75)))
    print("\tmax: {}".format(np.max(counts)))

    plot_histogram(counts)

    print()
    bad_statistics("data/bad.txt", b, counts, num_songs)


if __name__ == '__main__':
    main()
