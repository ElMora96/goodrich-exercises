"""Write a simple text editor that stores and displays a string of characters
using the positional list ADT, together with a cursor object that highlights
a position in this string. A simple interface is to print the string and then
to use a second line of output to underline the position of the cursor. Your
editor should support the following operations:
• left: Move cursor left one character (do nothing if at beginning).
• right: Move cursor right one character (do nothing if at end).
• insert c: Insert the character c just after the cursor.
• delete: Delete the character just after the cursor (do nothing at end)."""
###############LIBRARIES###########################
from copy import  deepcopy
from os import  system
###############BASE DATA STRUCTURES ###############
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
		"""Utility method. Return Node at Position p, or raise appropiate Error if invalid"""
		if not isinstance(p, self.Position):
			raise TypeError("p must be a Position instance")
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

###############EDITOR###############
class StringPositionalList(PositionalList):
	"""Subclass of PositionalList to represent strings for SimpleEditor"""
	def __init__(self, input_string = None):
		"""Extend to read given input string"""
		super().__init__()
		if input_string:
			if not isinstance(input_string, str): #Check if given input is a string
				raise TypeError("Input must be a string")
			else:
				self._initialize_string(input_string)

	def __str__(self):
		"""String representation"""
		string = '' #Empty string
		for element in self:
			string += str(element)
		return string

	def  _initialize_string(self, string):
		"""Load Initial String"""
		pos = self.add_first(string[0]) #Initialize position pointer e set first element
		for char in string[1:]: #Iterate over other chars
			pos = self.add_after(char, pos) #Add char and update position



class SimpleEditor():
	"""PositionalList-based minimal text editor"""
	class _Interface:
		"""Simple CLI""" 
		def __init__(self, editor):
			"""container is the outer editor object"""
			self._container = editor
			self._string = editor.string
			self._prompt = '>>>' #Prompt to insert commands
			self._position = self._string.last() #Initialize position
			self._cursor = self._container._Cursor(self._container, self._position) #Build initial cursor
			while(True): #Program loop
				self._refresh()
		
		def _refresh(self):
			"""Refresh ClI at each update"""
			system("cls") #Clear screen
			print("""Mora's SimpleEditor. Supported Commands: 'left', 'right', 'delete', insertion of a char. """)
			print(self._string)
			print(self._cursor)
			print(self._prompt, end ='')
			self._read_input()			
			

		def _read_input(self):
			"""Read CLI input and perform corresponding update actions"""
			cli_input = input()
			if cli_input == 'left':
				if self._position != self._string.first():
					self._position = self._string.before(self._position) #Move cursor left; do nothing if beginning
			elif cli_input == 'right':
				if self._position != self._string.last():
					self._position = self._string.after(self._position) #Move cursor right
			elif isinstance(cli_input, str) and  len(cli_input) == 1: #Short-circuits
				self._position = self._string.add_after(cli_input, self._position)#Insert the character just after the cursor
			elif cli_input == 'delete':
				if self._position != self._string.last():
					self._string.delete(self._string.after(self._position)) #Delete the character just after the cursor
			else:
				print("Invalid Input, try again.")
			self._cursor = self._container._Cursor(self._container, self._position) #Refresh cursor

	class _Cursor:
		"""Cursor object that highlights current position"""
		def __init__(self, editor, p):
			"""editor is the outer object, p is the PositionalList position"""
			self._original_string = editor.string
			self._position = p

		def __str__(self):
			"""String represenation"""
			string = '' #Empty string
			pos = self._original_string.first() #Initialize position
			for char in self._original_string: #Iterate over list
				if pos == self._position: 
					string += '_' #If position is current; place a cursor
				else:
					string += ' ' #Else place an empty char
				pos = self._original_string.after(pos)
			return string

	def __init__(self, input_string = None):
		"""Text Editor"""
		self.string = StringPositionalList(input_string)
		self._CLI = self._Interface(self)
		 

###############UNIT TEST###############
if __name__ == "__main__":
	value = "Follow the White Rabbit"
	mora_edit = SimpleEditor(value)

