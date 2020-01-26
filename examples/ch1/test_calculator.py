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

@pytest.mark.parametrize("v1, v2", [(["2"], ["6"]), ("2","6"),(2, ["6"]), (2,"6")])
def test_calculator_add_execption(theCalculator, v1, v2):
    with pytest.raises(TypeError):
        theCalculator.add(v1, v2)

@pytest.mark.parametrize("v1, v2", [(["2"], ["6"]), ("2","6"),(2, ["6"]), (2,"6")])
def test_calculator_substract_execption(theCalculator, v1, v2):
    with pytest.raises(TypeError):
        theCalculator.substract(v1, v2)

@pytest.mark.parametrize("v1, v2", [(["2"], ["6"]), (2, ["6"]), (2,"6")])
def test_calculator_multiply_execption(theCalculator, v1, v2):
    with pytest.raises(TypeError):
        theCalculator.multiply(v1, v2)

