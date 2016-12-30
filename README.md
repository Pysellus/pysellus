# Pysellus - A monitor and alerting system for your data

<img src="https://www.dropbox.com/s/kncye6uq629bgup/pysellus-logo.png?raw=1" alt="Pysellus logo" align="right"/>

[![Build Status](https://travis-ci.org/Pysellus/pysellus.svg)](https://travis-ci.org/Pysellus/pysellus)
[![Coverage Status](https://coveralls.io/repos/Pysellus/pysellus/badge.svg?branch=master&service=github)](https://coveralls.io/github/Pysellus/pysellus?branch=master)

---

Pysellus is a stream-based, monitoring and alerting service that runs automatic tests against your data.

### What would I use this for?

- Filtering, merging and cleaning your data.
- Searching for schemas and information in large, real-time data streams.
- Setting up automatic alerts, notifications and triggers that run whenever a match happens.

### Requirements

Pysellus is written in [Python 3](https://www.python.org/downloads/release/python-343/), so you will need to have it installed.

Additionally, if you want to install Pysellus with `pip`, you will need to have `pip3` installed.

### Installation

You can get Pysellus just by running:

```
$ pip3 install pysellus
```

Or you can go ahead and clone this repo, and install it (needs [setuptools](https://pypi.python.org/pypi/setuptools))

```
$ python3 setup.py install
```

### Getting started

Pysellus works by running some user-defined tests against all elements in a data stream.

Let's get started by writing a very basic test:

```python
input = stream([0, 1, 2, 3])

def is_positive(number):
    return number > 0

@failure >> terminal
@check 'all numbers should be positive':
    expect(input)(is_positive)
```

Save this to a file, for example `test.stl`, and then run it with pysellus:

```
$ pysellus test.stl
```

This will print to the terminal:

```
Assert error: In all numbers should be positive, got: 0
```

In the previous example, you wrote your tests in STL, or _Stream Testing Language_. This is just a thin DSL layer over regular Python, and its usage is completely optional.

You can read about the full STL syntax in the official [documentation](./doc/STL\ syntax.md), or learn how to write your tests in [regular Python](./doc/Python\ Test\ Syntax.md).

### Usage

**Pysellus** is installed as a command-line application. To use it, just call `pysellus`, passing either your test directory or file path.

```
$ pysellus [-d|--dir] /path/to/test/dir,
           [-f|--file] /path/to/test/file
```

### Documentation

- [User Guide](.) - In Progress
- [STL Syntax](./doc/STL\ syntax.md)
- [Python Syntax](./doc/Python\ Test\ Syntax.md)
- [Integrations](./doc/Integrations.md)
- [Adding your own API](.) - In Progress
- [Custom Integrations](./doc/Integrations.md#custom-integrations)
- [Notification Protocol](.) - In Progress

### Contributing

Contributors are welcome. Please fork the repository and send a pull request to the `master` branch.

Additionally, you can read the [*Contributing*](./CONTRIBUTING.md) file.

## License

Pysellus is released under the MIT License. For more information, see the [License](./LICENSE)
