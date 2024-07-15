import main

def openTxt(filepathNoExt: str) -> str:
    file = open(filepathNoExt + ".txt", 'r')
    fileAsStr = file.read()
    file.close()
        
    return fileAsStr


def openAndRemDup(filepathNoExt: str) -> list[str]:
    file = open(filepathNoExt + ".txt", 'r')
    fileAsStr = file.read()
    file.close()
        
    return main.removeDuplicates(fileAsStr)


def saveTxt(dataAsStr: str, filepathNoExt: str) -> None:
    try:
        file = open(filepathNoExt + ".txt", 'w')
        file.write(dataAsStr)
        file.close()
    # print result if writing did not work
    except OSError:
        print(dataAsStr)
