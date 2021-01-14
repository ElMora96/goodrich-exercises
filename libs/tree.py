class Tree:
	"""Abstract Base Class to represent trees"""
	#------------------Nested Position Class----------------------------
	class Position:
		"""Abstraction representing location of single Node (Wrapper)"""
		def element(self):
			"""Return element stored at this position"""
			raise NotImplementedError("must be implemented by subclass")

		def __eq__(self, other):
			"""Return True if other Position represents same location"""
			raise NotImplementedError("must be implemented by subclass")

		def  __ne__(self, other):
			"""Return True if other represents a different location"""
			return not self == other 

	#---------Abstract Methods that concrete subclass must support------
	def root(self):
		"""Return Position representing tree's root (or None if it is Empty)"""
		raise NotImplementedError("must be implemented by subclass")

	def parent(self, p):
		"""Return position representing p's parent"""
		raise NotImplementedError("must be implemented by subclass")

	def children(self, p):
		"""Generate an iteration of Positions representing p's Children"""
		raise NotImplementedError("must be implemented by subclass")

	def num_children(self, p):
		"""Return number of children of Position p"""
		raise NotImplementedError("must be implemented by subclass")

	def __len__(self):
		"""Return total number of nodes in the tree"""
		raise NotImplementedError("must be implemented by subclass")

	#--------Concrete Methods implemented in this Class-----------------
	def is_root(self, p):
		"""Return True if Position p represents root node of the tree"""
		return p == self.root()

	def is_leaf(self, p):
		"""Return True if Positon p represents a leaf node of the tree (no children)"""
		return self.num_children(p) == 0

	def is_empty(self):
		"""Return True if tree does not contain any node"""
		return len(self) == 0

		#Notice __iter__ depends on concrete implementation
	
	def depth(self, p):
		"""Returns depth of node at Position p"""
		if self.is_root(p):
			return 0
		else:
			return 1 + self.depth(self.parent(p)) #Recursively compute number of ancestors

	#nonpublic method to compute height of subtree
	def _heigth(self, p):
		"""Return the height of the subtree rooted at Position p (Height of position p)"""
		if self.is_leaf(p):
			return 0
		else:
			return 1 + max(self._heigth(q) for q in self.children(p)) #time is linear in size of subtree
	
	#Wrap with a public method
	def height(self, p = None):
		"""Return the height of the subtree rooted at Position p.
		If p is None, return the height of the entire tree.
		"""
		if p is None:
			p = self.root()
		return self._heigth(p)

class BinaryTree(Tree):
	"""Abstract Base Class Representing a binary tree structure"""
	#------------------Additional Abstract Methods------------------
	def left(self, p):
		"""Return a position representing p's left child (or None)"""
		raise NotImplementedError("must be implemented by subclass")

	def right(self, p):
		"""Return a position representing p's right child (or None)"""
		raise NotImplementedError("must be implemented by subclass")

	def sibling(self, p):
		"""Return the other child of p's parent (or None)"""
		if self.is_root(p): #Check if p is root
			return None
		else:
			parent = self.parent(p) #Parent's position
			if p == self.left(parent):
				return self.right(parent)
			else:
				return self.left(parent)

	def children(self, p):
		"""Generate an iteration over p's children"""
		if self.left(p) is not None:
			yield self.left(p)
		if self.right(p) is not None:
			yield self.right(p)