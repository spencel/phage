import io
import os

# Parse summaryInfo.txt #
f = open("dat/summaryInfo.txt",'r', encoding="utf-8")
lisData = []
i = 0
for l in f: #Loop through lines in the file
    lisData.append(l.split('|', -1))
    uBound = len(lisData[i])
    for j in range(0, uBound): #Strip characters from list items
        lisData[i][j] = lisData[i][j].strip(" \t\n")
    lisData[i][0] = lisData[i][0].replace('\t',' ').replace('_',' ')
    #print(lisData[i][0])
    #print(lisData[i])
    i+= 1
f.close()
del i

diJobId = {}
uBound = len(lisData)
for i in range(1 , uBound): #skips first row, which is column names
    diJobId[lisData[i][1]] = i - 1 #accounts for column names and output data won't have them
del uBound

# Parse extendedSummaryInfo.txt #
f = open("dat/extendedSummaryInfo.txt",'r', encoding="utf-8")
liExtSumInf = []
i = 0
for l in f: #Loop through lines in the file
    liExtSumInf.append(l.split('|', -1))
    uBound = len(liExtSumInf[i])
    for j in range(0, uBound): #Strip characters from list items
        liExtSumInf[i][j] = liExtSumInf[i][j].strip(" \t\n")
    i+= 1
f.close()
del i
i = 0
for x in liExtSumInf: #Gets rid of column names and rows that are just repeats of column names
    if x[0] == "# Job Description":
        liExtSumInf.pop(i)
    i += 1
del i
for x in liExtSumInf: #Gets rid of phage names because they're already in another array
    x[1] = diJobId[x[1]]
    x.pop(0)
for i in range(0, len(liExtSumInf)):
    for j in range(0, len(liExtSumInf[i])):
        try:
            liExtSumInf[i][j] = int(liExtSumInf[i][j])
        except:
            try:
                liExtSumInf[i][j] = float(liExtSumInf[i][j])
            except:
                pass                
    
# Generate extSumInf.js #
f =open("dat/extSumInf.js",'w', encoding="utf-8")
f.write("var extSumInf = [\n")
for i in liExtSumInf:
    f.write(str(i) + ",\n")
f.write("]")
f.close()


# Generate strArPhageDirPaths.js #
strArPath = [""] * (len(lisData) - 1)
def getPaths(strCurPath):
    print("1: " + strCurPath)
    isPhageFolder = os.path.exists(strCurPath + "/summary.html")
    if isPhageFolder:
        aPath = strCurPath.split("/")
        index = diJobId[aPath[len(aPath)-1]]
        strArPath[index] = strCurPath
    else:
        strLiDir = os.listdir(strCurPath)
        for strDir in strLiDir:            
            if os.path.isdir(strCurPath + "/" + strDir):
                getPaths(strCurPath + "/" + strDir)
getPaths("K:/PHYRE2/Results/ec54f8c2dc927ec8") #starts a recursive function
strData = "var strArPhageDirPaths=[\"" + strArPath[0] + "\""
uBound = len(strArPath)
for i in range(1, uBound):
    strData = strData + ",\"" + strArPath[i] + "\""
del uBound
strData = strData + "];"
f =open("dat/strArPhageDirPaths.js",'w', encoding="utf-8")
f.write(strData)
f.close()
del strData

# Generate arPhages.js #
phages = []
uBound = len(lisData)
for i in range(1, uBound):
    phages.append([lisData[i][0]])
    phages[i-1].append(lisData[i][1])
    phages[i-1].append([])
#print(phages)
uBound = len(liExtSumInf)
for i in range(0, uBound):
    if liExtSumInf[i][0] != "# Job Description":
        phages[liExtSumInf[i][0]][2].append(i)
strData = "// Description, Job ID, Index relation to extSumInf\n"
strData = strData + "var arPhages=" + str(phages) + ";"
f = open("dat/arPhages.js",'w', encoding="utf-8")
f.write(strData)
f.close()
del strData

# Generate index.html #
strHtml = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"/><title>Phage Project GUI</title>"
# Generate script tags
# Generate database script tags
strLiFilesAndFolders = os.listdir("dat/")
for strFileOrFolder in strLiFilesAndFolders:
    if strFileOrFolder.endswith(".js"):
        strHtml = strHtml + "<script type=\"text/javascript\" src=\"dat/" + strFileOrFolder + "\"></script>"
strHtml = strHtml + "<script type=\"text/javascript\" src=\"lib/jquery-3.0.0.min.js\"></script>"
strHtml = strHtml + "<script type=\"text/javascript\" src=\"main.js\"></script>"
strHtml = strHtml + "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/style.css\">"
strHtml = strHtml + "</script><style></style></head><body>"
strHtml = strHtml + "<input id=\"searchA\" autocomplete=\"on\" placeholder=\"Search...\" type=\"search\"></input>"
strHtml = strHtml + "</body></html>"
#print(strHtml)
f = open("index.html",'w', encoding="utf-8")
f.write(strHtml)
f.close()
