import sys
import operator as op

four_operations = op.add, op.sub, op.mul, op.floordiv

class node(object):
	def __init__(self):
		self.parent = None
		self.leaves = []
		self.numbers = []

	def path(self):
		return ""

class root(node):
	def __init__(self):
		super().__init__()	

	def new_number(self, x):
		for leaf in self.leaves:
			leaf.new_number(x)
		new_leaf = arithmetic_node(x, self)
		for n in self.numbers:
			new_leaf.new_number(n)
		self.leaves.append(new_leaf)
		self.numbers.append(x)

class operation_node(node):
	def __init__(self, operation, parent, parens=False):
		super().__init__()
		self.operation = operation
		self.parent = parent
		self.parens = parens

	def new_number(self, x):
		if self.operation is op.floordiv and self.parent.multiplicand % x:
			return
		for leaf in self.leaves:
			leaf.new_number(x)
		new_leaf = arithmetic_node(x, self)
		for n in self.parent.numbers:
			new_leaf.new_number(n)
		self.leaves.append(new_leaf)

	def path(self):
		options = {op.add: " + ",
				   op.sub: " - ",
				   op.mul: " * ",
				   op.floordiv: " / ",
		}
		if self.parens:
			return self.parent.path() + '(' + options[self.operation] + ')'
		return self.parent.path() + options[self.operation]

class arithmetic_node(node):
	def __init__(self, x, parent):
		super().__init__()
		self.parent = parent
		self.x = x
		for operation in four_operations:
			self.leaves.append(operation_node(operation, self))
		self.leaves.append(operation_node(op.add, self, parens=True))
		self.leaves.append(operation_node(op.sub, self, parens=True))

		if type(self.parent) is root:
			self.partial_sum = 0
			self.multiplicand = x
		else:
			operation = self.parent.operation
			if (operation is op.add or operation is op.sub) and not self.parent.parens:
				self.partial_sum = self.parent.parent.ans()
				self.multiplicand = operation(0, x)
			else:
				self.partial_sum = self.parent.parent.partial_sum
				self.multiplicand = operation(self.parent.parent.multiplicand, x)
		
		submit_solution(self.ans(), self)

	def new_number(self, x):
		for leaf in self.leaves:
			leaf.new_number(x)
		self.numbers.append(x)

	def ans(self):
		return self.partial_sum + self.multiplicand

	def path(self):
		return self.parent.path() + str(self.x)

def switch_neighboring_indices(s, i):
	return s[:i] + s[i+1] + s[i] + s[i+2:]

def repair_parens(s):
	open_parens = [i for i, letter in enumerate(s) if letter == '(']
	for i in open_parens:
		s = switch_neighboring_indices(s, i-1)
		s = switch_neighboring_indices(s, i+4)
	return s.replace('()','')

def print_answer(target, expression, flush=False):
	print(target, ': ', repair_parens(expression), flush=flush)

def quit():
	print('Usage: countdown_maths.py [target] [6 numbers]')
	exit()

if __name__ == '__main__':
	if len(sys.argv) < 8:
		quit()
	try:
		target = int(sys.argv[1])
		numbers = [int(n) for n in sys.argv[2:]]
	except:
		quit()

	solutions = {}
	def submit_solution(sol, node):
		if sol in solutions:
			solutions[sol] += [node]
		else:
			solutions[sol] = [node]
		if sol == target:
			print_answer(target, node.path(), flush=True)


	tree = root()
	for n in numbers:
		tree.new_number(n)
	if target in solutions:
		print(len(solutions[target], "solutions"))
		exit()
	
	distances = [(0,)]
	for i in range(1,11):
		distances += [(i, -i)]

	target_reached = False
	for distance in distances:
		targets = [d + target for d in distance]
		for t in targets:
			if t in solutions:
				for sol in solutions[t]:
					print_answer(t, sol.path())
				target_reached = True
		if target_reached:
			exit()
		else:
			print('No solution', targets)