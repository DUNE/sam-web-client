# SAM Web Client

This Python code allows client-side access to SAM Web.

This repository on DUNE GitHub is a fork of upstream code from FNAL in
order to provide proper Python packaging.

## Installation

Installation from PyPI:

```
$ pip install sam-web-client
```

Installation from source

```
$ cd sam-web-client
$ python setup.py install
```

## Branches

- `upstream` pristine FNAL's master branch
- `master` tracks `upstream` with merges at releases.

## Versions

Packaged releases on PyPI are labeled with tags on `master` which are
associated with tags on `upstream`.  The `upstream` tag convention
appears to be `vX_Y_Z` (with `_Z` optional).  Each packaged release
will mimic the upstream release with as `X.Y.Z`.
