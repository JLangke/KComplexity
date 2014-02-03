from math import log
def lg(x): return log(x) / log(2)

def varies(prog):
	return "x" in prog or "y" in prog

def genAll(size, t, notsOk=True):
	if size <= 0: return
	if t == 'bool':
		if size == 1:
			yield "#t"
			yield "#f"
		else:
			if notsOk:
				for x in genAll(size-1, "bool", notsOk=False):
					if varies(x):
						yield "(not " + x + ")"
			for spl in range(1, size-1):
				for left in genAll(spl, "bool"):
					for right in genAll(size-1-spl, "bool"):
						if varies(right) and varies(left):
							yield "(and " + left + " " + right + ")"
							yield "(or " + left + " " + right + ")"
				for left in genAll(spl, "int"):
					for right in genAll(size-1-spl, "int"):
						if varies(left) or varies(right):
							yield "(< " + left + " " + right + ")"
	elif t == 'int':
		if size == 1:
			yield "0"
			yield "1"
			yield "x"
			yield "y"
		else:
			for spl in range(1, size-1):
				for left in genAll(spl, "int"):
					for right in genAll(size-1-spl, "int"):
						yield "(+ " + left + " " + right + ")"
						yield "(* " + left + " " + right + ")"
		

height = 3
width = 3

def start_racket():
	import subprocess
	p = subprocess.Popen("racket", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	print p.stdout.readline()

	print >>p.stdin, "(define height", height, ")"
	print >>p.stdin, "(define width", width, ")"
	print >>p.stdin, """(define tf-fn-to-number
	  (lambda (f)
	    (define g
	      (lambda (x y)
		(cond 
		  ((f x y) 1)
		  (else 0))))

	    (define build-number
	      (lambda (x y c)
		(cond 
		  ((and (< x width) (< y height)) (+ (arithmetic-shift (g x y) c) 
						     (build-number (+ 1 x) y (+ 1 c))))
		  ((< y height) (build-number 0 (+ 1 y) c))
		  (else 0))))

	    (build-number 0 0 0)))

	(define ns (make-base-namespace))
	(define program-to-procedure (lambda (p) (eval p ns)))"""
	return p

numbers = {}
#for line in open('data'):
	#size, n, prog = line.split(" ", 2)
	#size = int(size)
	#n = int(n)
	#numbers[n] = (size, prog)
#size += 1 #assume the data in 'data' is complete for each level
size = 1

rackets = [ start_racket() for i in range(11) ]

while len(numbers) < 2**(width*height):
	print "Generating size", size
	count = 0
	for prog in genAll(size, "bool"):
		if count % 100000 == 0:
			print count

		# Every numProcs trips through the loop, drain each
		# communication channel
		if 0 == (count % len(rackets)) and count != 0:
			for p in rackets:
				out = int(p.stdout.readline().split()[-1])
				if out not in numbers:
					numbers[out] = (size, p.prog)
					print size, out, p.prog
				
		# Put the current program in the next channel in line
		rackets[count % len(rackets)].prog = prog
		print >>rackets[count % len(rackets)].stdin, "(tf-fn-to-number (program-to-procedure '(lambda (x y)", prog + ")))"
		count += 1

	# Drain the remaining programs in case the number of generated programs
	# for a given size is not 0 mod the number of processors
	for i in range(0, count % len(rackets)):
		p = rackets[i]
		out = int(p.stdout.readline().split()[-1])
		if out not in numbers:
			numbers[out] = (size, p.prog)
			print size, out, p.prog
		
	size += 1

for p in rackets:
	print >>p.stdin, "(exit)"
