
[![Build Status](https://travis-ci.org/moonso/phizz.svg)](https://travis-ci.org/moonso/phizz)

# phizz #

Tool to query HPO and OMIM

## Installation ##

```pip install phizz```

or 

```
$git clone https://github.com/moonso/phizz.git
$cd phizz
$python setup.py install
```

## Usage ##

Using command line utility:

```
Usage: phizz query [OPTIONS]

  Query the hpo database.

  Print the result in csv format as default.

Options:
  -c, --config PATH
  -h, --hpo_term TEXT     Specify a hpo term
  -m, --mim_term TEXT     Specify a omim id
  -o, --outfile FILENAME  Specify path to outfile
  -j, --to_json           If output should be in json format
  --help                  Show this message and exit.
```

so trying:

```
$ phizz query -m OMIM:615373
#hpo_id	description
HP:0011675	Arrhythmia
HP:0001644	Dilated cardiomyopathy
HP:0001653	Mitral regurgitation
HP:0000006	Autosomal dominant inheritance
HP:0001711	Abnormality of the left ventricle
```
to json:

```
$ phizz query --hpo_term HP:0000002 --to_json
[{"hpo_term": "HP:0000002", "description": "Abnormality of body height"}]
```

Importing in python:

```
In [1]: import phizz

In [2]: phizz.query_disease(['OMIM:615373'])
Out[2]:
[{'description': u'Arrhythmia', 'hpo_term': u'HP:0011675'},
 {'description': u'Dilated cardiomyopathy', 'hpo_term': u'HP:0001644'},
 {'description': u'Mitral regurgitation', 'hpo_term': u'HP:0001653'},
 {'description': u'Autosomal dominant inheritance', 'hpo_term': u'HP:0000006'},
 {'description': u'Abnormality of the left ventricle',
  'hpo_term': u'HP:0001711'}]
```


