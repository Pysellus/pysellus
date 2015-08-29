# Writing tests in Python

**Pysellus** works by running your tests automatically against all elements in a data stream, but to do that, you have to define your tests first.

In this section, we'll go over the process of writing a test file in Python 3.

---

## Getting started

Tests scripts in **pysellus** usually have the following sections:

- Defining your data streams.
- Writing your test functions (Optional).
- Setting up your data.
- Declaring your test case and testing your streams.

We will cover the basics on how to write a complete test script below.

#### Defining your data streams

The `stream` function takes care of converting our data to a stream. Usually you'll pass an `APIReader` definition to it, but you can use any Python iterable to get an stream. It returns a stream which you can use later.

```python
input = stream(YourOwnAPIReader)  # Connect to your own APIReader implementation

input = stream([1,2,3,4])  # getting a stream from a list

input = stream(some_file)  # you can read a file as a stream of lines
```

#### Writing your test functions

These are the functions you want the streams to test against, and they are just normal Python functions, with the only limitation that they must only receive one argument, which will be an element from the stream, and must return either `True` or `False`.

Test functions receive every element on the stream they test against, so you have complete control on how to inspect it. Even though you can, we recommend not to modify or alter the element in any way, as that could change how other tests behave.

```python
def is_positive(number):
    return number > 0
    
def contains_subkey(value):
    return 'subkey' in value
```

These test functions can also be used to filter our data streams, as we'll see below.

#### Setting up your data

Sometimes you want to focus only on certain parts of your data. For this purpose, you can `map`, `filter`, `merge` and `zip` your streams.

You can use either `lambda` or regular functions for any of these operations.

```python
input = stream(range(100))

def is_odd(n):
    return n % 2 != 0

odd = input.filter(is_odd)
# => 1, 3, 5..., 99

even = odd.map(lambda x: x - 1)
# => 0, 2, 3..., 98

original_input = odd.merge(even)
# => 0, 1, 2..., 99

combined = even.zip(odd, lambda left, right: (left, right))
# => (0, 1), (2, 3), (4, 5)..., (98, 99)
```

#### Declaring your test case and testing your streams

Finally, let's define some test cases.

Test cases have three parts: the failure notification, the test case function and description, and an optional test body, followed by an `expect` call:

```python
@on_failure('terminal')
def a_test():
    """this is a test, a very important test!"""
    expect(a_stream)(a_test)
```

In short, this construction tells **pysellus** to watch the `input` stream, pass each of its elements to the test functions and, if the test functions return `False`,
notify wherever it was declared with the call to `on_failure`.

##### Failure notification

This is the most important part of the test, as it lets **pysellus** know where it should notify of any errors happening inside this specific test case.
  
All test cases must have a failure notification, so make sure to put them in.

If you want to notify more than one place about errors, you can do so:

```python
@on_failure('slack', 'terminal')
```

##### Test case function and description

You can name your test case functions any way you like, as this is unimportant.

What is important, however, is the test docstring.

The very first line says what the test is about. Note that you **must** include a docstring. This will be what **pysellus** delivers, among other things, when notifying failures to an integration.

```python
def foo():
    """this is a test, a very important test!"""
```

Optionally, you can extend your docstring to include more details, in a different, blank-separated section. You can read more about notifications in [_Notification Protocol_]().

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
