# Advanced Topics

This chapter will cover advanced topics that will be very usefull when testing more complicated code. 

Also in this chapter the examples are using the `pytest` module.

## Mocking 

When testing your code/class/framework you proabably use external modules or file that you either don't want to test or can't test. Mocking is a way to simulates these dependecies (or what you expect as input for your functions) within a testing framework.

A extended introduction can be found [here on RealPython](https://realpython.com/python-mock-library/).

### Patching 

One common use case is to patch a function of an external dependency.     
Let's say, that your project includes a operation with the filesystem via `remove` from the `os` module. 

In principl you could write a test that creates a file in the test step, calls the function and finally checks if the function is still on the file system in the test assertion step.

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

With `mocker.patch` you tell pytest that `os.remove` should be replaced with a `Mock` object that can be used by during the test for assertions. The `Mock` object has the `assert_called_once_with` method which can be used to check if the function was called and with what. 

This method is not necessarily useful in all cases but the `Mock` object supports a wide array of additional functionality. Here are some examples:

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

To some extent `side_effect` and `return_value` can be used to achieve the same behavior. 

#### Opening files

A very common problem is to mock opening files. When the builtin `open` with `with` is used patching is not so easy. Let's assume we have a file we want to mock that contains

```
line1
line2
```

We add a method that opens a file and returns the lines as a `list`:

```python
@staticmethod
def openFile(filename):
    with open(filename, "r") as f:
        return [l for l in f.read().split("\n") if l != ""]
```

The initial idea would be to just patch the open and give it a return value:

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

Generally, when calling a Attirbute of a `Mock` object, it is automatically created. But we can also create attributes (like `thisPoliceDB.stolenCars`) or functions with return values (`stolenCar.getLicencePlate.return_value`).

### Note on mocking standard library modules

Let's say, you include `os.path` in your module and used `isfile` to check if a file is present. Let's call the module `MyAmazingModule`.

If you now mock the `isfile` with `mocker.patch.object(os.path, "isfile", True)` it works but this mocks `isfile` also in your test script and all other dependencies you include! In practice, this means that if you want to use `os.path.isfile` in your test it will also always return `True`.

Obviously there is a way to only mock it in the module `MyAmazingModule`. In principle `mocker.patch.object(MyAmazingModule.os.path, "isfile", , return_value=True)` should work but for some reason this is not always the case :man_shrugging:. It certainly works if you do `from os.path import isfile` in `MyAmazingModule` and then patch it with `mocker.patch.object(MyAmazingModule, "isfile", return_value=True)`.

## monkeypatching

If it not necessary to replace a whole object but only a single function/class/attribute, `monkeypatch` can be used. This does not give you any additioninal information like checking how many time the function was called.

Examples for situation where monkeypatching is useful:

An external dependency `module` uses a global variable `gVar` to save some state which is expected to be `expectedValue` for your test: 

```python
 monkeypatch.setattr(module, "gVar", expectedValue)
```

You are testing a method `method2` of your class `C` that requires the output `method1_value` of `method1`. Method `method1` is tested in a separate test  (`method1_value` can also be a function).

```python
monkeypatch.settatrr(C, "method1", method1_value)
```

See [this documentation](https://docs.pytest.org/en/latest/monkeypatch.html) for more information on monkeypatching in pytest.


-------

The full code for these examples can be found in the file [mocker_2.py](../examples/ch2/mocker_2.py).

-----



