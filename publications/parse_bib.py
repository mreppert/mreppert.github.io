import sys
import numpy as np
import re

infile = sys.argv[1]

def extract_entry(key, rec):
    x = re.search(key + "[ ]*=[ ]*", rec)
    if x == None:
        return ""
    else:
        n1 = x.span()[1] 

        delim = rec[n1]
        if delim=="{":
            clim = "}"
        elif delim=="\"":
            clim = delim

        # If we don't recognize the delimiter, assume that there isn't one.
        # In this case, the entry terminates with either a comma or the end of 
        # the Record, as indicated by a "}".
        else:
            if rec[n1+1:].count(",")>0:
                n2 = n1 + 1 + rec[n1+1:].find(",")
                return rec[n1:n2]
            elif rec[n1+1:].count("}")>0:
                n2 = rec[n1+1:].find("}")
                return rec[n1:n2]
            else: 
                print("Error identifying entry " + key + " for the following record:\n\n" + rec + "\n")
                return ""


    # If we reach this part of the code, there is a delimiter and it should be identified

    search_lim = n1+1
    found_end = False
    while found_end == False:
        # Find the next occurrence of clim after search_lim
        n2 = search_lim + rec[search_lim:].find(clim)

        # n2 is a candidate end limit, but let's check if it might be 
        # a false alarm. 
        # First possibility is that clim is "}" and the located brace
        # just closes a secondary left-brace (e.g., for a special char). 
        if (clim=="}" and rec[search_lim:n2].find("{")>=0) or (clim=="\"" and rec[n2-1]=="\\"):

            # If this happens, we just update the search_lim and go again
            search_lim = n2+1

        else:
            found_end = True

    if n2<n1+1:
        print('Could not find close record!')
        return ""
    else:
        return rec[n1+1:n2]



RefList = []
YearList = []

Record = ""
bcount = 0
with open(infile, "r") as fd:
    for line in fd:
        if "@article" in line.lower() or "@incollection" in line.lower():
            Record = line[:-1]
            bcount = Record.count("{") - Record.count("}")

        elif bcount>0 and len(line)>0:
            Record += line
            bcount = Record.count("{") - Record.count("}")

        if len(Record)>0 and bcount==0:

            Record = Record.replace("\n", " ")
            authors = extract_entry("author", Record)
            title = extract_entry("title", Record)
            ppg = extract_entry("pages", Record)
            year = extract_entry("year", Record)

            authlist = ""
            for auth in authors.split(' and '):
                auth = auth.replace("{\\\"a}", "a")
                auth = auth.replace("{\\\"o}", "o")
                auth = auth.replace("{\\\"u}", "u")
                fname = auth.split(",")[1].strip()
                lname = auth.split(",")[0].strip()
                authlist += lname + ', ' + fname + '; '

            authlist = authlist[:-2]

            if "@article" in Record.lower():
                journal = extract_entry("journal", Record)
                vol = extract_entry("volume", Record)
                doi = extract_entry("doi", Record)

                if len(vol)>0:
                    vol += ", "

                if len(doi)>0:
                     title = "<a href=\"https://doi.org/" + doi + "\">\"" + title + "\"</a>. "
                entry = "<li>" + authlist + "; " + title + "<i>" + journal + "</i>, " + vol + ppg + " (" + year + ").</li>"

            if "@incollection" in Record.lower():
                btitle = extract_entry("booktitle", Record)
                editor = extract_entry("editor", Record)
                publisher = extract_entry("publisher", Record)
                chapter = extract_entry("chapter", Record)
                address = extract_entry("address", Record)

                entry = "<li>" + authlist + "\"" + title + "In <i>" + btitle + "</i>, " + editor + ", editor, Chapter " + chapter + ", " + ppg + ". " + publisher + ", " + address + "(" + year + ").</li>"

            entry = entry.replace("~", " ")

            RefList.append(entry)
            YearList.append(int(year))
            Record = ""

Years = np.array(YearList)
ndcs = np.argsort(-1*Years)



lastyear = Years[ndcs[0]]
print("<h2>" + str(lastyear) + "</h2>")
print()

for n in range(0, len(Years)):

    print(RefList[ndcs[n]], "\n\n")
    if Years[ndcs[n]] != lastyear:
        lastyear = Years[ndcs[n]]
        print()
        print("<h2>" + str(lastyear) + "</h2>")
        print()
