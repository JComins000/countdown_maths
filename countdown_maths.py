import sys
import operator as op

four_operations = op.add, op.sub, op.mul, op.floordiv

def get_other_numbers(numbers):
	return [(n, numbers[:i] + numbers[i+1:]) for i, n in enumerate(numbers)]

class node(object):
	def __init__(self, numbers):
		self.parent = None
		self.leaves = []
		for n, others in get_other_numbers(numbers):
			self.leaves.append(arithmatic_node(n, others, self))

	def path(self):
		return ""

class operation_node(node):
	def __init__(self, numbers, operation, parent=None, parens=False):
		self.operation = operation
		self.parent = parent
		self.leaves = []
		self.parens = parens
		for n, others in get_other_numbers(numbers):
			self.leaves.append(arithmatic_node(n, others, self))

	def path(self):
		options = {op.add: " + ",
				   op.sub: " - ",
				   op.mul: " * ",
				   op.floordiv: " / ",
		}
		if self.parens:
			return self.parent.path() + '(' + options[self.operation] + ')'
		return self.parent.path() + options[self.operation]

class arithmatic_node(node):
	def __init__(self, x, other_numbers, parent=None):
		self.parent = parent
		self.x = x
		self.partial_sum = 0
		self.multiplicand = x

		if type(parent) is operation_node:
			operation = self.parent.operation
			if (operation is op.add or operation is op.sub) and not self.parent.parens:
				self.partial_sum = self.parent.parent.ans()
				self.multiplicand = operation(0, x)
			else:
				if operation is op.floordiv and self.parent.parent.multiplicand % x:
					return
				self.partial_sum = self.parent.parent.partial_sum
				self.multiplicand = operation(self.parent.parent.multiplicand, x)
		
		submit_solution(self.ans(), self)
		self.leaves = []

		if other_numbers:
			for operation in four_operations:
				self.leaves.append(operation_node(other_numbers, operation, self))
			self.leaves.append(operation_node(other_numbers, op.add, self, True))
			self.leaves.append(operation_node(other_numbers, op.sub, self, True))

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

	tree = node(numbers)
	if target in solutions:
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