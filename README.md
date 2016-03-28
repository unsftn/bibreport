A tool for generating reports from BibTex files.


Installation
============

You must have a working installation of Python and pip tool.

I suggest using of [python
virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).


Clone this repository (or [download
zip](https://github.com/igordejanovic/bibreport/archive/master.zip) and unpack)
and do:

```
$ python setup.py install
```


Usage
=====

Report on all references:

```
$ bibreport myrefs.bib
```

Report on references for a specific year:

```
$ bibreport myrefs.bib 2015
```

Report on references for a range of years:

```
$ bibreport myrefs.bib 2011-2015
```

Each command above produces `bibreport.html` report.

