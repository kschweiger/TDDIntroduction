# The Basics

This chapter will cover 

- testing return values,
- testing erros and
- test parametrization

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


## Practival Example: A calculator

The following code examples will be wrtitting using the `pytest` testing framework. All the concepts are transferrable to the `unittest` framework.

-------

Let's start with a simple class structure:

```python
class Calculator:
    def __init__(self):

    def add(self, v1, v2):
        pass

    def substract(self, v1, v2):
        pass
    
    def multiply(self, v1, v2):
        pass
        
    def divide(self, v1, v2):
        pass
        
```

Before further wrinting the actual class methods, let's start with writing tests:

```python
from calculator import Calculator
import pytest

def test_calculator_add():
    theCalculator = Calculator()
    
    assert theCalculator(2,6) == 8

def test_calculator_substract():
    theCalculator = Calculator()
    
    assert theCalculator(6,2) == 4

def test_calculator_multiply():
    theCalculator = Calculator()
    
    assert theCalculator(6,2) == 12

def test_calculator_divide():
    theCalculator = Calculator()
    
    assert theCalculator(6,2) == 3
```

Running the test file result (obviously) in 4 failed test, since we did not implement anything in the calculator class. So lets change that.

```python
class Calculator:
    def __init__(self):
        pass
    
    def add(self, v1, v2):
        return v1 + v2

    def substract(self, v1, v2):
        return v1 - v2
    
    def multiply(self, v1, v2):
        return v1 * v2
        
    def divide(self, v1, v2):
        return v1 / v2
```

No all tests pass. At this point we can think about cleaning the test code a bit. One thing we notice is that we have to initialize the calculator each time. In `pytest` we can use a fixture to change this by adding the following the test file:

```python 
@pytest.fixture(scope="module")
def theCalculator():
    calculator = Calculator()

    return calculator
``` 

In this case, `scope="module"` means it will be initialized once per test script execution. Now we can use this initialized calculator in all test by passing `theCalculator` as function argument. Which leaves us with:

```python
from calculator import Calculator
import pytest


@pytest.fixture(scope="module")
def theCalculator():
    calculator = Calculator()

    return calculator

def test_calculator_add(theCalculator):
    assert theCalculator.add(2,6) == 8

def test_calculator_substract(theCalculator):
    assert theCalculator.substract(6,2) == 4

def test_calculator_multiply(theCalculator):
    assert theCalculator.multiply(6,2) == 12

def test_calculator_divide(theCalculator):
    assert theCalculator.divide(6,2) == 3
```

Let's parametrize the tests so we can check that the caluclator does not only work by chance with the number we choose. In `pytest` parametrization is also added via a function decorator: `@pytest.mark.parametrize()`.

The syntax here a bit confusing. Inside the decorator, first a the parameter names (string) are set. And then a list is passed as the next parameter. The list contains tuples for each set of paramters to be tested. The elements in the tuple need to correspond to the number of parameter names. In case of one paramter we can just pass a list of values.

```
@pytest.mark.parametrize("v1, v2", [(2, 6), (1, 2), (1.2, 3.2)])
```

This decorator results in three test (since the list contains 3 tuples). Let's add this to the tests:

```
from calculator import Calculator
import pytest


@pytest.fixture(scope="module")
def theCalculator():
    calculator = Calculator()

    return calculator

@pytest.mark.parametrize("v1, v2", [(2, 6), (1, 2), (1.2, 3.2)])
def test_calculator_add(theCalculator, v1, v2):
    assert theCalculator.add(v1, v2) == v1+v2

@pytest.mark.parametrize("v1, v2", [(2, 6), (1, 2), (1.2, 3.2)])
def test_calculator_substract(theCalculator, v1, v2):
    assert theCalculator.substract(v1, v2) == v1-v2

@pytest.mark.parametrize("v1, v2", [(2, 6), (1, 2), (1.2, 3.2)])
def test_calculator_multiply(theCalculator, v1, v2):
    assert theCalculator.multiply(v1, v2) == v1*v2

@pytest.mark.parametrize("v1, v2", [(2, 6), (1, 2), (1.2, 3.2)])
def test_calculator_divide(theCalculator, v1, v2):
    assert theCalculator.divide(v1, v2) == v1/v2
```

In the current form the addition will work with a lot of datatypes in python since the basic operators often mean something for them. But let's say we only want it to work with `int` and `float`. We could just add a check to the class but let's start from the tests again and add:

```python
@pytest.mark.parametrize("v1, v2", [(["2"], ["6"]), ("2","6")])
def test_calculator_add_execption(theCalculator, v1, v2):
    with pytest.raises(TypeError):
        theCalculator.add(v1, v2)
```

Running now leads to failing tests:

```
================================== FAILURES ==================================
___________________ test_calculator_add_execption[v10-v20] ___________________

theCalculator = <calculator.Calculator object at 0x10b975cc0>, v1 = ['2']
v2 = ['6']

    @pytest.mark.parametrize("v1, v2", [(["2"], ["6"]), ("2","6")])
    def test_calculator_add_execption(theCalculator, v1, v2):
        with pytest.raises(TypeError):
>           theCalculator.add(v1, v2)
E           Failed: DID NOT RAISE <class 'TypeError'>

test_calculator.py:18: Failed
_____________________ test_calculator_add_execption[2-6] _____________________

theCalculator = <calculator.Calculator object at 0x10b975cc0>, v1 = '2'
v2 = '6'

    @pytest.mark.parametrize("v1, v2", [(["2"], ["6"]), ("2","6")])
    def test_calculator_add_execption(theCalculator, v1, v2):
        with pytest.raises(TypeError):
>           theCalculator.add(v1, v2)
E           Failed: DID NOT RAISE <class 'TypeError'>

test_calculator.py:18: Failed
======================== 2 failed, 12 passed in 0.10s ========================
```

So let's add some check to the class method:

```
	def add(self, v1, v2):
        if not (isinstance(v1, int) or isinstance(v1, float)):
            raise TypeError
        if not (isinstance(v2, int) or isinstance(v2, float)):
            raise TypeError
        
        return v1 + v2
```

Now all tests are passing. We probably want that for all methods so let's add the tests for the others. After adding just the same tests (just changing the calcualtor method) we see that the test are passing even if we don't add a check. The reason is that python raises TypeErrors for i.e. when strings are multiplied anyways. But e.g. a int and string can be multiplied w/o problems so let's change the parametrization to:

`@pytest.mark.parametrize("v1, v2", [(2, ["6"]), (2,"6")])`.

As expcted the test fail now. Adding the same type check to the multiplication method makes them pass again. We should probably add type combinations like this to the other test aswell. Technically we would not need to add the check to substraction (since it always raises a type error) but we can use this and add a custom error message so the user knows why it fails in any case. 

With this we arrive at the following for the **tests**

```python
from calculator import Calculator
import pytest


@pytest.fixture(scope="module")
def theCalculator():
    calculator = Calculator()

    return calculator

@pytest.mark.parametrize("v1, v2", [(2, 6), (1, 2), (1.2, 3.2)])
def test_calculator_add(theCalculator, v1, v2):        
    assert theCalculator.add(v1, v2) == v1+v2
        
@pytest.mark.parametrize("v1, v2", [(2, 6), (1, 2), (1.2, 3.2)])
def test_calculator_substract(theCalculator, v1, v2):
    assert theCalculator.substract(v1, v2) == v1-v2

@pytest.mark.parametrize("v1, v2", [(2, 6), (1, 2), (1.2, 3.2)])
def test_calculator_multiply(theCalculator, v1, v2):
    assert theCalculator.multiply(v1, v2) == v1*v2

@pytest.mark.parametrize("v1, v2", [(2, 6), (1, 2), (1.2, 3.2)])
def test_calculator_divide(theCalculator, v1, v2):
    assert theCalculator.divide(v1, v2) == v1/v2

@pytest.mark.parametrize("v1, v2", [(["2"], ["6"]), ("2","6")])
def test_calculator_add_execption(theCalculator, v1, v2):
    with pytest.raises(TypeError):
        theCalculator.add(v1, v2)

@pytest.mark.parametrize("v1, v2", [(["2"], ["6"]), ("2","6")])
def test_calculator_substract_execption(theCalculator, v1, v2):
    with pytest.raises(TypeError):
        theCalculator.substract(v1, v2)

@pytest.mark.parametrize("v1, v2", [(2, ["6"]), (2,"6")])
def test_calculator_multiply_execption(theCalculator, v1, v2):
    with pytest.raises(TypeError):
        theCalculator.multiply(v1, v2)
```

And the **class**:

```python
class Calculator:
    def __init__(self):
        pass
    
    def add(self, v1, v2):
        if not (isinstance(v1, int) or isinstance(v1, float)):
            raise TypeError("%s is not type float or int")
        if not (isinstance(v2, int) or isinstance(v2, float)):
            raise TypeError("%s is not type float or int")
        
        return v1 + v2

    def substract(self, v1, v2):
        if not (isinstance(v1, int) or isinstance(v1, float)):
            raise TypeError("%s is not type float or int")
        if not (isinstance(v2, int) or isinstance(v2, float)):
            raise TypeError("%s is not type float or int")

        return v1 - v2
    
    def multiply(self, v1, v2):
        if not (isinstance(v1, int) or isinstance(v1, float)):
            raise TypeError("%s is not type float or int")
        if not (isinstance(v2, int) or isinstance(v2, float)):
            raise TypeError("%s is not type float or int")
        return v1 * v2
        
    def divide(self, v1, v2):
        if not (isinstance(v1, int) or isinstance(v1, float)):
            raise TypeError("%s is not type float or int")
        if not (isinstance(v2, int) or isinstance(v2, float)):
            raise TypeError("%s is not type float or int")

        return v1 / v2
```



We now notice that this is quite convoluted. The type check is the same in all method. So let's **refactor**! By moving the type check to a staticmethod we can get rid of a bit code and improve readability and maintainability:

```python
class Calculator:
    def __init__(self):
        pass
    
    def add(self, v1, v2):
        self.checkInputType(v1)
        self.checkInputType(v2)
        
        return v1 + v2

    def substract(self, v1, v2):
        self.checkInputType(v1)
        self.checkInputType(v2)

        return v1 - v2
    
    def multiply(self, v1, v2):
        self.checkInputType(v1)
        self.checkInputType(v2)
        
        return v1 * v2
        
    def divide(self, v1, v2):
        self.checkInputType(v1)
        self.checkInputType(v2)

        return v1 / v2
        
    @staticmethod
    def checkInputType(var):
        if not (isinstance(var, int) or isinstance(var, float)):
            raise TypeError("%s is not type float or int")
```

Now we can run the tests again to make sure that everything still works. It does :D

The final python file can be found here: [Class](examples/ch1/calculator.py) and [Tests](examples/ch1/test_calculator.py)