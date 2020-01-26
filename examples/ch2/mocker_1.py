import os
import glob
import pytest

class FS:
    @staticmethod
    def removeFile(filename):
        os.remove(filename)

    @staticmethod
    def getFiles(query):
        return glob.glob(query)

    @staticmethod
    def openFile(filename):
        with open(filename, "r") as f:
            return [l for l in f.read().split("\n") if l != ""]
    
def test_fs_remove(mocker):
    mocker.patch('os.remove')
    FS.removeFile("filename.txt")
    os.remove.assert_called_once_with("filename.txt")
    
def test_fs_list(mocker):
    expectation=["file1.txt", "file2.txt"]
    query = "/path/to/folder/*.txt"
    mocker.patch('glob.glob', return_value=expectation)

    files = FS.getFiles(query)

    glob.glob.assert_called_once_with(query)

    assert expectation == files

def test_fs_list_exception(mocker):
    mocker.patch('glob.glob', side_effect=TypeError)

    with pytest.raises(TypeError):
        FS.getFiles(1)


#NOTE: This one does not work
# def test_fs_open(mocker):
#     content = ["line1", "line2"]
#     mocker.patch('builtins.open', return_value=content)

#     data = FS.openFile("/pyth/to/file.txt")
    
#     assert data == content


def test_fs_open(mocker):
    content = ["line1", "line2"]
    mocker.patch('builtins.open', mocker.mock_open(read_data="line1\nline2\n"))

    data = FS.openFile("/pyth/to/file.txt")
    
    assert data == content
