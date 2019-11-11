from data_access_layer import DAL

# def myPrint(list_of_conferences):
#     print ("{:<4} {:<30} {:<18} {:<18} {:<12} {:<35} {:<12} {:<12}".format("ID", "Name", "City", "State", "Country", "Site", "Start", "End"))
#     for c in list_of_conferences:
#         print ("{:<4} {:<30} {:<18} {:<18} {:<12} {:<35} {:<12} {:<12}".format(c["ID"], c["Name"], c["City"], c["State"], c["Country"], c["Website"], c["Start Date"], c["End Date"]))


def printTable(list_of_dicts):
    """ Pretty print a list of dictionaries (list_of_dicts) as a dynamically sized table.
    sep: row separator. Ex: sep='\n' on Linux. Default: dummy to not split line.
    Author: Thierry Husson - Use it as you want but don't blame me.
    """
    sep = '\n'
    colList = ["ID", "Name", "City", "State", "Country", "Start Date", "End Date", "Website"]
    if not colList: colList = list(list_of_dicts[0].keys() if list_of_dicts else [])
    myList = [colList] # 1st row = header
    for item in list_of_dicts: myList.append([str(item[col] or '') for col in colList])
    colSize = [max(map(len,(sep.join(col)).split(sep))) for col in zip(*myList)]
    formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
    line = formatStr.replace(' | ','-+-').format(*['-' * i for i in colSize])
    print(line)
    item=myList.pop(0); lineDone=False
    while myList:
        if all(not i for i in item):
            item=myList.pop(0)
            if line and (sep!='\n' or not lineDone): print(line); lineDone=True
        row = [i.split(sep,1) for i in item]
        print(formatStr.format(*[i[0] for i in row]))
        item = [i[1] if len(i)>1 else '' for i in row]
    print(line)
