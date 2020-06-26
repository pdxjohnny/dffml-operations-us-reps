name: Testing

on:
  push:
    branches:
      - master

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [ '3.7' ]
    name: Python ${{ matrix.python-version }} sample
    steps:
      - uses: actions/checkout@v2
      - name: Setup python
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
          architecture: x64
      - run: python setup.py test
