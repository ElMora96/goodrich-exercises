"""Implement the binary tree ADT using the array-based representation described in Section 8.3.2."""
from libs.tree import BinaryTree #Import previoulsy implemented binary tree ABC
from numpy import floor

class ArrayBinaryTree(BinaryTree):
	"""Array-based representation of a Binary Tree (concrete).
	No need to define internal node object"""

	class Position(BinaryTree.Position):
		"""Abstraction to represent position in tree w/ array-based representation"""
		def __init__(self, container, node):
			"""Constructor should no be invoked by user"""
			self._container = container #Pointer to wrapper tree object
			self._numbering = container._level_numbering(self) #Integer representing level numbering

		def element(self):
			"""Return element corresponding to this position"""
			return self._container._array[self._numbering]

		def __eq__(self, other):
			"""Return True if self and other represent same position in tree"""
			return type(self) == type(other) and self._container == other._container and self._numbering == other._numbering

		def  __ne__(self, other):
			"""Return True if self and other represent different positions"""
			return not self == other

	def _make_position(self, numbering):
		"""Return position instance corrisponding to given numbering"""
		return self.Position(self, numbering)

	def _level_numbering(self, p):
		"""Function for the numbering of Positions p in the tree"""
		if self.is_root(p):
			return 0 #Return zero if root node
		else:
			current_numbering = p._numbering #This position num
			parent_numbering = floor((current_numbering - 1)/2)
			q = self._make_position(parent_numbering)
			if current_numbering % 2 == 1: #If left child
				return 2 * self._level_numbering(q) + 2 #Recursive call
			else: #If right child
				return 2 * self._level_numbering(q) + 2 #Recursive call

	def _validate(self, p):
		"""Utility to check validity of position"""
		raise  NotImplementedError("todo")
	
	#--------------BinaryTree Constructor---------------------------------------
	def __init__(self):
		"""Create an empty tree"""
		self._array = [] #Array to store elements of the tree
		self._size = 0 #Initialize tree size (number of nodes)

	#------------------------Public Accessors-----------------------------------
	def __len__(self):
		"""Return total number of nodes in tree"""
		return self._size

	def root(self):
		"""Return zero (root postition) or None if tree is Empty"""
		if self.is_empty():
			return None
		else:
			return 0

	def left(self, p):
		"""Return position representing p's left child"""
		return self._make_position(2 * p + 1)

	def right(self, p):
		"""Return position representing p's right child"""
		return self._make_position(2 * p + 2)

	def parent(self, p):
		"""Return position representing p's parent"""
		return self._make_position(floor((p - 1)/2))

	def num_children(self, p):
		"""Return number of children of Position p"""
		current = p._numbering
		count = 0
		if self._array[2*current + 1] is not None: #Left child exists
			count += 1
		if self._array[2*current + 2] is not None: #Right child exists
			count += 1
		return count

	#--------------------------Public Mutators----------------------------------
	def add_root(self, e):
		"""Place element at the root of the tree.
		Raise ValueError if tree is nonempty."""
		if not self.is_empty():
			raise ValueError("Root already exists")
		else:
			self._size += 1
			self._array.append(e) #Add element

	def add_left(self, p, e):
		"""Create left child for node p, storing element e.
		Raise ValueError if p already has left child"""
		child_numbering = left(p)
		if self._array[child_numbering] is not None:
			raise ValueError("This node already has a child")
		else:
			self._array[child_numbering] = e #assign element e to empty position

