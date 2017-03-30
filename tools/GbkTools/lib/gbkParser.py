import io
import os
import sys
import json

class gbkReport:
	meta = {}
	alias = []
	regAlias = {}
	def getAllAlias(path):
		fileNames = os.listdir(path)
		i = 0
		while i < len(fileNames):
			if fileNames[i].endswith("gbk") == False:
				fileNames.pop(i)
			else:
				i += 1
		for iFileName, fileName in enumerate(fileNames):
			d = {}
			with open("%s/%s" % (path, fileName), 'r', encoding="utf-8") as f:
				line = f.readline()
				iLine = 1
				while line != "": # loop until EOF is reached
					# CDS #
					if line[:21] == "     CDS             ":
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							line = f.readline()
							iLine += 1
						while line != "" and line[:21] == "                     ":
							# Alias #
							if line[21:28].lower() == "/alias=":
								value = line[28:].strip("\n")
								line = f.readline()
								iLine += 1
								while line != "" and line[:21] == "                     " and line[21:22] != "/":
									value = "%s%s"%(value, line[21:].strip("\n"))
									line = f.readline()
									iLine += 1
								gbkReport.alias.append(value.strip("\""))
							else:
								line = f.readline()
								iLine += 1
					else:
						line = f.readline()
						iLine += 1
					print(iLine)
			if iFileName % len(fileNames) == 0:
				print(iFileName/len(fileNames)*100)
		with open("%s/%s" % ("K:/PHANTOME/Viruses-caudo_with_major-capsid", "reportAlias.txt"), 'w', encoding="utf-8") as f:
			for i in gbkReport.alias:
				f.write(i+"\n")
		for i in gbkReport.alias:
			strFrag = ""
			for c in i:
				strFrag = "%s%s" % (strFrag, c)
				if strFrag in  gbkReport.regAlias:
					gbkReport.regAlias[strFrag] += 1
				else:
					gbkReport.regAlias[strFrag] = 1
		with open("%s/%s" % ("K:/PHANTOME/Viruses-caudo_with_major-capsid", "reportRegAlias.txt"), 'w', encoding="utf-8") as f:
			for k in gbkReport.regAlias:
				f.write(k + ";" + str(gbkReport.regAlias[k]) + "\n")


def pyToJsonFile(d, rootIdentifier, path, fileName):
	strD = "var " + rootIdentifier + " = {\n" # initialize dictionary
	def toJson(d, level, strD):
		if isinstance(d, dict):
			for iK, k in enumerate(d):
				for i in range(0, level):
					strD = "%s\t" % (strD)
				strD = "%s\"%s\": " % (strD, k)
				if isinstance(d[k], dict):
					strD = "%s{\n" % (strD)
					nextLevel = level + 1
					strD = toJson(d[k], nextLevel, strD)
					for i in range(0, level):
						strD = "%s\t" % (strD)
					if iK < len(d)-1:
						strD = "%s},\n" % (strD)
					else:
						strD = "%s}\n" % (strD)
				elif isinstance(d[k], list):
					strD = "%s[\n" % (strD)
					nextLevel = level + 1
					strD = toJson(d[k], nextLevel, strD)
					for i in range(0, level):
						strD = "%s\t" % (strD)
					if iK < len(d)-1:
						strD = "%s],\n" % (strD)
					else:
						strD = "%s]\n" % (strD)
				else:
					if iK < len(d)-1:
						strD = "%s%s,\n" % (strD, d[k])
					else:
						strD = "%s%s\n" % (strD, d[k])
		else:
			for k in range(0, len(d)):
				for i in range(0, level):
					strD = "%s\t" % (strD)
				if isinstance(d[k], dict):
					strD = "%s{\n" % (strD)
					nextLevel = level + 1
					strD = toJson(d[k], nextLevel, strD)
					for i in range(0, level):
						strD = "%s\t" % (strD)
					if k < len(d)-1:
						strD = "%s},\n" % (strD)
					else:
						strD = "%s}\n" % (strD)
				elif isinstance(d[k], list):
					strD = "%s[\n" % (strD)
					nextLevel = level + 1
					strD = toJson(d[k], nextLevel, strD)
					for i in range(0, level):
						strD = "%s\t" % (strD)
					if k < len(d)-1:
						strD = "%s],\n" % (strD)
					else:
						strD = "%s]\n" % (strD)
				else:
					if k < len(d)-1:
						strD = "%s%s,\n" % (strD, d[k])
					else:
						strD = "%s%s\n" % (strD, d[k])
		return strD
	strD = strD + toJson(d, 1, "")
	strD = strD + "}" # close out dictionary
	with open("%s/%s" % (path, fileName), 'w', encoding="utf-8") as f:
		f.write(strD)


def gbkToPy(path, fileName, debugOn):
	d = {
		"LOCUS":"",
		"DEFINITION":"",
		"ACCESSION":"",
		"SOURCE":"",
		"ORGANISM":"",
		"FEATURES":"",
		"source": {},
		"RNA":[],
		"ORIGIN":""
	}
	with open("%s/%s" % (path, fileName), 'r', encoding="utf-8") as f:
		line = f.readline()
		iLine = 1
		while line != "": # loop until EOF is reached
			# LOCUS #
			if line[:12] == "LOCUS       ":
				value = line[13:].strip("\n")
				line = f.readline()
				iLine += 1
				while line != "" and line[:12] == "            ":
					value = "%s %s"%(value, line[12:].strip("\n"))
					line = f.readline()
					iLine += 1
				d["LOCUS"] = "%s" % (value)
			# DEFINITION #
			elif line[:12] == "DEFINITION  ":
				d["DEFINITION"] = line[12:].strip("\n")
				line = f.readline()
				iLine += 1
				while line != "" and line[:12] == "            ":
					d["DEFINITION"] = "%s %s"%(d["DEFINITION"], line[12:].strip("\n"))
					line = f.readline()
					iLine += 1
				d["DEFINITION"] = "%s" % (d["DEFINITION"])
			# ACCESSION #
			elif line[:12] == "ACCESSION   ":
				d["ACCESSION"] = line[12:].strip("\n")
				line = f.readline()
				iLine += 1
				while line != "" and line[:12] == "            ":
					d["ACCESSION"] = "%s %s"%(d["ACCESSION"], line[12:].strip("\n"))
					line = f.readline()
					iLine += 1
				d["ACCESSION"] = "%s" % (d["ACCESSION"])
			# SOURCE #
			elif line[:12] == "SOURCE      ":
				d["SOURCE"] = line[12:].strip("\n")
				line = f.readline()
				iLine += 1
				while line != "" and line[:12] == "            ":
					d["SOURCE"] = "%s %s"%(d["SOURCE"], line[12:].strip("\n"))
					line = f.readline()
					iLine += 1
				d["SOURCE"] = "%s" % (d["SOURCE"])
			# ORGANISM #
			elif line[:12] == "  ORGANISM  ":
				d["ORGANISM"] = line[12:].strip("\n")
				line = f.readline()
				iLine += 1
				while line != "" and line[:12] == "            ":
					d["ORGANISM"] = "%s %s"%(d["ORGANISM"], line[12:].strip("\n"))
					line = f.readline()
					iLine += 1
				d["ORGANISM"] = "%s" % (d["ORGANISM"])
			# FEATURES #
			elif line[:21] == "FEATURES             ":
				d["FEATURES"] = line[21:].strip("\n")
				line = f.readline()
				iLine += 1
				while line != "" and line[:21] == "                     ":
					d["FEATURES"] = "%s %s"%(d["FEATURES"], line[21:].strip("\n"))
					line = f.readline()
					iLine += 1
				d["FEATURES"] = "%s" % (d["FEATURES"])
			# Source #
			elif line[:21] == "     source          ":
				d["source"]["source"] = (line[21:].strip("\n"))
				line = f.readline()
				iLine += 1
				while line != "" and line[:21] == "                     " and line[21:22] != "/":
					d["source"]["source"] = "%s %s"%(d["source"]["source"], line[21:].strip("\n"))
					line = f.readline()
					iLine += 1
				d["source"]["source"] = "%s" % (d["source"]["source"])
				while line != "" and line[:21] == "                     ":
                     #/mol_type="genomic DNA"
					if line[21:31] == "/mol_type=":
						d["source"]["mol_type"] = line[31:].strip("\n").strip("\"")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							d["source"]["mol_type"] = "%s %s"%(d["source"]["mol_type"], line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
                     #/genome_md5="a07cc063bbe344fc9c87a19456ef8354"
					elif line[21:33] == "/genome_md5=":
						d["source"]["genome_md5"] = line[33:].strip("\n").strip("\"")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							d["source"]["genome_md5"] = "%s%s"%(d["source"]["genome_md5"], line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
                     #/project="redwards_1247"
					elif line[21:30] == "/project=":
						d["source"]["project"] = line[30:].strip("\n").strip("\"")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							d["source"]["project"] = "%s %s"%(d["source"]["project"], line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
                     #/genome_id="1247.119"
					elif line[21:32] == "/genome_id=":
						d["source"]["genome_id"] = line[32:].strip("\n").strip("\"")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							d["source"]["genome_id"] = "%s %s"%(d["source"]["genome_id"], line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
                     #/organism="Oenococcus phage phi9805, complete genome."
					elif line[21:31] == "/organism=":
						d["source"]["organism"] = line[31:].strip("\n").strip("\"")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							d["source"]["organism"] = "%s %s"%(d["source"]["organism"], line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
                     #/dbxref="taxon: 1247"
					elif line[21:36] == "/dbxref=\"taxon:":
						d["source"]["dbxref-taxon"] = line[36:].strip("\n").strip("\"")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							d["source"]["dbxref-taxon"] = "%s %s"%(d["source"]["dbxref-taxon"], line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
						d["source"]["dbxref-taxon"] = "%s" % (d["source"]["dbxref-taxon"].strip(" "))
					#Error Handling for Child Tokens
					elif debugOn == True:
						print(fileName + " Line " + str(iLine) + " Error: " + line.strip("\n"))
						line = f.readline()
						iLine += 1
			# CDS #
			elif line[:21] == "     CDS             ":
				if "CDS" not in d:
					d["CDS"] = []
				iCds = len(d["CDS"])
				d["CDS"].append({})
				value = line[21:].strip("\n")
				line = f.readline()
				iLine += 1
				while line != "" and line[:21] == "                     " and line[21:22] != "/":
					value = "%s %s"%(value, line[21:].strip("\n"))
					line = f.readline()
					iLine += 1
				d["CDS"][iCds]["CDS"] = "%s" % value
				while line != "" and line[:21] == "                     ":
					# Locus #
					if line[21:28] == "/locus=":
						value = line[28:].strip("\n").strip("\"")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							value = "%s%s"%(value, line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
						d["CDS"][iCds]["locus"] = "%s" % (value.strip(" "))
                    # Alias #
					elif line[21:28] == "/Alias=":
						k = "Alias"
						value = line[28:].strip("\n")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							value = "%s%s"%(value, line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
						if k not in d["CDS"][iCds]:
							d["CDS"][iCds][k] = [value.strip(" ").strip("\"")]
						else:
							d["CDS"][iCds][k].append(value.strip(" ").strip("\""))
					# gene_symbol #
					elif line[21:34] == "/gene_symbol=":
						k = "gene_symbol"
						value = line[34:].strip("\n")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							value = "%s%s"%(value, line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
						if k not in d["CDS"][iCds]:
							d["CDS"][iCds][k] = [value.strip(" ").strip("\"")]
						else:
							d["CDS"][iCds][k].append(value.strip(" ").strip("\""))
					# locus_tag #
					elif line[21:32] == "/locus_tag=":
						k = "locus_tag"
						value = line[32:].strip("\n")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							value = "%s%s"%(value, line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
						if k not in d["CDS"][iCds]:
							d["CDS"][iCds][k] = [value.strip(" ").strip("\"")]
						else:
							d["CDS"][iCds][k].append(value.strip(" ").strip("\""))
					# Color #
					elif line[21:28] == "/color=":
						d["CDS"][iCds]["color"] = line[28:].strip("\n").strip("\"")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							d["CDS"][iCds]["color"] = "%s %s"%(d["CDS"][iCds]["color"], line[21:].strip("\n").strip("\""))
							line = f.readline()
							iLine += 1
					# Translation #
					elif line[21:34] == "/translation=":
						d["CDS"][iCds]["translation"] = line[34:].strip("\n").strip("\"")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							d["CDS"][iCds]["translation"] = "%s%s"%(d["CDS"][iCds]["translation"], line[21:].strip("\n").strip("\""))
							line = f.readline()
							iLine += 1
					# Product #
					elif line[21:30] == "/product=":
						d["CDS"][iCds]["product"] = line[30:].strip("\n").strip("\"")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							d["CDS"][iCds]["product"] = "%s %s"%(d["CDS"][iCds]["product"], line[21:].strip("\n").strip("\""))
							line = f.readline()
							iLine += 1
					# Ec_number #
					elif line[21:32] == "/ec_number=":
						d["CDS"][iCds]["ec_number"] = line[32:].strip("\n").strip("\"")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							d["CDS"][iCds]["ec_number"] = "%s %s"%(d["CDS"][iCds]["ec_number"], line[21:].strip("\n").strip("\""))
							line = f.readline()
							iLine += 1
					# Note #
					elif line[21:27] == "/Note=":
						d["CDS"][iCds]["Note"] = line[27:].strip("\n").strip("\"")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							d["CDS"][iCds]["Note"] = "%s %s"%(d["CDS"][iCds]["Note"], line[21:].strip("\n").strip("\""))
							line = f.readline()
							iLine += 1
					# Dbxref #
					elif line[21:29] == "/Dbxref=":
						k = "Dbxref"
						value = line[29:].strip("\n")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							value = "%s%s"%(value, line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
						if k not in d["CDS"][iCds]:
							d["CDS"][iCds][k] = [value.strip(" ").strip("\"")]
						else:
							d["CDS"][iCds][k].append(value.strip(" ").strip("\""))
					# Error Handling for Child Tokens
					elif debugOn == True:
						print(fileName + " Line " + str(iLine) + " Error: " + line.strip("\n"))
						line = f.readline()
						iLine += 1
            #     RNA             1
            #/Note="tRNA-Leu"
            #/Dbxref="FIG_ID:fig|1247.119.rna.1"
			elif line[:21] == "     RNA             ":
				iRna = len(d["RNA"])
				d["RNA"].append({})
				d["RNA"][iRna]["RNA"] = (line[21:].strip("\n"))
				line = f.readline()
				iLine += 1
				while line != "" and line[:21] == "                     " and line[21:22] != "/":
					d["RNA"][iRna]["RNA"] = "%s %s"%(d["RNA"][iRna]["RNA"], line[21:].strip("\n"))
					line = f.readline()
					iLine += 1
				d["RNA"][iRna]["RNA"] = "%s" % (d["RNA"][iRna]["RNA"])
				while line != "" and line[:21] == "                     ":
                     #/Note="tRNA-Leu"
					if line[21:27] == "/Note=":
						d["RNA"][iRna]["Note"] = line[27:].strip("\n")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							d["RNA"][iRna]["Note"] = "%s %s"%(d["RNA"][iRna]["Note"], line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
					# Alias #
					elif line[21:28] == "/Alias=":
						k = "Alias"
						value = line[28:].strip("\n")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							value = "%s%s"%(value, line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
						if k not in d["RNA"][iRna]:
							d["RNA"][iRna][k] = [value.strip(" ").strip("\"")]
						else:
							d["RNA"][iRna][k].append(value.strip(" ").strip("\""))
					# color #
					elif line[21:28] == "/color=":
						k = "color"
						value = line[28:].strip("\n")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							value = "%s%s"%(value, line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
						if k not in d["RNA"][iRna]:
							d["RNA"][iRna][k] = [value.strip(" ").strip("\"")]
						else:
							d["RNA"][iRna][k].append(value.strip(" ").strip("\""))
					# Dbxref #
					elif line[21:29] == "/Dbxref=":
						k = "Dbxref"
						value = line[29:].strip("\n")
						line = f.readline()
						iLine += 1
						while line != "" and line[:21] == "                     " and line[21:22] != "/":
							value = "%s%s"%(value, line[21:].strip("\n"))
							line = f.readline()
							iLine += 1
						if k not in d["CDS"][iRna]:
							d["CDS"][iRna][k] = [value.strip(" ").strip("\"")]
						else:
							d["CDS"][iRna][k].append(value.strip(" ").strip("\""))
					#Error Handling for Child Tokens
					elif debugOn == True:
						print(fileName + " Line " + str(iLine) + " Error: " + line.strip("\n"))
						line = f.readline()
						iLine += 1
			#ORIGIN      
			#        1 gcggacgtgg cggaattggc agacgcgcag gattaaggat cctgtggtag aaataccgta
			#       61 tgggttcgac tcccatcgcc cgcattttag ctctatatcg acaaagattg atatagagct
			#...
			elif line[:12] == "ORIGIN      ":
				line = f.readline()
				iLine += 1
				while line != "" and line[:2] != "//":
					d["ORIGIN"] = "%s%s"%(d["ORIGIN"], line[10:].strip("\n"))
					line = f.readline()
					iLine += 1
				d["ORIGIN"] = "%s" % (d["ORIGIN"].replace(" ",""))
			elif line[:2] == "//": # EOF token
				line = f.readline()
			#Error Handling for Root Tokens
			elif debugOn == True:
				print(fileName + " Line " + str(iLine) + " Error: " + line.strip("\n"))
				line = f.readline()
				iLine += 1

		return(d)

def allGbkToPy(path, debugOn): # Doesn't do anything at the moment
	fileNames = os.listdir(pathArchive)
	i = 0
	while i < len(fileNames):
		if fileNames[i].endswith("gbk") == False:
			fileNames.pop(i)
		else:
			i += 1

	fileNameList = []

	for iFileName, fileName in enumerate(fileNames):
		d = gbkToPy(path, fileName, True)
		# Progress #
		if iFileName % 100 == 0 and debugOn == True:
			x = iFileName / len(fileNames) * 100
			print("%s %" % (x))

def allGbkToJson( path, debugOn ):

	fileNames = os.listdir(path)

	i = 0
	while i < len(fileNames):

		if fileNames[i].endswith("gbk") == False:

			fileNames.pop(i)

		else:

			i += 1

	fileNameList = []

	for iFileName, fileName in enumerate( fileNames ):

		pyData = gbkToPy( path, fileName, True )

		#print( pyData )

		jsonData = json.dumps( pyData, ensure_ascii=False, indent=4 )

		#print( jsonData )

		with open( path + fileName + ".json", 'w', encoding="utf-8" ) as f:

			f.write( jsonData )

		

		''' Old
		rootIdentifier = fileName.rstrip(".gbk").replace(".","_")
		if rootIdentifier[0] in "0123456789":
			rootIdentifier = "_%s" % rootIdentifier
		jsFileName = "%sjs" % (fileName.rstrip("gbk"))
		pyToJsonFile(d=d,rootIdentifier=rootIdentifier,path=path,fileName=jsFileName)
		'''
		# Progress #
		if iFileName % 100 == 0 and debugOn == True:
			print("%f" % (iFileName / len(fileNames) * 100))

def getMajorCapsid(path, debugOn):
	fileNames = os.listdir(path)
	i = 0
	while i < len(fileNames):
		if fileNames[i].endswith("gbk") == False:
			fileNames.pop(i)
		else:
			i += 1

	fileNameList = []

	with open("%s/%s" % (path, "MajorCapsid.txt"), 'w', encoding="utf-8") as f:
		f.write("File Name\tDEFINITION\tCDS-Note\tCDS-translation\n")
		for iFileName, fileName in enumerate(fileNames):
			d = gbkToPy(path, fileName, True)

			for cds in d["CDS"]:
				if "Note" in cds: 
					if cds["Note"].casefold().find("major capsid") >= 0:
						f.write(fileName+"\t")
						#print(d["DEFINITION"])
						f.write(d["DEFINITION"]+"\t")
						#print(cds["Note"])
						f.write(cds["Note"]+"\t")
						#print(cds["translation"])
						f.write(cds["translation"]+"\n")
				else:
					print("Note key does not exist in d[\"CDS\"] for " + fileName + " for " + cds["CDS"])
					f.write(fileName+"\t")
					f.write(d["DEFINITION"]+"\t")
					f.write(cds["CDS"]+"\t")
					f.write("NO NOTE KEY"+"\n")

			# Progress #
			if iFileName % 100 == 0 and debugOn == True:
				x = iFileName / len(fileNames) * 100
				print(x)

def getMajorCapsid_ConvertToFasta(path, debugOn):
	fileNames = os.listdir(path)
	i = 0
	while i < len(fileNames):
		if fileNames[i].endswith("gbk") == False:
			fileNames.pop(i)
		else:
			i += 1

	fileNameList = []

	with open("%s/%s" % (path, "PhantomeCaudoMajorCapsid.fasta"), 'w', encoding="utf-8") as f:
		for iFileName, fileName in enumerate(fileNames):
			d = gbkToPy(path, fileName, debugOn)
			for cds in d["CDS"]:
				if "Note" in cds: 
					if cds["Note"].casefold().find("major capsid") >= 0:
						print(cds)
						if "Alias-geneID" in cds:
							header = ">" + d["source"]["genome_id"].strip("\"") + "|genId:" + cds["Alias-geneID"].strip("\"") + "|" + d["DEFINITION"].strip("\"")
						elif "Alias-gene_name" in cds:
							header = ">" + d["source"]["genome_id"].strip("\"") + "|genNam:" + cds["Alias-gene_name"].strip("\"") + "|" + d["DEFINITION"].strip("\"")
						elif "Alias-protein_id" in cds:
							header = ">" + d["source"]["genome_id"].strip("\"") + "|proId:" + cds["Alias-protein_id"].strip("\"") + "|" + d["DEFINITION"].strip("\"")
						else:
							header = ">" + d["source"]["genome_id"].strip("\"") + "|bp:" + cds["CDS"].strip("\"") + "|" + d["DEFINITION"].strip("\"")
						f.write(header+"\n")
						line = ""
						i = 0
						for c in cds["translation"].strip("\""):
							if i == 80:
								f.write(line+"\n")
								line = c
								i = 1
							else:
								line = "%s%s" % (line, c)
								i += 1
						f.write(line+"\n") # write remaining characters
							
				else:
					print("Note key does not exist in d[\"CDS\"] for " + fileName + " for " + cds["CDS"])

			# Progress #
			if iFileName % 100 == 0 and debugOn == True:
				x = iFileName / len(fileNames) * 100
				print(x)