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


class HeapPriorityQueue(PriorityQueueBase): #Recall _Item is defined in base class
	"""A min-oriented priority queue implemented using a heap"""
	#--------------------------Nonpublic Methods-------------------------
	def _parent(self, j):
		return (j-1)//2

	def _left(self, j):
		return 2*j + 1

	def _right(self, j);
		return 2*j + 2

	def _has_left(self, j):
		return self._left(j) < len(self._data) #Is index before end of the array?

	def _has_right(self, j):
		return self._right(j) < len(self._data) #Is index before end of the array?

	def _swap(self, i, j):
		"""Swap items at positions i and j of the array"""
		self._data[i], self._data[j] = self._data[j], self._data[i]

	#looks smirnoff - to be corrected
	def _upheap(self, j):
		"""Recursive upheap to insert new elements. 
		Swaps items until key order is restored"""
		parent = self._parent(j)
		if j > 0 and  self._data[j] < self._data[parent]:
			self._swap(j, parent)
			self._upheap(parent)

	def _downheap(self, j):
		if self._has_left(j):
			left = self._left(j)
			small_child = left #Although right could be smaller
			if self._has_right(j):
				right = self._right(j)
				if self._data[right] < self._data[left]:
					small_child = right
			if self._data[small_child] < self._data[j]:
				self._swap(small_child, j)
				self._downheap(small_child) #recur at position of smallest child

	#----------------------------------Public Methods---------------------------------
	def __init__(self):
		"""Create empty priority queue"""
		self._data = []

	def __len__(self):
		"""Return number of items in priority queue"""
		return len(self._data)

	def add(self, key, value):
		"""add a key-value pair to priority queue"""
		self._data.append(self._Item(key, value))
		self._upheap(len(self._data) -1) #upheap newly added position

	def min(self):
		"""Return but do not remove tuple (k,v) with minimum key k.
		Raise Empty if queue is empty"""
		if self.is_empty():
			raise  Empty("Priority Queue is empty")
		item = self._data[0]
		return (item._key, item._value)

	def remove_min(self):
		""""Return and remove tuple (k,v) with minimum key k.
		Raise empty if queue is empty."""
		if self.is_empty():
			raise  Empty("Priority Queue is empty")
		self._swap(0, len(data) - 1) #Put element at the end
		item = self._data.pop() #remove it from array
		self._downheap(0) #Fix new root
		return (item._key, item._value)
