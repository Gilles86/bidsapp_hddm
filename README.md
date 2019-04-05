# BIDS-app for HDDM
This Docker image is a BIDS-app that came out of the Brain Imaging Data Structure (BIDS) meeting at Princeton University, April 3-5, 2019.
It is a proof-of-principle example of how to make BIDS-apps that can estimate (cognitive) computational models. Specifically, it wraps the [HDDM](http://ski.clps.brown.edu/hddm_docs/)-package in such a way that it can fit, in principle, arbitrary BIDS-compliant behavioral datasets.

# Installation
To install the app you need to install [Docker](https://www.docker.com/get-started). 

You can then build the Docker image using
```
make docker-build
```

And run the example dataset using
```
make run
```

# Usage
This BIDS-app assumes you have your behavioral data ordered according to the [Brain imaging data structure-specification (BIDS)](http://bids.neuroimaging.io/). Specifically, the data should be structured according to like `_events.tsv`-files as described [here](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/05-task-events.html).

For example:
```
sub-01/
    func/
        sub-01_task-rdm_run-01_events.tsv
        sub-01_task-rdm_run-02_events.tsv
sub-02/
    func/
        sub-02_task-rdm_run-01_events.tsv
        sub-02_task-rdm_run-02_events.tsv
```

Data should look something like this:
```
onset	trial_type	response_time	response
1.486003119773947	hard	1.486003119773947	0
3.16089390411562	hard	0.6748907843416729	1
5.804000285185904	hard	1.6431063810702835	1
7.737937040907079	hard	0.9339367557211753	0
```
