"""
pseudocode-parser: parses pseudocode and outputs it's python equivalent into output.py
Copyright (C) 2018  Chinmaya Krishnan Mahesh

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import re
import sys
import string

# prints usage
def usage():
	print("USAGE:")
	print("python main.py <pseudocode file> <output file>")
	print("python main.py --license")
	print("python main.py -l")

# finds the purpose of the line read
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

# tokenizes the line into useful elements
def retelems(curline):
	elems = re.split("(\+|\-|\/|\*|\=|to |\!| |\n|\t|\:|\^|\.|\(|\)|\,|\[|\]|\'|\")",curline)
	b = len(elems)
	i = 0
	while i < b:
		if elems[i] == "\"":
			pos = elems[i+1:].index("\"") + i + 1
			while elems[i+1] != "\"":
				elems[i] += elems[i+1]
				elems.pop(i+1)
				b -= 1
			elems[i] += "\""
			elems.pop(i+1)
			b -= 1
		i += 1

	elems = list(filter(None, elems))
	b = len(elems)
	print("b=" + str(b))
	i = 0
	pos = -1
	while i < b:
		print("i=" + str(i))
		if elems[i] == "/":
			print("slash detected")
			if elems[i+1] == "/":
				print("comment detected")
				pos = i
				break
		i += 1
	if pos != -1:
		comstart = curline.rfind("//") + 2
		comment = "#" + curline[comstart:]
		elems[pos] = comment
		elems = elems[:pos+1]
		
		
	return elems

# converts pseudocode tokens and functions into valid python ones
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
				

notabs = 0 # keeps track of the number of tabs to place before the line for indentation

if len(sys.argv) == 1:
	print("Not enough arguements!")
	usage()
	sys.exit()

if len(sys.argv) == 2:
	if sys.argv[1] == "--license" or sys.argv[1] == "-l":
		print("pseudocode-parser: parses pseudocode and outputs it's python equivalent.")
		print("Copyright (C) 2018  Chinmaya Krishnan Mahesh")

		print("This program is free software: you can redistribute it and/or modify")
		print("it under the terms of the GNU General Public License as published by")
		print("the Free Software Foundation, either version 3 of the License, or")
		print("(at your option) any later version.")
		print()
		print("This program is distributed in the hope that it will be useful,")
		print("but WITHOUT ANY WARRANTY; without even the implied warranty of")
		print("MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the")
		print("GNU General Public License for more details.")
		print()
		print("You should have received a copy of the GNU General Public License")
		print("along with this program. If not, see <http://www.gnu.org/licenses/>.")
	elif sys.argv[1][0] == "-":
		print("Option " + sys.argv[1] + " not recognised!")
		usage()
	else:
		print("Incorrect usage!")
		usage()
	sys.exit()
		

a = open(sys.argv[1], "r").readlines() # input is read line by line
b = open(sys.argv[2], "w")

b.write("def eof(fp):\n\tans=fp.read(1)\n\tfp.seek(fp.tell()-1)\n\treturn not ans\n\n") # hacky solution for an eof function
comp = "" # used to maintain indentation in switch and if blocks
for i in a:
	incase = 0
	i = i.lstrip()
	i = i.rstrip()
	print("notabs = " + str(notabs))
	pyline = "" # stores line to write to file
	pyline += "\t" * notabs
	elems = retelems(i)
	elems = list(filter(None, elems)) # remove all null elements
	elems = [x for x in elems if x != " "] # remove all space elements
	print("===elems===")
	print(elems)
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
	b.write(pyline + "\n")
