"""
Removes duplicates and groups issues by series for Marvel.
Not web app related.
Only runs in IDLE with the pasted thing as a multi line string???
"""

def sortMarvel(s: str):
    """
    list of issue names from fandom.com wiki
    """
    # get list of issue names (w. dup.s) (w. line breaks) and make into list
    names = s.split("\n")

    # remove duplicates:
    # enumerate returns (index, string); add to new list if string is not in old list up to index
    names_filtered = [x for i, x in enumerate(names) if x not in names[:i]]

    # function to get name of issue w.o. issue number
    def getTitle(name):
        return name[:name.find("Vol")]

    # resulting list
    names_sorted = []

    print("--> Processing...")
    
    # loop through names
    for name in names_filtered:
        # ignore if already added to resulting list
        if name in names_sorted:
            continue

        # otherwise -> add to resulting list and get title
        title = getTitle(name)
        names_sorted.append(name)
        # loop through rest of list
        for othername in names_filtered[names_filtered.index(name):]:
            # add other name with the same title to resulting list (if not already in it)
            if getTitle(othername)==title and othername not in names_sorted:
                names_sorted.append(othername)


    # make sure sorted list has same num. of items as list w.o. dup.s
    # NOT AN ACCURATE CHECK OF ACTUAL CONTENTS!
    if len(names_sorted)==len(names_filtered):
        print("--> Sorted list size = Duplicates-removed list size: =", len(names_sorted))
    else:
        print("--> Missing list items")


    # ask for file name
    filename = input("--> File name (without extension): ")

    # no file name -> print sorted result
    if filename == "":
        for name in names_sorted:
            print(name)
        print("--> Done")
        return

    # filename given -> open file and write items in list
    try:
        # file aready exists -> add to end
        with open(filename+".txt", "a") as file:
            print("--> File exists, adding to file...")
            for name in names_sorted:
                file.write(name+"\n")
    # file doesn't exist -> make new file
    except FileNotFoundError:
        try:
            with open(filename+".txt","w") as file:
                for name in names_sorted:
                    file.write(name+"\n")
        # file writing didn't work -> print result
        except IOError:
            print("--> File error(")
            for name in names_sorted:
                print(name)
            pass
    print("--> Done")
