"""Give a complete ArrayDeque implementation of the double-ended queue
ADT as sketched in Section 6.3.2."""
from libs.stack import Empty
class ArrayDeque:
	"""(Circular) Array-based Double-Ended Queue implementation."""
	INITIAL_CAPACITY = 10 #Initial size for dynamic array used to store data

	def __init__(self):
		"""Create and empty deque"""
		self._data = [None] * 10
		self._size = 0 #elements in deck
		self._front = 0 #Reference to front of the queue

	def __len__(self):
		"""Return number of elements in the deque"""
		return self._size

	def is_empty(self):
		"""Return True if deck contains no elements"""
		return len(self) == 0

	def first(self):
		"""Return (but do not remove) the first element of the deck.
		Raise empty exception if deck is empty"""
		if self.is_empty():
			raise Empty("Deque is empty")
		return self._data[self._front]

	def last(self):
		"""Return (but do not remove) the last element of the deck.
		Raise empty exception if deck is empty"""
		if self.is_empty():
			raise Empty("Deque is empty")
		last = (self._front + self._size - 1) % len(self._data) #Index of last element
		return self._data[last]

	def _resize(self, cap):
		"""Resize underlying array to a new capacity cap"""
		old = self._data #temporarily backup old data
		self._data = [None] * cap #Reassign _data to new array of size cap
		walk = self._front
		for k in range(self._size):
			self._data[k] = old[walk] 
			walk = (walk + 1) % len(old) #Use old length as modulus to reconstruct order
		self._front = 0 #realign front
	
	def add_first(self, e):
		"""Add element e to the front of the deck"""
		self._front = (self._front - 1) % len(self._data) #Recompute first tracker
		self._data[self._front] = e #assign element
		self._size += 1 #Increse queue size

	def add_last(self, e):
		"""Add element e to the back of the deck (similar to enqueue method for simple queues)"""
		if len(self) == len(self._data): #If array is full...
			self._resize(2 * len(self._data)) #Resize it to double capacity
		back =  (self._front + self._size) % len(self._data) #new index of back of deque
		self._data[back] = e #Add new element
		self._size +=1 #Increase size
	
	def delete_first(self):
		"""Remove and return first element of the deck (similar to dequeue method for simple queues).
		Raise Empty if queue is empty"""
		if self.is_empty():
			raise Empty("Deque is empty")
		value = self._data[self._front] #Store value to return
		self._data[self._front] = None #Enhance garbage collection
		self._front = (self._front + 1) % len(self._data) #Step forward 
		self._size -= 1 #Decrease deck size
		if 0 < len(self) < len(self._data) // 4:
			self._resize(len(self._data) // 4) #Perform array shrinkage if necessary
		return value

	def delete_last(self):
		"""Remove and return last element of the deck.
		Raise Empty if deck is empty."""
		if self.is_empty():
			raise Empty("Deque is empty")
		last = (self._front + self._size - 1) % len(self._data) #Index of last element in queue
		value = self._data[last] #Store value to return
		self._data[last] = None #Improve garbage collection
		self._size -= 1 #Decrease deck size
		if 0 < len(self) < len(self._data) // 4:
			self._resize(len(self._data) // 4) #Perform array shrinkage if necessary	
		return value


#------------------------------------Unit Tests----------------------------------			
if __name__ == "__main__":
	deck = ArrayDeque()
	for i in range(25):
		if i % 2 == 0:
			deck.add_last(i)
		else:
			deck.add_first(i)
	for j in range(15):
		if j % 2 ==0:
			print(deck.delete_first())
		else:
			print(deck.delete_last())
	print(len(deck))