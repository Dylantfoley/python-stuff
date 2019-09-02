#sets can only contain unique values
def firstDuplicate(a):
    aset = set()
    for i in a:
        if i in aset:
            return i # if item is in the list it will return the first duplicate
        else:
            aset.add(i) #adds each new item in the list to the set
    return -1