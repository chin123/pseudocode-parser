import re
import sys
import string

def typeline(curline):
	i = curline.split()
	if "for" in i:
		return "for"
	if "while" in i:
		return "while"
	if "do" in i:
		return "do"
	if "endif" in i:
		return "endif"
	for k in ["next", "endwhile", "endfunction", "endprocedure"]:
		if k in i:
			return "end"
	if "endswitch" in i:
		return "endswitch"
	if "until" in i:
		return "until"
	if "if" in i:
		return "if"
	if "elseif" in i:
		return "if"
	if "else" in i:
		return "if"
	if "switch" in i:
		return "switch"
	if "case" in i:
		return "case"
	for k in ["function", "procedure"]:
		if k in i:
			return "function"
	if "array" in i:
		return "array"
	return "stmt"

def retelems(curline):
	elems = re.split("(\+|\-|\/|\*|\=|to |\!| |\n|\t|\:|\^|\.|\(|\)|\,|\[|\]|\'|\")",curline)
	return elems

def formatstmt(elems):
	for i in range(0,len(elems)):
		if elems[i] == "AND":
			elems[i] = "and"
		elif elems[i] == "OR":
			elems[i] = "or"
		elif elems[i] == "NOT":
			elems[i] = "not"
		elif elems[i] == "MOD":
			elems[i] = "%"
		elif elems[i] == "DIV":
			elems[i] = "//"
		elif elems[i] == "^":
			elems[i] = "**"
		elif elems[i] == "elseif":
			elems[i] = "elif"
			
	if "." in elems:
		print("dot detected")
		print(elems)
		if "substring" in elems:
			pos = elems.index("substring") - 1
			startpos = elems[pos+3]
			stlen = elems[pos+5]
			print("substring detected")
			print(elems[:pos])
			print(elems[pos+7:])
			print(elems)
			if len(elems) == pos+1+6:
				elems = elems[:pos]
			else:
				elems = elems[:pos] + elems[pos+7:]
			elems.insert(pos, "[" + startpos + ":" + str(int(startpos) + int(stlen)) + "]")
		if "length" in elems:
			pos = elems.index("length") - 1
			elems.pop(pos)
			elems.pop(pos)
			pos -= 1
			elems[pos] = "len(" + elems[pos] + ")"
		if "readLine" in elems:
			pos = elems.index("readLine")
			elems[pos] = "readline"
		if "writeLine" in elems:
			pos = elems.index("writeLine")
			elems[pos] = "write"
		if "endOfFile" in elems:
			print("eof detected")
			pos = elems.index("endOfFile") - 1
			elems.pop(pos)
			elems.pop(pos)
			elems.pop(pos)
			elems.pop(pos)
			pos -= 1
			elems[pos] = "eof(" + elems[pos] + ")"
			
	for i in range(len(elems)):
		if elems[i] == '[':
			counter = 0
			while elems[i] != ']':
				if elems[i] == "," and counter == 0:
					elems[i] = "]["
					break
				if elems[i] == ")":
					counter -= 1
				if elems[i] == "(":
					counter += 1
				i += 1
	if "openRead" in elems:
		pos = elems.index("openRead")
		elems[pos] = "open"
		
	if "openWrite" in elems:
		pos = elems.index("openWrite")
		elems[pos] = "open"
		pos2 = elems.index(")")
		elems[pos2-1] += ", \"w\""
		
	retstr = ""
	for i in range(len(elems)):
		retstr += elems[i]
		if i != len(elems) - 1:
			if elems[i] in ["for", "while", "if","and","or","not","return","else","elif"]:
				retstr += ' '
			if elems[i+1] in ["or","and","not"]:
				retstr += ' '
			if elems[i][-1].isalnum() and elems[i+1][0].isalnum() and elems[i] not in ["for", "while", "if","and","or","not","return","else","elif"] and elems[i+1] not in ["for", "while", "if","and","or","not","return","else","elif"]:
				retstr += ' '
	return retstr
				

notabs = 0
a = open(sys.argv[1], "r").readlines()
b = open("output.py", "w")
b.write("def eof(fp):\n\tans=fp.read(1)\n\tfp.seek(fp.tell()-1)\n\treturn not ans\n\n")
comp = ""
for i in a:
	incase = 0
	i = i.lstrip()
	i = i.rstrip()
	print("notabs = " + str(notabs))
	pyline = ""
	pyline += "\t" * notabs
	elems = retelems(i)
	elems = list(filter(None, elems))
	elems = [x for x in elems if x != " "]
	if typeline(i) == "stmt":
		sides = i.split("=")
		pyline += formatstmt(elems)
	if typeline(i) == "for":
		print("elems are: ")
		print(elems)
		pyline += "for " + elems[1] + " in range(" + elems[3] + ", " + elems[5] + "):"
		notabs += 1
	if typeline(i) == "while":
		pyline += formatstmt(elems) + ":"
		notabs += 1
	if typeline(i) == "do":
		pyline += "while True:\n"
		notabs += 1
	if typeline(i) == "end":
		notabs -= 1
	if typeline(i) == "endif":
		comp = ""
	if typeline(i) == "until":
		elems[0] = "if "
		pyline += formatstmt(elems) + ":\n" + "\t"*(notabs+1) + "break"
		notabs -= 1
	if typeline(i) == "if":
		elems = [x for x in elems if x != "then"]
		pyline += formatstmt(elems) + ":"
		#notabs += 1
		comp = "a"
		incase = 1
	if typeline(i) == "switch":
		comp = elems[1]
	if typeline(i) == "case":
		pyline += "if " + comp + " == " + elems[1] + ":"
		incase = 1
	if typeline(i) == "endswitch":
		comp = ""
	if typeline(i) == "function":
		temp = i.split()
		temp[0] = "def"
		for t in temp:
			pyline += t + " "
		pyline += ":"
		notabs += 1
	if typeline(i) == "array":
		varname = elems[1]
		if "," not in i:
			varsize = elems[3]
			pyline += varname + " = [0] * " + varsize
		else:
			h = elems[3]
			w = elems[5]
			pyline += varname + " = [[0 for x in range(" + w + ")] for y in range(" + h + ")]" 
		
	if comp != "" and incase == 0:
		pyline = "\t" + pyline
	pyline = pyline.replace("//","#")
	b.write(pyline + "\n")

