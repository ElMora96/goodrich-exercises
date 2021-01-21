"""Although we have used a doubly linked list to implement the positional
list ADT, it is possible to support the ADT with an array-based implementation. The key is to use the composition pattern and store a sequence
of position items, where each item stores an element as well as that element’s current index in the array. Whenever an element’s place in the array
is changed, the recorded index in the position must be updated to match.
Give a complete class providing such an array-based implementation of
the positional list ADT. What is the efficiency of the various operations?"""	
from libs.stack import Empty

class ArrayPositionalList:
	"""Sequential container of elements allowing positional access.
	Uses an array as underlying storage"""
	INITIAL_CAPACITY = 10 #Initial size for dynamic array used to store data
	#---------------------Nested Position Class-----------------------
	class Position:
		"""Abstraction representing position of single element"""
		def __init__(self, container, index):
			"""Constructor should not be invoked by user"""
			self._container = container
			self._index = index #current index in storage array
			self._element = container._data[self._index]

		def element(self):
			"""Return element stored at this position"""
			return self._element

		def __eq__(self, other):
			"""Return True if other is a Position representing the same location"""
			return type(other) is type(self) and self._index == other._index and self._element == other._element

		def  __ne__(self, other):
			"""Return True if other represents a different location"""
			return not self == other
	#---------------------------Positional List - Nonpublic Methods-----------------------
	def _make_position(self, index):
		"""Return position index for given index"""
		if index < 0 or index >= len(self._data):
			raise ValueError("This index is invalid")
		return self.Position(self, index)


	#---------------------------Positional List - Public Methods-----------------------
	def __init__(self):
		"""Create an empty positional list"""
		self._data = [None] * INITIAL_CAPACITY
		self._size = 0

	def __len__(self):
		"""Return number of elements in the PL"""
		return self._size

	def is_empty(self):
		"""Return True if PL contains no elements"""
		return len(self) == 0

	def first(self):
		"""Return first Position of PositionalList (or None if PositionalList is empty)"""
		if self.is_empty():
			return None
		else:
			return self._make_position(0) #position of first element

	def last(self):
		"""Return the last Position in PositionalList (or None if PositionalList is empty)"""
		if self.is_empty():
			return None
		else:
			last = (self._size - 1)
			return self._make_position(last) #position of last element
