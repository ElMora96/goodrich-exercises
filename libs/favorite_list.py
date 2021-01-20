#Favorite List: Data structure to maintain access frquencies
from libs.positional_list import PositionalList

class FavoriteList:
	"""List of elements ordered from most frequently accessed to least.
	Implementation performed applying the composition pattern.
	Uses PositionalList as underlying storage."""

	#-----------------------------Nested Item class-----------------------------------
	class _Item:
		"""Items of the underlying PositionalList"""
		__slots__ = '_value', '_count'	#Streamline memory usage

		def __init__(self, e):
			self._value = e #user's element
			self._count = 0 #access count initially zero

	#---------------------------------Nonpublic Utilities-----------------------------
	def _find_position(self, e):
		"""Search for an element e and return its position (or None if not found)"""
		trav = self._data.first() #First position in underlying PositionalList
		while trav and trav.element()._value != e:
			trav = self._data.after(trav)
		return trav #return position

	def _move_up(self, p):
		"""Move element at Position p earlier in the list, based on access count"""
		if p != self._data.first(): #Move only if element is not already at first pos
			cnt = p.element()._count
			trav = self._data.before(p) #Positihon before the given one
			if cnt > trav.element()._count:
				while trav != self._data.first() and cnt > self._data.before(trav).element()._count:
					trav = self._data.before(trav) #Move one step back towards the beginning
				self._data.add_before(self._data.delete(p), trav) #Delete/Reinsert

	#-----------------------------------Public Methods--------------------------------	
	def __init__(self):
		"""Create an empty Favorite List"""
		self._data = PositionalList() #Underlying storage
	
	def __len__(self):
		"""Return number of entries of the Favorite List"""
		return len(self._data) 

	def is_empty(self):
		"""Return True if Favorite List is empty"""
		return self._data.is_empty()

	def access(self, e):
		"""Access element e in list, thereby increasing its access count"""
		p = self._find_position(e)
		if p is None:
			self._data.add_last(self._Item(e)) #If new, add to the end of the list
		p.element()._count += 1 #increase access count
		self._move_up(p) #Run move-up routine
	
	def remove(self, e):
		"""Remove element e from the list of favorites"""
		p = self._find_position(e)
		if p is not None:
			self._data.delete(p) #delete if found

	def top(self, k):
		"""Generate an iteration of the top k elements in Favorite List"""
		if not 1 <= k <= len(self):
			raise ValueError("Illegal value for k")
		trav = self._data.first()
		for j in range(k):
			item = trav.element()
			yield item._value
			trav = self._data.after(trav)