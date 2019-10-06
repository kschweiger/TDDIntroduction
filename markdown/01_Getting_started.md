# 1. Getting started

## Terminology
Test-driven development comes with a lot of terminilogy that the reader should be familiar with. Different kinds of tests like **unit-tests** and **integration-tests**. 
For modern programming languages, there are **testing frameworks** (or test runner), that help oganizing, automating and formalizing tests. For python, commonly used ones are `unittest` (included in the standard library) or `pytest`.

### Unit-test
The most basic way of testing is the unit-test. It denotes a test that tests a single function.     
The idea of a unit-test is that a function is called with a defined input (called the **test step**) and the return value is compared to the expected output (called the **test assertion**). 

### Integration-test
An integration-test, tests if different components of your application interact in the expected way. This makes unit-tests so important when following the test-driven approach. If the integration-test fails, a good set of unit-test can help with finding the problem quickly.

### Testing frameworks

#### unittest 
The unittest module is part of the python standard library since 2.1 and therefore can be used in almost any installation without problems. Setting a tests with unittest requires 

- To put your test into class (inheriting from `unittest.TestCase`) methods 
- Use a set of special assertion methods from the `unittest.TestCase` modules instead of the built-in assertion.


#### pytest
[Pytest](https://pytest.org/en/latest/) builds on the foundations of unittest (and works very similar) but simplifies the how tests have to written and evaluated. In contrast to `unittest` the tests in `pytest` do not need 

- to be be a method of a `unittest.TestCase`-type class or 
- use the special assertion methods.

Other great features are:

- tests are functions just have to start with `test_`
- Executing `pytest` form the CLI offers nice output 
- A large number of additional plugins

### Other commonly used terms

#### coverage
For coverage the test runner records with lines of the code are actually run during the tests. The ratio between executed lines and all lines of the code is called the coverage. Ideally to coverage of your project should be as high as possible.

#### mock
A mock is a object that acts as a outside dependency with defined attributes. This is e.g. required if your test need some input from a third party dependency which you don't want to test. More on this will be covered in [Add link]().

#### side effect
Often looking at the return value is not the only thing a test need to check. A piece of code will often alter e.g. some class atribute. This is called a **side effect**.

## Writing your first test
Let's start with testing the built-in `sum` function. The obvious unit-test for the sum function is, if the sum works correction when passing a list of values (that python can add). Let's create a file [`firstTest.py`](../examples/ch1/firstTest.py):

```python
import unittest

class TestSum(unittest.TestCase):
    def test_sum(self):
        res = sum([2, 4, 6])
        self.assertEqual(res, 12)
```

As discussed previously `unittest` requires all test to be a method in a classes inheriting from `unittest.TestCase`-class. In this examples the test `test_sum` executes the sum of 2,4 and 6 and we check with ` self.assertEqual` if the sum is equal to 12 (which is true in this case :wink:). To execute this test from the CLI you would run:

```bash
python -m unittest firstTest.py
```

This returns:

```bash
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

Unsurpisingly this worked out great. If we change the expected value to 11 (which is obviously wrong but for the sake of this introduction we want to see the output) we get:

```bash
F
======================================================================
FAIL: test_sum (firstTest.TestSum)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "TDDIntroduction/examples/ch1/firstTest.py", line 7, in test_sum
    self.assertEqual(res, 11)
AssertionError: 12 != 11

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

We immediately see, that the test fails. Checking the output more closely, it tells you which assertion failed (`self.assertEqual(res, 11)`) and why (`AssertionError: 12 != 11`). Let's revert it back to 12 and go on.

----

Another commonly used test one want to run is, if exepctions are handled as expected. `unittest` provides special syntax for this with the `self.assertRaises` method.      
We know that the sum returns a `TypeError` if a values is passed that can not be summed (like a `string`). So let's add a test to our `TestSum` class:

```
def test_sum_fail_str(self):
	with self.assertRaises(TypeError):
   		res = sum("SOMESTRING")
```

Running `unittest` again yields:

```bash
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

You see that the runner now ran 2 test and both where successful.

----
The same tests but using `pytest` can be found in the file: [`firstTest_pytest.py`](../examples/ch1/firstTest_pytest.py). The runner now is started with `python -m pytest firstTest_pytest.py`

Note: `pytest` needs to be installed with `pip intall pytest` first.



