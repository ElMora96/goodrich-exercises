class Tree:
	"""Abstract Base Class to represent trees"""
	#------------------Nested Position Class----------------------------
	class Position:
		"""Abstraction representing location of single Node (Wrapper).
		Notice here __init__ is missing. 
		"""

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

	def __iter__(self):
		"""Generate an iteration of the tree's elements"""
		for p in self.positions(): #Use same order as positions
			yield p.element() #But yield element

	def height(self, p = None):
		"""Return the height of the subtree rooted at Position p.
		If p is None, return the height of the entire tree.
		"""
		if p is None:
			p = self.root()
		return self._heigth(p)

	def preorder(self):
		"""Generate a preorder iteration of positions in the tree"""
		if not self.is_empty():
			for p in self._subtree_preorder(self.root()):
				yield p 			

	def postorder(self):
		"""Generate a postorder iteration of positions in the tree"""
		if not self.is_empty():
			for p in self._subtree_postorder(self.root()):
				yield p

	def breadthfirst(self):
		"""Generate a breadth-first iteration of positions	in 	the	tree.
		Relies on LinkedQueue Class."""
		if not self.is_empty():
			fringe = LinkedQueue() #Queue to store known positions not yet yielded
			fringe.enqueue(self.root()) 
			while not fringe.is_empty():
				p = fringe.dequeue() #pick element
				yield p #Yield it
				for c in self.children(p): #for each child c
					fringe.enqueue(c)

	def positions(self):
	"""Generate an iteration of the tree's positions - Preorder Traversal default"""
		return self.preorder() #Directly return generator

#---------------Nonpublic Methods------------------------------------------------------
	def _heigth(self, p):
		"""Return the height of the subtree rooted at Position p (Height of position p)"""
		if self.is_leaf(p):
			return 0
		else:
			return 1 + max(self._heigth(q) for q in self.children(p)) #time is linear in size of subtree
	
	def _subtree_preorder(self, p):
		"""Generate a preorder iteration of positions in the subtree rooted at p"""
		yield  p #Visit p before its subtrees
		for c in self.children(p): #for each child c
			for other in self._subtree_preorder(c): #do preorder of c's subtree
				yield other #yielding each to our caller (re-yield position yielded by internal _subtree_preorder)

	def _subtree_postorder(self, p):
		"""Generate a postorder iteration of positions in the subtree rooted at p"""
		for c in self.children(p): #for each child c
			for other in self._subtree_postorder(c): #do postorder of subtree rooted at c
					yield other		#yielding each position	to our caller	
		yield p #Visit p after its subtree


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


class LinkedBinaryTree(BinaryTree):
	"""Linked representation of a binary tree structure (concrete)"""
	class _Node:
		"""Lightweight, nonpublic class for representing a Node"""
		def __init__(self, element, parent = None, left = None, right = None):
			self._element = element
			self._parent = parent
			self._left = left
			self._right = right

	class Position(BinaryTree.Position):
		"""Abstraction to represent location of single element; inherits from nested class"""
		def __init__(self, container, node):
			"""Constructor should not be invoked by user"""
			self._container = container
			self._node = node

		def element(self):
			"""Return element stored at this Position"""
			return self._node._element

		def __eq__(self, other):
			"""Returns True if self and other represent same Position in Tree"""
			return type(other) == type(self) and self._node == other._node #Short-circuits

		def  __ne__(self, other):
			"""Returns True if self and other represent different Positions"""
			return not self == other

	def _validate(self, p):
		"""Robust utility method to check validity of position. 
		Return Node at Position p, or raise appropriate Error if Position is invalid"""
		if not isinstance(p, self.Position):
			raise TypeError("p must be a Position instance")
		if p._container is not self:
			raise  ValueError("p does not belong to this Tree")
		if p._node._parent is p._node: #Convention for deprecated nodes
			raise ValueError("This position is no longer valid")
		return p._node	

	def _make_position(self, node):
		"""Return Position instance corresponding to given node (or None if node is None)"""
		return self.Position(self, node) if node is not None else None

	#--------------BinaryTree Constructor---------------------------------------
	def __init__(self):
		"""Return an empty binary tree"""
		self._root = None #Instance variable storing refence to root node
		self._size = 0

	#------------------------Public Accessors-----------------------------------
	def __len__(self):
		"""Return total number of nodes in tree"""
		return self._size

	def root(self):
		"""Return Position representing tree's root (or None if it is Empty)"""
		return self._make_position(self._root)

	def parent(self, p):
		"""Return Position representing p's parent"""
		node = self._validate(p)
		return self._make_position(self, node._parent)

	def left(self, p):
		"""Return a Position representing p's left child (or None)"""
		node = self._validate(p)
		return self._make_position(self, node._left)

	def right(self, p):
		"""Return a Position representing p's right child (or None)"""
		node = self._validate(p)
		return self._make_position(self, node._right)

	def num_children(self, p):
		"""Return number of children of Position p"""
		node = self._validate(p)	
		count = 0
		if node._left is not  None: #Left child exists
			count += 1
		if node._right is not None: #Right child exists
			count += 1
		return count

#-------------------Nonpublic Mutators----------------------------------
	def _add_root(self, e):
		"""Place element at the root of the tree.
		Raise ValueError if tree is nonempty."""
		if self._root is not None:
			raise ValueError("Root already exists")
		else:
			self._size += 1 #Update tree size
			self._root = self._Node(e)
			return self._make_position(self._root)

	def _add_left(self, p, e):
		"""Create left child for node P, storing element e.
		Return new position. Raise ValueError if p is invalid
		or if p alreadt has left child.
		"""
		node = self._validate(p) #Raises ValueError if p is invalid
		if node._left is not  None:
			raise ValueError("This node already has a left child")
		else:
			node._left = self._Node(e, node) #node is its parent
			return self._make_position(node._left)

	def _add_right(self, p, e):
		"""Create right child for node P, storing element e.
		Return new position. Raise ValueError if p is invalid
		or if p alreadt has left child.
		"""
		node = self._validate(p) #Raises ValueError if p is invalid
		if node._right is not  None:
			raise ValueError("This node already has a right child")
		else:
			node._right = self._Node(e, node) #node is its parent
			return self._make_position(node._right)

	def _replace(self, p, e):
		"""Replace element at position p with e, and return old element"""
		node = self._validate(p)
		old = node._element
		node._element = e
		return old

	def _delete(self, p):
		"""Delete node at position p and Replace it with its child, if any.
		Return the element that had been stored at Position p.
		Raise ValueError if node at position p has two children.
		Raise ValueError if position p is invalid."""
		node = self._validate(p)
		if self.num_children(p) == 2:
			raise  ValueError("Node at this position has two children")
		child = node._left if node._left else node._right #Might be None
		if self._root is node:
			self._root = child #Child becomes new root
			child._parent = None 
		else:
			parent = node._parent
			if node is parent._left:
				parent._left = child
			else:
				parent._right = child
		self.size -= 1 #Decrease tree size
		node._parent = node #Deprecate old node; convention
		return node._element

	def _attach(self, p, T_1, T_2):
		"""Attach trees T_1 and T_2 to leaf p as left and right subtrees, respectively"""
		node = self._validate(p)
		if not self.is_leaf(p):
			raise ValueError("p must be a leaf node")
		if not type(self) is type(T_1) is type(T_2): #Check you're indeed passing trees
			raise  TypeError("Tree types must match")
		self._size += len(T_1) + len(T_2) #Increase size (Notice use of public methods for external trees)
		if not T_1.is_empty(): #Attach T_1 as left subtree
			T_1._root._parent = node
			node._left = T_1._root
			T_1.root = None #Deprecate tree
			T_1.size = 0 #Deprecate tree
		if not T_2.is_empty(): #Attach T_2 as right subtree
			T_2._root._parent = node
			node._right = T_2._root
			T_2._root = None #Deprecate tree
			T_2._size = 0 #Deprecate tree


