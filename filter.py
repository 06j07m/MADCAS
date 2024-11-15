"""
Filter by consecutive issues
"""
import helper

def filter(sortedIssueList: list[str], numConsecutive: int) -> list[str]:
    final = []
    temp = []

    for i in sortedIssueList:
        if len(temp) == 0:
            # auto add first issue when restarting
            temp.append(i)
            continue

        # get title and number of current issue and issue to compare with
        curtitle, curnumber = helper.getTitle(i), helper.getIssueNum(i)
        title, number = helper.getTitle(temp[-1]), helper.getIssueNum(temp[-1])

        # determine whether to restart
        if curtitle != title:
            # diff series
            restart = True
        elif curnumber % 1 == 0 and curnumber != number + 1:
            # not next integer and not a float
            restart = True
        else:
            restart = False

        if restart:
            if len(temp) >= numConsecutive:
                final += temp
            temp.clear()
        temp.append(i)
               
    return final