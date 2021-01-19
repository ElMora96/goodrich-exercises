#Stack basic ADT
#New, basic Exception for implementing Stack
class Empty(Exception):
	"""Error attempting to access an element from an empty container."""
	pass

class ArrayStack:
	"""Stack (LIFO) implemented using a Python list (adapter pattern)."""
	def __init__(self):
		"""Create an empty stack"""
		self._data = []

	def __len__(self):
		"""Return number of elements in the stack"""
		return len(self._data)

	def is_empty(self):
		"""Return True if stack is empty"""
		return len(self._data) == 0

	def push(self, e):
		"""Add an element at the top of the stack"""
		self._data.append(e)

	def first(self):
		"""Return first element of the stack without removing it.
		Raise Empty Exception if stack is empty."""
		if self.is_empty():
			raise Empty
		return self._data[-1]

	def pop(self):
		"""Remove and return first element of the stack.
		Raise Empty Exception if stack is empty."""
		if self.is_empty():
			raise Empty
		return self._data.pop()