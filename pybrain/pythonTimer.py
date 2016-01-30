import multiprocessing
from time import sleep
from multiprocessing import Value


def timer(val,num):
	for i in range(0, 60):
		sleep(num)
		if(val.value==0 and i==59):	
			print "Arrived" #play recording

v = Value('i',0)
p = multiprocessing.Process(target=timer, args = (v,3))

minutes = 3 #input from switch- 3 or 5
newInput = False #based from buttons
v.value =0
if(minutes ==3):
	p.start()
#sleep(2.0)	#test lines
#newInput = False #test lines


if(newInput == True): #check periodically??????
	v.value=1
	p.terminate
