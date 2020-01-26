import pytest

def checkLicencePlate(car, policeDB):
    if car.getLicencePlate() in policeDB.stolenCars:
        return True
    else:
        return False
    
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
