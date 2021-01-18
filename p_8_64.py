"""Implement the binary tree ADT using the array-based representation described in Section 8.3.2."""
from libs.tree import BinaryTree #Import previoulsy implemented binary tree ABC

class ArrayBinaryTree(BinaryTree):
	"""Array-based representation of a Binary Tree (concrete).
	No need to define internal node object"""

	class Position(BinaryTree.Position):
		"""Abstraction to represent position in tree w/ array-based representation"""
		def __init__(self, container, node):
			"""Constructor should no be invoked by user"""
			self._container = container #Pointer to wrapper tree object
			self._node = node
			#self._numbering = container._level_numbering(self) #Integer representing level numbering

		def element(self):
			"""Return element corresponding to this position"""
			return self._container._array[self._numbering]

		def __eq__(self, other):
			"""Return True if self and other represent same position in tree"""
			return type(self) == type(other) and self._numbering == other._numbering

		def  __ne__(self, other):
			"""Return True if self and other represent different positions"""
			return not self == other

	def _level_numbering(self, p):
		"""Function for the numbering of positions in the tree"""
		if self.is_root(p):
			return 0 #Return zero if root node
		pass
	def _validate(self, p):
		"""Utility to check validity of position"""
		raise NotImplementedError("Position Validation Utility not yet implemented")
	
	def _make_position(self, node):
		"""Return Position instance corresponding to given element"""

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
		"""Return position representing p's left child (or None)"""
		return 2 * self._level_numbering(p) + 1

	def right(self, p):
		"""Return position representing p's right child (or None)"""
		return 2* self._level_numbering(p) + 2

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

