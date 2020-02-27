import pytest

def checkLicensePlate(car, policeDB):
    if car.getLicensePlate() in policeDB.stolenCars:
        return True
    else:
        return False
    
def test_checkLicensePlatres_stolen(mocker):
    stolenCar = mocker.Mock()
    stolenCar.getLicensePlate.return_value = "ABC123"
    
    thisPoliceDB = mocker.Mock()
    thisPoliceDB.stolenCars = ["ABC123", "DEF456"]
    
    assert checkLicensePlate(stolenCar, thisPoliceDB)

def test_checkLicensePlatres_notStolen(mocker):
    notStolenCar = mocker.Mock()
    notStolenCar.getLicensePlate.return_value = "GHI789"

    thisPoliceDB = mocker.Mock()
    thisPoliceDB.stolenCars = ["ABC123", "DEF456"]
    
    assert not checkLicensePlate(notStolenCar, thisPoliceDB)
