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
	#---------------------Nested Position Class-----------------------
	class Position:
		"""Abstraction representing position of single element"""
		def __init__(self, container, element, index):
			"""Constructor should not be invoked by user"""
			self._container = container
			self._element = element
			self._index = index #Index in storage array

		def 