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