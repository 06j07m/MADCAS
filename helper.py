"""
Helper/util functions
"""

def getTitle(issueName: str) -> str:
    """
    Get series title.
    """
    return issueName[:issueName.rfind(" ")]


def formatSorted(sorted: list[str]) -> str:
    """
    Join list with newline
    """
    return "\n".join(sorted)
