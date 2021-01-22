from  libs.positional_list import PositionalList #For the implementations based on a list
from libs.stack import Empty
class PriorityQueueBase:
	"""Abstract base class for a priority queue"""
	class _Item:
		"""Lightweight composite to store priority queue items"""
		__slots__ = '_key', '_value'

		def __init__(self, k, v):
			self._key = k
			self._value = v

		def __lt__(self, other):
			"""Compare elements based on their keys"""
			return self._key < other._key

	def is_empty(self): 	#Concrete method relying upon len
		"""Return True if queue is empty"""
		return len(self) == 0

class UnsortedPriorityQueue(PriorityQueueBase):
	"""Concrete implementation of min-oriented priority queue using an unsorted (positional) list to store items"""
	def _find_min(self): #Nonpublic utility
		"""Return Position of item with minimum key"""
		if self.is_empty():
			raise Empty("This priority queue is empty")
		trav = self._data.first()
		small = trav
		while trav: #traverse all positional list & find minimum
			if trav.element() < small.element():
				small = trav
			trav = self._data.after(trav)
		return trav

	def __init__(self):
		"""Create an empty priority queue"""
		self._data = PositionalList()

	def __len__(self):
		"""Return number of items in queue"""
		return len(self._data)

	def add(self, key, value):
		"""Add an item to queue as a key-value pair"""
		self._data.add_last(self._Item(key, value))

	def min(self):
		"""Return but do not remove tuple (k,v) with minimum key k"""
		position = self._find_min()
		item = position.element()
		return (item._key, item._value)

	def remove_min(self):
		"""Return and remove tuple (k, v) with minimum key k"""
		position = self._find_min()
		item = self._data.delete(position)
		return (item._key, item._value)

class SortedPriorityQueue(PriorityQueueBase):
	"""Concrete implementation of a priority queue using a sorted positional list to store items"""
	def __init__(self):
		"""Create an empty priority queue"""
		self._data = PositionalList()

	def __len__(self):
		"""Return number of items in queue"""
		return len(self._data)

	def add(self, key, value):
		"""Add an item to the priority queue (key-value pair)"""
		new_item = self._Item(key, value)
		trav = self._data.last() #traverse list backwards
		while trav is not None and new_item < trav.element():
			trav = self._data.before(trav)
		if trav is None:
			self._data.add_first(new_item) #new first item of the queue
		else:
			self._data.add_after(new_item, trav) #new item goes after trav

	def min(self):
		"""Return but do not remove tuple (k,v) with minimum key k"""
		item = self._data.first().element()
		return (item._key, item._value)

	def remove_min(self):
		"""Return and remove tuple (k, v) with minimum key k"""
		item = self._data.delete(self._data.first()) #Minimum element is the first
		return (item._key, item._value)