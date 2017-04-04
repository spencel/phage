import io
import os
import json

datDirectory = "../../dat/"
pathToPhyre2Results = datDirectory + "phyre2"
summaryInfoFileName = datDirectory + "phyre2/2016.08.03/summaryInfo.txt"
summaryInfoExtendedFileName = datDirectory + "phyre2/2016.08.03/summaryInfoExtended.txt"
gbkDirectory = datDirectory + "json/"

# Parse summaryInfo.txt #
f = open(summaryInfoFileName,'r', encoding="utf-8")
lisData = []
i = 0
for l in f: #Loop through lines in the file
    lisData.append(l.split('|', -1))
    uBound = len(lisData[i])
    for j in range(0, uBound): #Strip characters from list items
        lisData[i][j] = lisData[i][j].strip(" \t\n")
    lisData[i][0] = lisData[i][0].replace('\t',' ').replace('_',' ') # Replace tabs and then underscores with space for genome id
    lisData[i][1] = lisData[i][1].replace('\t',' ').replace('_',' ') # Replace tabs and then underscores with space for bp range
    lisData[i][2] = lisData[i][2].replace('\t',' ').replace('_',' ') # Replace tabs and then underscores with space for species name

    i += 1    

f.close()
del i
#print(lisData)

diJobId = {}
uBound = len(lisData)
for i in range(1 , uBound): #skips first row, which is column names
    diJobId[lisData[i][3]] = i - 1 #accounts for column names and output data won't have them
del uBound

# Parse extendedSummaryInfo.txt #
f = open(summaryInfoExtendedFileName,'r', encoding="utf-8")
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
    x[1] = diJobId[x[3]]
    x.pop(0) # gets rid of genome id
    x.pop(1) # gets rid of virus name
    x.pop(1) # gets rid of job id
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
f =open( datDirectory + "extSumInf.js",'w', encoding="utf-8")
f.write("var extSumInf = [\n")
for i in liExtSumInf:
    f.write(str(i) + ",\n")
f.write("]")
f.close()


# Generate strArPhageDirPaths.js #
strArPath = [""] * (len(lisData) - 1)
def getPaths( strCurPath ):
    print("1: " + strCurPath)
    isPhageFolder = os.path.exists(strCurPath + "/summary.html")
    if isPhageFolder:
        aPath = strCurPath.split("/")
        #print(diJobId)
        index = diJobId[aPath[len(aPath)-1]]
        strArPath[index] = strCurPath[ 6 : ]
    else:
        strLiDir = os.listdir(strCurPath)
        for strDir in strLiDir:            
            if os.path.isdir(strCurPath + "/" + strDir):
                getPaths(strCurPath + "/" + strDir)
getPaths( pathToPhyre2Results ) #starts a recursive function
strData = "var strArPhageDirPaths=[\"" + strArPath[0] + "\""
uBound = len(strArPath)
for i in range(1, uBound):
    strData = strData + ",\"" + strArPath[ i ] + "\""
del uBound
strData = strData + "];"
f =open( datDirectory + "strArPhageDirPaths.js",'w', encoding="utf-8")
f.write(strData)
f.close()
del strData


# Generate arPhages.js #
#print(lisData)
phages = []
uBound = len(lisData)
for i in range(1, uBound):
    phages.append([lisData[i][0]])
    phages[i-1].append(lisData[i][1])
    phages[i-1].append(lisData[i][2])
    phages[i-1].append([])
    phages[i-1].append("")
    phages[i-1].append("")
    phages[i-1].append("")
    # Get the protein id based on the species id and base pair range of the protein
    ## Skip the column titles row
    with open( gbkDirectory + lisData[ i ][ 0 ] + ".gbk.json", 'r', encoding="utf-8" ) as f:
        #print( f.read() )
        jsonString = f.read()
        #print( jsonString )
        jsonData = json.loads( jsonString, encoding="utf-8" ) 
        #print( jsonData )
        #print( lisData[ i ][ 1 ][ 3: ] )
        bpRange = lisData[ i ][ 1 ][ 3: ]

        for CDS in jsonData[ "CDS" ]:

            
            if bpRange in CDS[ "CDS" ]:
                #print( bpRange + " " + CDS[ "CDS" ] )
                #print( CDS[ "Dbxref" ] )
                #print( phages[i-1].append() )
                found = False

                for dbxref in CDS[ "Dbxref" ]:

                    if "NCBI_genpept:" in dbxref:
                        #print( dbxref[ len( "NCBI_genpept:protein_id|" ) : ] )
                        phages[ i-1 ][ 4 ] = dbxref 
                        found = True

                    if "NCBI_gi:" in dbxref:
                        #print( dbxref[ len( "NCBI_genpept:protein_id|" ) : ] )
                        phages[ i-1 ][ 5 ] = dbxref 
                        found = True

                    if "FIG_ID:" in dbxref:
                        #print( dbxref[ len( "NCBI_genpept:protein_id|" ) : ] )
                        phages[ i-1 ][ 6 ] = dbxref 
                        found = True

                if found == False:

                    print( "WARNING: Protein ID not found: " + lisData[i][0] + "; " + lisData[i][1] + "; " + lisData[i][2] )

#print(phages)
uBound = len(liExtSumInf)
for i in range(0, uBound):
    if liExtSumInf[i][0] != "# Job Description":
        phages[liExtSumInf[i][0]][3].append(i)
strData = "// Description, Job ID, Index relation to extSumInf\n"
strData = strData + "var arPhages=" + str(phages) + ";"
f = open( datDirectory + "arPhages.js",'w', encoding="utf-8" )
f.write(strData)
f.close()
del strData


# Generate index.html #
strHtml = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"/><title>Phage Project GUI</title>"
# Generate script tags
# Generate database script tags
strLiFilesAndFolders = os.listdir( datDirectory )
for strFileOrFolder in strLiFilesAndFolders:
    if strFileOrFolder.endswith(".js"):
        strHtml = strHtml + "<script type=\"text/javascript\" src=\"dat/" + strFileOrFolder + "\"></script>"
strHtml = strHtml + "<script type=\"text/javascript\" src=\"lib/jquery-3.0.0.min.js\"></script>"
strHtml = strHtml + "<script type=\"text/javascript\" src=\"main.js\"></script>"
strHtml = strHtml + "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/style.css\">"
strHtml = strHtml + "</script><style></style></head><body onload='main();'>"
strHtml = strHtml + "<input id=\"searchA\" autocomplete=\"on\" placeholder=\"Search...\" type=\"search\"></input>"
strHtml = strHtml + "</body></html>"
#print(strHtml)
f = open("../../index.html",'w', encoding="utf-8")
f.write(strHtml)
f.close()
