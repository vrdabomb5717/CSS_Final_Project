Title: Computational Social Science Final Project    
Author: Varun Ravishankar    
        Viktor Roytman     
Email:  vr2263@columbia.edu    
       vr2262@columbia.edu   
Date: May 10th, 2013     

# Analyzing the Million Song Database
## Computational Social Science Final Project

This program analyzes the [Million Song Dataset], a free-for-noncommerical-use dataset made available to analyze audio features and metadata for a million contemporary songs.

### Dependencies

This program was tested on OS X 10.8.3 and Fedora 18 using Python 3.3. The program may run on older versions of Python; however, these are untested and unsupported.

Dependency versions that have been tested are listed here. Older versions of Python modules such as numpy or matplotlib may work as well; however, you will most likely need to install the development versions of NLTK and PyTables for the newly-added Python 3 support.

* Bash 3.0 or greater
* wget
* Python 3.2 or greater
* numpy 1.7.1
* matplotlib 1.2.1
* libpng
* NLTK 3.0a1 (install using ```pip3 install git+git://github.com/nltk/nltk.git```)
* pandas 0.11.0
* PyTables 3.0.0b1 for HDF5 support (install using ```pip3 install git+https://github.com/PyTables/PyTables.git@develop#egg=tables```)

You should just be able to run ```pip3 install -r requirements.txt``` and let it install all the dependencies. However, if this does not work for some reason, the dependencies have been listed for a manual install.

### Usage

First, clone the repository and add it to your ```PYTHONPATH```. Then, download the data using the provided shell script, ```download_msd.sh```. This will download the lyrics dataset and will prepare it for analysis. It will also download the MSD dataset, a total of 1 GB. This will take a while, so expect the script to run for at least a couple of minutes.

[Million Song Dataset]: http://labrosa.ee.columbia.edu/millionsong/

Next, you can run the Python scripts.

See an example below that starts off in the cloned repo:

```
$ pip3 install -r requirements.txt
$ ./download_msd.sh
$ python3 -O read_lyrics.py data/mxm.txt
$ python3 -O duration_v_time.py
$ python3 -O duration_histogram.py
$ python3 -O loudness_v_time.py
$ python3 -O loudness_histogram.py
$ python3 -O tempo_v_time.py
$ python3 -O tempo_histogram.py
```

### Output

All output graphs are located in ```data/graphs```.

```
Fri May 10 01:03 PM CSS_Final_Project $ ./read_lyrics.py data/mxm.txt
Number of songs: 237662
baby: Rank 110 with 13.34668562917084%
love: Rank 37 with 30.893874494029333%

Top 10 Words:
    Rank 1: the with 79.27266454039771%
    Rank 2: a with 77.18608780537065%
    Rank 3: to with 75.42812902357129%
    Rank 4: and with 74.0198264762562%
    Rank 5: i with 73.25319150726662%
    Rank 6: you with 70.17192483442872%
    Rank 7: in with 67.35574050542367%
    Rank 8: is with 64.62539236394544%
    Rank 9: me with 63.57558212924237%
    Rank 10: it with 62.91329703528541%

Top 10 Words that are not Stopwords:
    Rank 29: know with 38.56401107455125%
    Rank 35: like with 33.34188890104434%
    Rank 37: time with 31.49725240046789%
    Rank 38: love with 30.893874494029333%
    Rank 43: see with 29.391741212309917%
    Rank 44: come with 28.83254369651017%
    Rank 45: go with 28.819079196505964%
    Rank 46: one with 28.484149758901296%
    Rank 50: get with 26.738393180230744%
    Rank 53: never with 25.17609041411753%

Statistics on the Distribution:
    count: 5000
    mean: 3809.0664
    std: 12624.514851113743
    min: 73
    25%: 120.0
    50%: 151.99
    75%: 179.4925
    max: 188401

Some statistics on swear words:
    Rank 294: fuck, with 5.174575657867055%
    Rank 333: hell, with 4.474421657648256%
    Rank 360: shit, with 4.137388391917933%
    Rank 416: blow, with 3.5104476104720153%
    Rank 593: ass, with 2.2645605944576754%
    Rank 614: bitch, with 2.1391724381684916%
    Rank 628: nigga, with 2.082789844400872%
    Rank 936: fuckin, with 1.3014280785316963%
    Rank 1093: sex, with 1.055280187829775%
    Rank 1286: dick, with 0.8777170940242865%
    Rank 1330: niggaz, with 0.8436350783886359%
    Rank 1469: flip, with 0.7237168752261616%
    Rank 1753: whore, with 0.5840226876825071%
    Rank 1972: sexi, with 0.5057602814080501%
    Rank 2018: cock, with 0.4897711876530535%
    Rank 2141: pussi, with 0.4430662032634582%
    Rank 2168: bastard, with 0.43717548451161736%
    Rank 2246: screw, with 0.41908256263096333%
    Rank 2491: gay, with 0.36690762511465863%
    Rank 3392: fucker, with 0.23731181257415995%
    Rank 3401: crap, with 0.23647028132389694%
    Rank 3596: carpet, with 0.21837735944324294%
    Rank 3691: slut, with 0.21038281256574462%
    Rank 3723: asshol, with 0.2078582188149557%
    Rank 3927: cum, with 0.19018606255943313%
    Rank 4693: cunt, with 0.12875428129023572%

Fri May 10 03:33 PM CSS_Final_Project $ ./duration_histogram.py
Statistics on the Distribution:
    count: 1000000
    mean: 4.158345916560894 minutes
    std: 2.103826216761537 minutes
    min: 0.005217 minutes
    25%: 0.29648216666666666 minutes
    50%: 0.45321700000000004 minutes
    75%: 0.5790400000000001 minutes
    max: 50.581761166666666 minutes

Fri May 10 03:34 PM CSS_Final_Project $ ./loudness_histogram.py
Statistics on the Distribution:
    count: 1000000
    mean: -10.124039260000012 dBFS
    std: 5.197242141465852 dBFS
    min: -58.178 dBFS
    25%: -33.031 dBFS
    50%: -30.256 dBFS
    75%: -28.538007500000003 dBFS
    max: 4.318 dBFS

Fri May 10 03:35 PM CSS_Final_Project $ ./tempo_histogram.py
Statistics on the Distribution:
    count: 996770
    mean: 124.2906773578665 bpm
    std: 34.39484368551902 bpm
    min: 7.362 bpm
    25%: 39.7719225 bpm
    50%: 45.023535 bpm
    75%: 50.002 bpm
    max: 302.3 bpm

```