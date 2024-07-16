"""
Read and write files
"""

import helper


def openTxt(filepathNoExt: str) -> str:
    file = open(filepathNoExt + ".txt", 'r')
    fileAsStr = file.read()
    file.close()
        
    return fileAsStr


def saveTxt(dataAsStr: str, filepathNoExt: str) -> None:
    try:
        file = open(filepathNoExt + ".txt", 'w')
        file.write(dataAsStr)
        file.close()
    # print result if writing did not work
    except OSError:
        print(dataAsStr)


def saveTxt(dataAsList: list[str], filepathNoExt: str) -> None:
    try:
        file = open(filepathNoExt + ".txt", 'w')
        dataAsStr = helper.formatSorted(dataAsList)
        file.write(dataAsStr)
        file.close()
    # print result if writing did not work
    except OSError:
        print(dataAsStr)