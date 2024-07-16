"""
Web app related sorting functions
"""

import requests
from bs4 import BeautifulSoup
import datetime
from operator import itemgetter
import helper


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


def sortAccordingly(allIssues, seriesInOrder):
    """
    Sorts all issues into new list based on series order.
    """
    sorted = []

    # add all issues from each series to sorted list
    for title in seriesInOrder:
        sorted += [issue for issue in allIssues if helper.getTitle(issue) == title]

    return sorted


def sortMarvel(issueList: list[str]) -> list[str]:
    """
    Sort (Marvel wiki).
    """
    # get series titles in order
    series = []
    for issue in issueList:
        title = helper.getTitle(issue)
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
    Get issue published date (DC wiki) as comparable object.
    """
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
    
    # Make url
    testurl = makeDcUrl(issueName)

    # Try to get webpage information
    response = requests.get(testurl)
    htmlContent = response.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    textContent = soup.get_text()

    # Try to find "published on"
    toFind = "was published on "
    pos = textContent.find(toFind)
    startPos = pos + len(toFind)

    if pos == -1:
        # Try to find "with a cover date of"
        toFind = "cover date of "
        pos = textContent.find(toFind)
        startPos = pos + len(toFind) + 1
        
        if pos == -1:
            return None

    # If found, get index of date start and end
    endPos = textContent.find(".", startPos)

    # Get date 
    date = textContent[startPos:endPos]

    # Get date components
    comps = [comp.strip(",") for comp in date.split(" ")]
    
    try:
        # Convert to numbers
        month = MONTHS[comps[0]]
        year = int(comps[-1])
    
        # MMMM DD, YYYY
        if len(comps) == 3:
            day = int(comps[1])

        # MMMM, YY
        elif len(comps) == 2:
            day = 1

        # Convert to date object (1st of the month)
        comparableDate = datetime.date(year, month, 1)
        return comparableDate
    # If date doesn't convert, pretend it doesn't exist
    except:
        return None


def sortDc(issueList: list[str]) -> list[str]:
    """
    Sort (DC wiki).
    """
    sorted = []

    # Get uniqe series and the "first" issues of that series
    series = []
    firstIssues = []
    for issue in issueList:
        title = helper.getTitle(issue)
        if title not in series:
            series.append(title)
            firstIssues.append(issue)

    # Move into lists with and without date
    withDate = []
    noDate = []
    for i in range(len(firstIssues)):
        date = findDatePublished(firstIssues[i])
        if date == None:
            noDate.append(series[i])
        else:
            withDate.append((date, series[i]))

    # sort series with date
    withDate.sort(key=itemgetter(0))
    # remove dates
    withDate2 = [item[1] for item in withDate]

    withDateSorted = sortAccordingly(issueList, withDate2)
    noDateSorted = sortAccordingly(issueList, noDate)

    if len(noDateSorted) != 0:
        return noDateSorted + ["---"] + withDateSorted

    return withDateSorted