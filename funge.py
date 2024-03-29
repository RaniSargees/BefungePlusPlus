from display import *
from time import sleep
import random

class Funge:
	def __init__(self, program, stack=[], func={}, buf="", debug=""):
		self.buf = buf
		self.display = Display()
		self.ip = [0,0] #instruction pointer
		self.vec = [1,0] #instruction vector
		self.stack = stack #program stack
		self.grid = [] #program grid
		self.func = func #function dict hexname:(numargs,grid,cache)
		self.string = False
		self.nx = False
		self.skip = False
		self.debug = debug
		#programs must be loaded in as a 2d array of integers
		#blank space in programs should be 32, not 0
		for n,y in enumerate(program):
			self.grid.append([])
			for x in y:
				self.grid[n].append(x)
	@staticmethod
	def addv(m_grid, m_ip, m_vec):
		ip=m_ip[:]
		if (m_vec[0]):
			ip[0]=(ip[0]+m_vec[0])%len(m_grid[ip[1]])
		ip[1]=(ip[1]+m_vec[1])%len(m_grid)
		return ip
	@staticmethod
	def next_instruction(m_grid, m_ip, m_vec):
		ip = m_ip[:]
		comment = 0
		while (len(m_grid[ip[1]])==0 or m_grid[ip[1]][ip[0]]==32 or comment): #skip spaces
			ip = Funge.addv(m_grid, ip, m_vec)
			if (m_grid[ip[1]][ip[0]]==ord(";")):
				comment = not comment
		return m_grid[ip[1]][ip[0]]
	def getch(self):
		if not len(self.buf):
			self.buf = input()+"\n"
		ret = self.buf[0]
		self.buf = self.buf[1:]
		return ret[0]
	def pop(self):
		try: return self.stack.pop()
		except: return 0
	def push(self, val):
		self.stack.append(val)
		return val
	def tick(self):
		ret = 0
		if (not self.string and not self.nx and not self.skip):
			while len(self.grid[self.ip[1]])<=self.ip[0] or self.grid[self.ip[1]][self.ip[0]] == 32: #skip blank
				self.ip = Funge.addv(self.grid, self.ip, self.vec)
			if "d" in self.debug:
				try: #PRETTY DEBUG OUTPUT
					print("-------------------------" + str(self.string))
					print(self.stack)
					print('"'+self.buf+'"')
					print("-------------------------" + str(self.ip))
					pr = [[chr(max(32,y)) for y in x] for x in self.grid]
					pr[self.ip[1]][self.ip[0]]="\033[1;32;40m"+pr[self.ip[1]][self.ip[0]].replace(" ", "_")+"\033[1;37;40m"
					for y in pr: print("".join(y))
				except:()

			if (self.grid[self.ip[1]][self.ip[0]] == ord('"')): #enter string mode
				self.string = True
			if (self.grid[self.ip[1]][self.ip[0]] == ord(';')): #enter no-execute mode
				self.nx = True
			else: #basic operations
				ret = self.op(self.grid[self.ip[1]][self.ip[0]])
		elif ((self.ip[0]>=len(self.grid[self.ip[1]]) or self.grid[self.ip[1]][self.ip[0]] != ord('"')) and self.string): #string mode
			try:self.push(self.grid[self.ip[1]][self.ip[0]])
			except:self.push(32)
		elif (self.ip[0]<len(self.grid[self.ip[1]]) and self.grid[self.ip[1]][self.ip[0]] == ord('"') and self.string):
			self.string=False
		elif (self.ip[0]<len(self.grid[self.ip[1]]) and self.grid[self.ip[1]][self.ip[0]] == ord(';') and self.nx):
			self.nx = False
		elif (self.skip):
			self.skip = False
		self.ip = Funge.addv(self.grid, self.ip, self.vec) #advance ip

		if (ret==0):
			self.display.tick()
			if self.display.pollquit():
				self.display.quit()
				ret = 1

		return ret
	def op(self, op): #basic funge operations
		if (op in [ord(x) for x in "0123456789abcdef"]):
			self.push("0123456789abcdef".index(chr(op)))
		elif (op == ord("k")):
			next = Funge.next_instruction(self.grid, Funge.addv(self.grid, self.ip, self.vec), self.vec)
			count = self.pop()
			if next == ord("k"): count = 0
			if next not in [ord(x) for x in "<>^v?@qn"]:
				for i in range(count): self.op(next)
			else: self.op(next)
		elif (op == ord("^")):
			self.vec = [ 0,-1]
		elif (op == ord("v")):
			self.vec = [ 0, 1]
		elif (op == ord("<")):
			self.vec = [-1, 0]
		elif (op == ord(">")):
			self.vec = [ 1, 0]
		elif (op == ord("?")):
			self.vec=random.choice([[ 0,-1],[ 0, 1],[-1, 0],[ 1, 0]])
		elif (op == ord("_")):
			self.vec = [2*(self.pop()==0)-1,0]
		elif (op == ord("|")):
			self.vec = [0,2*(self.pop()==0)-1]
		elif (op == ord("'")):
			charvec = Funge.addv(self.grid, self.ip, self.vec)
			self.push(self.grid[charvec[1]][charvec[0]])
			self.skip = True
		elif (op == ord("#")):
			self.skip = True
		elif (op == ord("!")):
			self.push(int(not self.pop()))
		elif (op == ord("$")):
			self.pop()
		elif (op == ord("%")):
			b = self.pop()
			self.push(self.pop()%b)
		elif (op == ord("+")):
			self.push(self.pop()+self.pop())
		elif (op == ord("-")):
			b = self.pop()
			self.push(self.pop()-b)
		elif (op == ord("*")):
			self.push(self.pop()*self.pop())
		elif (op == ord("/")):
			b = self.pop()
			self.push(self.pop()//b)
		elif (op == ord("`")):
			self.push(int(self.pop()<self.pop()))
		elif (op == ord(":")):
			a = self.pop()
			self.push(a)
			self.push(a)
		elif (op == ord("\\")):
			if (len(self.stack)):
				a = self.pop()
				b = self.pop()
				self.push(a)
				self.push(b)
			else: self.push(0)
		elif (op == ord(".")):
			print(self.pop(), end="")
		elif (op == ord(",")):
			try: print(chr(self.pop()), end="")
			except: print(chr(self.pop()), end="")
		elif (op == ord("g")):
			y = self.pop()
			x = self.pop()
			if (x<0 or y<0):self.push(0)
			else:
				try:self.push(self.grid[y][x])
				except:self.push(32)
		elif (op == ord("p")):
			y = self.pop()
			x = self.pop()
			n = self.pop()
			if (x<0 and y<0): #non-standard IO memory mapping
				try:self.display.pxput((-x, -y), n)
				except:()
			elif (x<0 or y<0):()
			else:
				if "m" in self.debug:print("SELF MODIFY. put ", n, "at (", x, y, ")")
				while len(self.grid)<=y:
					if "m" in self.debug:print("Y ADD: extended grid")
					self.grid.append([])
				while len(self.grid[y])<=x:
					if "m" in self.debug:print("X ADD: extended grid[",y,"]")
					self.grid[y].append(32)
				self.grid[y][x] = n
		elif (op == ord("~")):
			try:self.push(ord(self.getch()))
			except:self.push(0)
		elif (op == ord("&")):
			try:self.push(int(input()))
			except:self.push(0)
		elif (op == ord("@")):
			return self.stack[:]
		#non-standard functions
		elif (op == ord("u")): #update display
			self.display.update()
		elif (op == ord("x")): #create function
			#pop 0gnirt, height, width, vector (y x), num args
			cachable = True
			fstr = []
			while 1:
				popped = self.pop()
				if (not popped):break
				fstr.append(hex(popped).replace("0x",""))
			fstr = "".join(fstr)
			h = self.pop()
			w = self.pop()
			y = self.pop()
			x = self.pop()
			n = self.pop() #negative argument counts indicate 0gnirts for arguments
			grid = []
			if (min(x,y)<0 or min(h,w)<1):self.vec = [-i for i in self.vec];return 0
			cachable = bool(n);
			try:self.grid[y][x]
			except:self.vec = [-i for i in self.vec];return 0
			for i in range(h):
				try:
					self.grid[y+i]
					grid.append([])
					for j in range(w): #whatever.
						try:
							grid[-1].append(self.grid[y+i][x+j])
							if (self.grid[y+i][x+j] in [ord(x)for x in"p?~&"]):cachable=False
						except:break
				except:break
			self.func[fstr] = (n,grid,{"cachable":cachable})
			if "f" in self.debug:
				print("ADDED FUNC", fstr)
				print("##################")
				try:
					pr = [[chr(max(32,y)) for y in x] for x in grid]
					for y in pr: print("".join(y))
				except:()
				print("##################")
		elif (op == ord("=")): #execute function
			fstr = []
			while 1:
				popped = self.pop()
				if (not popped):break
				fstr.append(hex(popped).replace("0x",""))
			fstr = "".join(fstr)
			args = []
			try:self.func[fstr]
			except:self.vec = [-i for i in self.vec];return 0
			if (self.func[fstr][0]<0):
				for i in range(-self.func[fstr][0]):
					while 1:
						popped = self.pop()
						args.append(popped)
						if (not popped):break;print("BREAK")
			else:
				for i in range(self.func[fstr][0]):
					args.append(self.pop())
			args = args[::-1]
			if "f" in self.debug:print("EXECUTING FUNC", fstr, "WITH ARGS", args, "CACHE", self.func[fstr][-1]["cachable"])
			if self.func[fstr][-1]["cachable"]:
				try:
					self.stack=self.stack+self.func[fstr][-1][str(args)]
					if "f" in self.debug:print(" - GOT RESULT FROM CACHE")
				except:
					if "f" in self.debug:print(" - RESULT NOT CACHED")
					subfunge = Funge(self.func[fstr][1], args, self.func, self.debug)
					exe = 0
					while exe == 0:exe = subfunge.tick()
					if exe==1: return 1
					else:self.func[fstr][-1][str(args)] = exe
					self.stack=self.stack+self.func[fstr][-1][str(args)]
			else:
				subfunge = Funge(self.func[fstr][1], args, self.func, self.buf, self.debug)
				exe = 0
				while exe == 0:exe = subfunge.tick()
				if exe==1: return 1
				else:self.stack=self.stack+exe

		elif (op == ord("n")): #delete function
			fstr = []
			while 1:
				popped = self.pop()
				if (not popped):break
				fstr.append(hex(popped).replace("0x",""))
			fstr = "".join(fstr)
			try:self.func[fstr]
			except:self.vec = [-i for i in self.vec];return 0
			del self.func[fstr]
		elif (op == ord("z") and "p" in self.debug): #pause - debugging mode only
			sleep(1)
		return 0
