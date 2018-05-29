def eof(fp):
	ans=fp.read(1)
	fp.seek(fp.tell()-1)
	return not ans

def sayhi(name) :
	print("hello"+name)
	

def outputzero(x,y) :
	return 0#Comment 1
	

#Comment 2

x=3
print(x)
for i in range(1, 10):
	print(i)
	

while x!=5:
	print(x)
	x+=1
	

while True:

	answer=input("What's the password?")
	if answer=="computer":
		break

if x==5 or x==3**2:
	print(x)
elif x==7:
	print(x+6)
else:
	print("hello,world")


	
if x == 1:
	print("it\'s 1")
if x == 5:
	print("it\'s 5")


y="hello"
print(len(y))
print(y[1:3])

sayhi("chinmaya")

names = [0] * 5

names[0]="Ahmad"
names[1]="Ben"
names[2]="Catherine"
names[3]="Dana"
names[4]="Elijah"

print(names[3])

board = [[0 for x in range(8)] for y in range(8)]

board[outputzero(5,4)][0]="rook"
myFile=open("sample.txt")
x=myFile.readline()
myFile.close()

myFile=open("sample.txt")
while  not eof(myFile):
	print(myFile.readline())
	
myFile.close()

myFile=open("sample.txt", "w")
myFile.write("Hello World")
myFile.close()
