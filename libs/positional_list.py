#Linked Positional List Data Structure.

class _DoublyLinkedBase:
	"""Abstract base class with doubly linked list representation"""

	class _Node:
		"""Nested, lightweight doubly linked node class"""
		__slots__ = '_element', '_prev', '_next' #Memory-efficient
		def __init__(self, element, prev, next):
			self._element = element
			self._prev = prev 
			self._next = next

	def __init__(self):
		"""Create an empty list"""
		self._header = self._Node(None, None, None) #dummy header (stores no element)
		self._trailer = self._Node(None, None, None) #dummy trailer (stores no element)
		self._header._next = self._trailer
		self._trailer._prev = self._header 
		self._size = 0

	def __len__(self):
		"""Return number of elements in list"""
		return self._size

	def is_empty(self):
		"""Returns True if list is empty"""
		return self._size == 0

	def _insert_between(self, element, predecessor, successor):
		"""Insert element between predecessor and successor; return new node"""
		new = self._Node(element, predecessor, successor) #Create new node
		predecessor._next = new #new is after predecessor
		successor._prev = new #new is before successor
		self._size += 1 #increase list size
		return new

	def  _delete_node(self, node):
		"""Delete nonsentinel node from list; return its element"""
		predecessor = node._prev
		successor = node._next
		predecessor._next = successor  #Skip node with new links
		successor._prev = predecessor
		self._size -= 1 #Decrease list sie
		element = node._element #Record deleted element
		node._next = node._prev = node._element = None  #deprecate node
		return element 

class PositionalList(_DoublyLinkedBase):
	"""Sequential container of elements allowing positional access"""

	class Position():
		"""Nested class: abstraction representing position of single node"""

		def __init__(self, container, node):
			"""Constructor shouldn't be invoked by user"""
			self._container = container #Positional list to which position belongs
			self._node = node

		def element(self):
			"""Return element stored at this Position"""
			return self._node._element

		def __eq__(self, other):
			"""Return True if other is a Position representing the same location"""
			return type(other) is type(self) and self._node == other._node #short-circuits

		def  __ne__(self, other):
			"""Return True if other represents a different location"""
			return not self == other 

	def _validate(self, p):
		"""Utility method. Return Node at Position p, or raise appropriate Error if invalid"""
		if not isinstance(p, self.Position):
			raise TypeError("p must be a Position type")
		if p._container is not self:
			raise  ValueError("p does not belong to this PositionalList")
		if p._node._next == p._node._prev == None: #Recall _delete_node in base class sets _prev and _next to None 
			raise ValueError("This position is no longer valid")
		return p._node

	def _make_position(self, node):
		"""Utility method. Return Position instance for given node, or None if node is dummy"""
		if node is self._header or node is self._trailer:
			return None
		else:
			return self.Position(self, node)

	#Mutator. Override inherited version to return Position, rather than Node
	def _insert_between(self, element, predecessor, successor):
		"""Add element between existing nodes and return new position"""
		node = super()._insert_between(element, predecessor, successor)
		return self._make_position(node)

	#Public methods: Accessors ---------------------------------------------------------------
	def first(self):
		"""Return first Position of PositionalList (or None if PositionalList is empty)"""
		return self._make_position(self._header._next)

	def last(self):
		"""Return the last Position in PositionalList (or None if PositionalList is empty)"""
		return self._make_position(self._trailer._prev)

	def before(self, p):
		"""Return Position before given position p (or None if p is the first Position)"""
		node = self._validate(p) #validate position p
		return self._make_position(node._prev)

	def  after(self, p):
		"""Return Position after given position p (or None if p is the last Position)"""		
		node = self._validate(p)
		return self._make_position(node._next)

	def __iter__(self):
		"""Generate a forward iteration of the elements of the list"""
		cursor = self.first() #First Position in the list
		while cursor is not None:
			yield cursor.element() 
			cursor = self.after(cursor)

	#Public methods: Mutators ----------------------------------------------------------------
	def add_first(self, element):
		"""Insert element at the front of the list and return new Position"""
		return self._insert_between(element, self._header, self._header._next)

	def add_last(self, element):
		"""Insert element at the back of the list and return new Position"""
		return self._insert_between(element, self._trailer._prev, self._trailer)

	def add_before(self, element, p):
		"""Insert element before position p and return new Position"""
		original = self._validate(p) #Validate position and retrieve corresponding node
		return self._insert_between(element, original._prev, original)

	def add_after(self, element, p):
		"""Insert element after position p and return new Position"""
		original = self._validate(p) #Validate position and retrieve corresponding node
		return self._insert_between(element, original, original._next)

	def delete(self, p):
		"""Delete and return element at position p"""
		original = self._validate(p) #Validate position and retrieve corresponding node
		return self._delete_node(original) #inherited method returns element

	def replace(self, p, element):
		"""Replace element at position P with given element. Return element previously at position p"""
		original = self._validate(p)
		old_value = original._element #temporary
		original._element = element
		return old_value