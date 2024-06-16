"""
Web app related sorting functions.
"""

import requests
from bs4 import BeautifulSoup
import datetime
from operator import itemgetter


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
    return issueName[:issueName.rfind(" ")]


def sortAccordingly(allIssues, seriesInOrder):
    """
    Sorts all issues into new list based on series order.
    """
    sorted = []

    # add all issues from each series to sorted list
    for title in seriesInOrder:
        sorted += [issue for issue in allIssues if getTitle(issue) == title]

    return sorted


def sortMarvel(issueList: list[str]) -> list[str]:
    """
    Sort (Marvel wiki).
    """
    # get series titles in order
    series = []
    for issue in issueList:
        title = getTitle(issue)
        if title not in series:
            series.append(title)

    return sortAccordingly(issueList, series)


def makeDcUrl(issueName: str) -> str:
    """
    Get URL of page from issue name (DC wiki).
    """
    words = issueName.split(" ")

    url = "https://dc.fandom.com/wiki/" + "_".join(words)
    return url


def findDatePublished(issueName: str) -> str:
    """
    Get issue published date (DC wiki).
    """
    # Make url
    testurl = makeDcUrl(issueName)

    # Try to get webpage information
    response = requests.get(testurl)
    htmlContent = response.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    textContent = soup.get_text()

    # Try to find find "published on"
    toFind = "was published on "
    pos = textContent.find(toFind)
    if pos == -1:
        return ""
    
    # If found, get index of date start and end
    startPos = pos + len(toFind)
    endPos = textContent.find(".", startPos)

    date = textContent[startPos:endPos]
    return date


def convertDate(date: str) -> datetime.date:
    """
    Make date comparable.
    """
    MONTH = 0
    DAY = 1
    YEAR = 2
    MONTHS = {"January": 1,
              "February": 2,
              "March": 3,
              "April": 4,
              "May": 5,
              "June": 6,
              "July": 7,
              "August": 8,
              "September": 9,
              "October": 10,
              "November": 11,
              "December": 12}
    
    # Get date components
    comps = [comp.strip(",") for comp in date.split(" ")]

    # Convert to numbers
    month = MONTHS[comps[MONTH]]
    day = int(comps[DAY])
    year = int(comps[YEAR])

    # Convert to date object
    comparableDate = datetime.date(year, month, day)

    return comparableDate


def sortDc(issueList: list[str]) -> list[str]:
    """
    Sort (DC wiki).
    """
    sorted = []

    # Get uniqe series and the "first" issues of that series
    series = []
    firstIssues = []
    for issue in issueList:
        title = getTitle(issue)
        if title not in series:
            series.append(title)
            firstIssues.append(issue)

    # Move into lists with and without date
    withDate = []
    noDate = []
    for i in range(len(firstIssues)):
        date = findDatePublished(firstIssues[i])
        if date == "":
            noDate.append(series[i])
        else:
            date2 = convertDate(date)
            withDate.append((date2, series[i]))

    # sort series with date
    withDate.sort(key=itemgetter(0))
    # remove dates
    withDate2 = [item[1] for item in withDate]

    withDateSorted = sortAccordingly(issueList, withDate2)
    noDateSorted = sortAccordingly(issueList, noDate)

    return noDateSorted + ["---"] + withDateSorted


def formatSorted(sorted: list[str]) -> str:
    """
    Join list with newline
    """
    return "\n".join(sorted)