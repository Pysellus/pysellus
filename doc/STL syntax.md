# STL - Stream Testing Language

STL is just a DSL on top of Python 3 and its usage is completely optional. If you want to write your tests directly in Python, head over to the [Python syntax]() section.

---

## Getting started

Test scripts in pysellus usually have the following sections:

- Defining your data streams.
- Writing your test functions (Optional).
- Setting up your data.
- Declaring your test case and testing your streams.

We will cover the basics on how to write a complete test script below.

#### Defining your data streams

The `stream` function takes care of converting our data to a stream. Usually you'll pass an `APIReader` definition to it, but you can use any python iterable to get an stream.

```python
input = stream(YourOwnAPIReader)  # Connect to your own APIReader implementation

input = stream([1,2,3,4])  # getting a stream from a list

input = stream(some_file)  # you can read a file as a stream of lines
```

#### Writing your test functions

These are the functions you want the streams to test against, and they are just normal Python functions, with the only limitation that they only receive one argument, and have to return either `True` or `False`.

Test functions receive every element on the stream they test against, so you have complete control on how to inspect it. Even though you can, we recommend not to modify or alter the element in any way, as that could change how other tests behave.

```python
def is_positive(number):
    return number > 0
    
def contains_subkey(value):
    return 'subkey' in value
```

These test functions can also be used to filter our data streams, as we'll see below.

#### Setting up your data

Some times you want to focus only on certain parts of your data. For this purpose, you can `map`, `filter`, `merge` and `zip` streams.

You can use either `lambda` or regular functions for any of these operations.

```python
input = stream(range(100))

def is_odd(n):
    return n % 2 != 0

odd = input.filter(is_odd)
# => 1, 3, 5..., 99

even = even.map(lambda x: x - 1)
# => 0, 2, 3..., 98

original_input = odd.merge(even)
# => 0, 1, 2..., 99

combined = even.zip(odd, lambda l, r: (l, r))
# => (0, 1), (2, 3), (4, 5)..., (98, 99)
```

#### Declaring your test case and testing your streams

Finally, let's define some test cases.

Test cases have three parts: the failure notification, the test description, and an optional test body, followed by an `expect` call:

```python
@failure >> terminal
@check 'this is a test, a very important test!':
    expect(a_stream)(a_test)
```

##### Failure Notification

This is the most important part of the test, as it lets pysellus know where it should notify of any errors happening inside this specific test case.
  
All test cases must have a failure notification, so make sure to put them in.

If you want to notify more than one place about errors, you can do so. All the following ways are allowed and have the same final result:

```python
@failure >> slack, terminal

@failure >> slack >> terminal

@failure >> slack
@failure >> terminal
```

##### Test Description

This tells you why a test exists. Also, it will be what gets delivered, among other things, to any places you want to notify when an error happens.

All test descriptions must begin with `@check` as this is what lets pysellus know that this is a test case.

```python
@check 'this is a test, a very important test!':
```

All UTF-8 characters are supported in the description, so you don't have to worry about them getting filled with weird symbols.

##### Test Body

Inside the test body, you can further specify your data, as we saw in _Setting up your data_.

The only part that you must include in a test is an `expect` call. It follows the form `expect(stream)(test)`.

```python
expect(input)(a_test)
expect(input)(another_test)
```

You can also pass multiple tests, like so:

```python
expect(input)(test_1, test_2, ..., test_n)
```