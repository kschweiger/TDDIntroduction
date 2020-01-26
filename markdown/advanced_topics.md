# Advanced Topics

This chapter will cover advanced topics that will be very usefull when testing more complicated code. 

Also in this chapter the examples will be for the `pytest` module.

## Mocking external dependencies

When testing your code/class/framework you proabably use external modules or file that you either don't want to test or can't test. Mocking is a way to simulates the dependecies (or what you excpet as input for your functions) within a testing framework.

A extended introduction can be found [here on RealPython](https://realpython.com/python-mock-library/).

### Patching 

One common usuage is to patch a function of an external dependency.     
Let's say, that your project includes a operations with the filesystem via `remove` function of the `os` module. 

In principl you could write a test that creates a file in the test step, then calles the function and then checks if the function is still on the file system in the test assertion step.   

Instead you can patch `os.remove`:

```python
import os
import pytest

class FS:
    @staticmethod
    def removeFile(filename):
        os.remove(filename)

def test_fs_remove(mocker):
    mocker.patch('os.remove')
    FS.removeFile("filename.txt")
    os.remove.assert_called_once_with("filename.txt")
```

With `mocker.patch` you tell pytest that `os.remove` should be replaces with a `Mock` object that can be used by test for assertions. The `Mock` object has the `assert_called_once_with` method, which can be used to check if the function was called and with what. 

This is not necessarily useful in all cases but is supports a wide array of additional functionality. Here are some examples:

#### `return_value`

can be passed as a argument to the `patch` function to simulate the return value of the function:

```python
def test_fs_list(mocker):
    expectation=["file1.txt", "file2.txt"]
    query = "/path/to/folder/*.txt"
    mocker.patch('glob.glob', return_value=expectation)

    files = FS.getFiles(query)

    glob.glob.assert_called_once_with(query)

    assert expectation == files
```

#### `side_effect`

is a function that is called every time the patched function is called. Some examples:

- It can be used to raise exceptions
- If it is a iterable every time the function is called it will return the next value

Here we use the function from the last example but instead of mocking the return value we make the mocked function retrun a `KeyError` as the `glob.glob` would if passing a `int`:

```python
def test_fs_list_exception(mocker):
    mocker.patch('glob.glob', side_effect=TypeError)

    with pytest.raises(TypeError):
        FS.getFiles(1)
```

To some extent `side_effect` and `return_value` can be used to achive the same behavior. 

#### Opening files

A very common problem is to mock opening files. When the builtin `open` with `with` is used patching is not so easy. Let's assume we have a file we want to mock that contains

```
line1
line2
```

We add a method that open a file and return the lines as list:

```python
@staticmethod
def openFile(filename):
    with open(filename, "r") as f:
        return [l for l in f.read().split("\n") if l != ""]
```

The initial idea would be to just path the open and give it a return value:

```python
def test_fs_open(mocker):
    content = ["line1", "line2"]
    data = mocker.patch('builtins.open', return_value=content)
    
    assert data == content
```

Running the rest reveals that this is not working the way one would expect:

```
=========================== FAILURES ===========================
_________________________ test_fs_open _________________________

mocker = <pytest_mock.plugin.MockFixture object at 0x10c32b5f8>

    def test_fs_open(mocker):
        content = ["line1", "line2"]
        mocker.patch('builtins.open', return_value=content)

>       data = FS.openFile("/pyth/to/file.txt")

mocker_1.py:53:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

filename = '/pyth/to/file.txt'

    @staticmethod
    def openFile(filename):
>       with open(filename, "r") as f:
E       AttributeError: __enter__

mocker_1.py:16: AttributeError
================= 1 failed, 3 passed in 0.07s ==================
```

The problem here is that the `open` is used with the `with` statement. Since this is very common operation the mocking class provide a solution for this:

```python
def test_fs_open(mocker):
    content = ["line1", "line2"]
    mocker.patch('builtins.open', mocker.mock_open(read_data="line1\nline2\n"))

    data = FS.openFile("/pyth/to/file.txt")
    
    assert data == content
```

Passing `mocker.mock_open` simulates what one would get from the `with open...` statement. The string that is passed with `read_data`, should be what would be in the file.

-------

The full code for these examples can be found in the file [mocker_1.py](../examples/ch2/mocker_1.py).

-----

#### Mock all attribtues of a object you need for your code

You want to write a function that uses to objects and compares attributes of each of them. For the sake of this example, let's assume you have a function that checks the Licence plate of a car (`car.licencePlate`) agains all stolen cars in a plolice database (`policeDB.stolenCars`):

```python
def checkLicencePlate(car, policeDB):
    if car.licencePlate in policeDB.stolenCars:
        return True
    else:
        return False 
```

You don't want test the `car` nor the `policDB` but only your new function:

```python
def test_checkLicencePlatres_stolen(mocker):
    stolenCar = mocker.Mock()
    stolenCar.getLicencePlate.return_value = "ABC123"

    thisPoliceDB = mocker.Mock()
    thisPoliceDB.stolenCars = ["ABC123", "DEF456"]
    
    assert checkLicencePlate(stolenCar, thisPoliceDB)

def test_checkLicencePlatres_notStolen(mocker):
    notStolenCar = mocker.Mock()
    notStolenCar.getLicencePlate.return_value = "GHI789"

    thisPoliceDB = mocker.Mock()
    thisPoliceDB.stolenCars = ["ABC123", "DEF456"]
    
    assert not checkLicencePlate(notStolenCar, thisPoliceDB)
```

Generally, calling a Attirbute of a `Mock` object, it is automatically created and can be i.e. checked if it was called and with what. But we can also create attributes (like `thisPoliceDB.stolenCars`) or functions with return values (`stolenCar.getLicencePlate.return_value`).

-------

The full code for these examples can be found in the file [mocker_2.py](../examples/ch2/mocker_2.py).

-----



