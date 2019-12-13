import sys
from funge import *
# debugging params.
#	d: list program each step
#	m: self modify
#	f: function call/def
#	p: pause on "z"
if len(sys.argv) > 1:
	with open(sys.argv[1], "r") as f:
		program = [[ord(x) for x in y]for y in f.readlines()]
		if len(sys.argv)>2:funge = Funge(program, debug=sys.argv[2])
		else: funge=Funge(program, [], {}, "")
		hlt = 0
		while hlt==0:
			hlt = funge.tick()
else:
	print ("INVALID ARGUMENTS")
