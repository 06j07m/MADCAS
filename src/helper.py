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


def formatSorted(sorted: list[str]) -> str:
    """
    Join list with newline
    """
    return "\n".join(sorted)
