from __future__ import print_function
from subprocess import call
import os, time
path_to_watch = "../reminders/"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
d= open('bahahaha.txt', 'a') 
while True:
	
	d.write('becca'+'\n')
	after = dict ([(f, None) for f in os.listdir (path_to_watch)])
	added = [f for f in after if not f in before]
	removed = [f for f in before if not f in after]
	if added: print ("Added: ", ", ".join (added))
	if removed: print ("Removed: ", ", ".join (removed))
	before = after
