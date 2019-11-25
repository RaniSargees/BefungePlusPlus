import sys
from funge import *

if len(sys.argv) > 1:
	with open(sys.argv[1], "r") as f:
		program = [[ord(x) for x in y]for y in f.readlines()]
		if len(sys.argv)>2:[print(x) for x in program]
		funge = Funge(program, [], {}, len (sys.argv)>2)
		hlt = 0
		while hlt==0:
			hlt = funge.tick()
else:
	print ("INVALID ARGUMENTS")
