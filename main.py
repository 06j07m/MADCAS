"""
Web app related sorting functions.
"""

def removeDuplicates(pasted: str) -> list[str]:
    """
    Remove duplicate lines (both) and any alphabet headers (DC wiki).
    """
    # get list of issue names (w. dup.s) (w. line breaks) and make into list
    pastedList = pasted.strip().split("\n")

    # remove returns/end of lines
    pastedList = [issue.strip("\r") for issue in pastedList]

    # enumerate returns (index, string); add to new list if string is not in old list up to index
    uniqueList = [issue for index, issue in enumerate(pastedList) 
                    if (issue not in pastedList[:index] and len(issue) > 1)]
    
    return uniqueList


def getTitle(issueName: str) -> str:
    """
    Get series title.
    """
    return issueName[:issueName.find("Vol")]


def getVolIss(issueName: str) -> str:
    """
    Get issue volume and issue number.
    """
    return issueName[issueName.find("Vol"):]


def sortMarvel(issueList: list[str]) -> list[str]:
    """
    Sort (Marvel wiki).
    """
    sorted = []

    # get series titles in order
    series = []
    for issue in issueList:
        title = getTitle(issue)
        if title not in series:
            series.append(title)

    # add all issues from each series to sorted list
    for title in series:
        sorted += [issue for issue in issueList if getTitle(issue) == title]

    return sorted


def formatSorted(sorted: list[str]) -> str:
    """
    Join list with newline
    """
    return "\n".join(sorted)