from libs.stack import Empty
#Link-Based Data Structures
class LinkedStack:
	"""Stack (LIFO) implemented using a linked list as storage"""

	#-------------------------Nested Node Class----------------------
	class _Node:
		"""Lighweight, nonpublic class to represent nodes of linked list"""
		__slots__ = '_element', '_next' #reduce memory usage

		def __init__(self, data, next):
			"""Create new node"""
			self._data = data #reference to user's element
			self._next = next #reference to next node

	#----------------------- Stack-----------------------------------
	def __init__(self):
		"""Create an empty stack"""
		self._head = None #Reference to head of linked list
		self._size = 0

	def __len__(self):
		"""Return number of elements in the stack"""
		return self._size

	def is_empty(self):
		"""Return True if the stack is empty"""
		return self._size == 0

	def push(self, e):
		"""Add an element at the top of the stack"""
		new_node = _Node(e, self._head)
		self._head = new_node
		self._size +=1

	def top(self):
		"""Return top element of the stack without removing it.
		Raise empty exception if the stack is empty."""
		if self.is_empty():
			raise Empty
		return self._head._data

	def pop(self):
		"""Return and remove top element of the stack.
		Raise empty exception if the stack is empty."""
		if self.is_empty():
			raise Empty
		value = self._head.data #Store value to return
		self._head = self._head._next #Reassign head of linked list to next element
		self._size -= 1
		return value


class LinkedQueue:
	"""Queue (FIFO semantics) implemented using a linked list as storage.
	Keep a reference to the tail of the list to perform enque.
	Align the front of the queue with the head of the list, and the back
	of the queue with the tail of the list."""
	#------------------------Nested Node class-----------------------------
	class _Node:
		"""Lighweight, nonpublic class to represent nodes of linked list"""
		__slots__ = '_element', '_next' #reduce memory usage

		def __init__(self, data, next):
			"""Create new node"""
			self._data = data #reference to user's element
			self._next = next #reference to next node

	#-----------------------------Queue-----------------------------------
	def __init__(self):
		"""Create an empty queue"""
		self._head = None
		self._tail = None
		self._size = 0

	def __len__(self):
		"""Return number of elements in queue"""
		return self._size

	def is_empty(self):
		"""Return True if the queue is empty"""
		return self._size == 0

	def first(self):
		"""Return without removing the first element of the queue
		Raise Empty if queue is empty"""
		if self.is_empty():
			raise Empty
		return self._head._data

	def dequeue(self):
		"""Return and remove the first element of the queue.
		Raise empty if queue is empty"""
		if self.is_empty():
			raise Empty
		value = self._head._data #store value to be returned
		self._head = self._head._next #Set new head
		self._size -= 1 #Decrease queue size
		if len(self) == 0:
			self._tail = None #Special case when removing last element of the queue
		return value


	def enque(self, e):
		"""Add element to the back of the queue"""
		if self.is_empty():
			self._head = self._tail = self._Node(e, None) #initialize head and tail of the queue
		else:
			self._tail._next = self._Node(e, None)
		self._size += 1

class CircularQueue:
	"""Queue (FIFO) implemented using circularly linked list as storage"""
	#------------------------Nested Node class-----------------------------
	class _Node:
		"""Lighweight, nonpublic class to represent nodes of linked list"""
		__slots__ = '_element', '_next' #reduce memory usage

		def __init__(self, data, next):
			"""Create new node"""
			self._data = data #reference to user's element
			self._next = next #reference to next node
	
	#---------------------------Circular Queue----------------------------
	def __init__(self):
		"""Create an empty queue. Notice in this case we only keep reference to the tail of the queue,
		since its head can be retrieved as the tail's next."""
		self._tail = None
		self._size = 0

	def __len__(self):
		"""Return number of elements in queue"""
		return self._size

	def is_empty(self):
		"""Return True if the queue is empty"""
		return self._size == 0

	def first(self):
		"""Return without removing the first element of the queue
		Raise Empty if queue is empty"""
		if self.is_empty():
			raise Empty
		head = self._tail._next
		return head._data

	def dequeue(self):
		"""Return and remove the first element of the queue.
		Raise empty if queue is empty"""
		if self.is_empty():
			raise Empty			
		old_head = self._tail._next #Reference to old head to be removed
		if self._size == 1:
			self._tail = None #Set tail to None if we're removing the only element in queue
		else:
			self._tail._next = old_head._next
		self._size -= 1 #Decrease queue size
		return old_head._data

	def enqueue(self, e):
		"""Add element to the back of the queue"""
		new_node = self._Node(e, None)
		if self.is_empty():
			self._tail = new_node
		else:
			new_node._next = self._tail