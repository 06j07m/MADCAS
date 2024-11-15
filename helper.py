"""
Helper/util functions
"""

def getTitle(issueName: str) -> str:
    """
    Get series title.
    """
    return issueName[:issueName.rfind(" ")]


def getIssueNum(issueName: str) -> float:
    start = issueName.rfind(" ") + 1

    # if not a number
    last = issueName[start:]
    if not last.isnumeric():
        return 0.0
    
    return float(last)


def removeDuplicates(pastedList: list[str]) -> list[str]:
    """
    Remove duplicate lines (both) and any alphabet headers (DC wiki)
    """
    # enumerate returns (index, string); add to new list if string is not in old list up to index
    uniqueList = [issue for index, issue in enumerate(pastedList) 
                    if (issue not in pastedList[:index] and len(issue) > 1)]
    
    return uniqueList


def formatSorted(sorted: list[str]) -> str:
    """
    Join list with newline
    """
    return "\n".join(sorted)


def getLines(pasted: str) -> list[str]:
    """
    Get list of issue names (w. dup.s) (w. line breaks) and make into list
    (remove returns/end of lines)
    """
    lines = [i.strip() for i in pasted.strip().split("\n")]
    return lines