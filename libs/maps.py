from collections.abc import MutableMapping
from random import randrange

class MapBase(MutableMapping):
	"""My own ABC which contains a nonpublic nested _Item class"""
	class _Item:
		"""Lightweight composite to store key-value pairs as map items"""
		__slots__ = '_key', '_value' #Optimize memory usage

		def __init__(self, k, v):
			self._key = k
			self._value = v

		def __eq__(self, other):
			return self._key == other._key #Compare items based on their keys

		def __ne__(self, other):
			return not self == other #Opposite

		def __lt__(self, other):
			return self._key < other._key

class UnsortedTableMap(MapBase):
	"""(Naive) Map implementation using unsorted list.
	All core methods run in O(n) time."""
	def __init__(self):
		"""Create empty map"""
		self._table = [] 

	def __len__(self):
		"""Return number of stored entries"""
		return len(self._table)

	def __iter__(self):
		"""Iterator over items stored in table"""
		for item in self._table:
			yield item._key #Yield KEY of the element

	def __getitem__(self, k):
		"""Return value associated with key k (raise KeyError if not found)"""	
		for item in self._table:
			if item._key == k:
				return item._value
		raise KeyError('Key Error ' + repr(k)) #Iteration finished but item not found

	def __delitem__(self, k):
		"""Delete item associated with key k (raise KeyError if not found)"""
		for j in range(len(self._table)):
			if k == self._table[j]._key:
				self._table.pop(j) #Remove item
				return #Exit
		raise KeyError('Key Error ' + repr(k)) #Iteration finished but item not found

	def __setitem__(self, k, v):
		"""Assign value v to key k, overwriting existing value if present."""
		for item in self._table:
			if item._key == k: #match found
				item._value = v #assign new value
		#If no match found
		self._table.append(self._Item(k, v))

class HashMapBase(MapBase):
	"""Abstract base class for hash-based maps using MAD compression.
	Relies on concrete _bucket_getitem, _buckt_setitem and _bucket_delitem"""
	def __init__(self, cap = 11, p = 109345121):
		"""Create an empty hash-table map.
		Parameters.
		cap: int. Initial capacity of the bucket array
		p: int. Prime number used in MAD.
		"""
		self._table = cap * [None] #Initialize empty table
		self._prime = p
		self._n = 0 #Number of stored entries
		self._scale = 1 + randrange(p - 1) #scale from 1 to p-1 for MAD
		self._shift = randrange(p) #shift from 0 to p-1 for MAD

	def __len__(self):
		"""Return number of stored entries"""
		return self._n

	def __getitem__(self, k):
		j = self._hash_function(k)
		return self._bucket_getitem(j, k)

	def __delitem__(self, k):
		"""Remove but do not return element stored at key k"""
		j = self._hash_function(k)
		self._bucket_delitem(j, k) #Delete item - might raise KeyError
		self._n -= 1 #Decrease size

	def __setitem__(self, k, v):
		j = self._hash_function(k)
		self._bucket_setitem(j, k, v) #Store new item - subroutine mantains self._n
		if self._n > len(self._table) // 2: #Keep load factor <2
			self._resize(2 * len(self._table) - 1) 


	def _hash_function(self, k):
		"""Nonpublic hash wrapper"""
		return (hash(k)*self._scale + self._shift) % self._prime % len(self._table) #Notice len(self._table) == N with theory notation

	def _resize(self, c):
		"""Resize table (array) to capacity c"""
		old = list(self.items()) #Use iterations to store old values
		self._table = c * [None] #Create new table
		self._n = 0 #Reinitialize length value
		for (k, v) in old:
			self[k] = v #Reload items

class ChainHashMap(HashMapBase):
	"""Concrete implementation of Hash Table with Separate Chaining for collision resolution.
	Buckets are in turn Table Maps (unsorted)"""
	def __iter__(self):
		for bucket in self._table: #Iterate over table
			if bucket is not  None: #Nonempty slot in array
				for key in bucket: #Iterate over bucket
					yield key

	def _bucket_getitem(self, j, k):
		bucket = self._table[j]
		if bucket is None:
			raise KeyError('Key Error ' + repr(k)) #No match found
		return bucket[k] #Might raise KeyError

	def _bucket_delitem(self, j, k):
		bucket = self._table[j]
		if bucket is None:
			raise KeyError('Key Error ' + repr(k)) #No match found
		del bucket[k] #Might raise KeyError
	
	def _bucket_setitem(self, j, k, v):
		if self._table[j] is None:
			self._table[j] = UnsortedTableMap() #Create new bucket at required position
		oldsize = len(self._table[j]) #Old bucket size (might be zero if bucket is newly created)
		self._table[j][k] = v #Store new item
		if len(self._table[j]) > oldsize: #If key is new...
			self._n += 1 #Increase map size

class ProbeHashMap(HashMapBase):
	"""Concrete implementation of Hash Table using Open Addressing 
	with Linear Probing for collision resolution"""

	_AVAIL = object() #sentinel object to mark locations of deleted objects

	def _is_available(self, j):
		"""Return True if index j is available in table"""
		return self._table[j] is None or self._table[j] is ProbeHashMap._AVAIL

	def _find_slot(self, j, k):
		"""Search for key k in bucket j.
		Return (success, index) tuple, described as follows:
		If match was found, success is True and index denotes its location.
		If no match found, success is False and index denotes first available slot."""
		first_avail = None
		while True:
			if self._is_available(j):
				if first_avail is None:
					first_avail = j
				if self._table[j] is None:
					return (False, first_avail)
			elif k == self._table[j]._key:
				return (True, j)
			j = (j + 1) % len(self._table) #Keep looking cyclically

	def _bucket_getitem(self, j, k):
		found, s = self._find_slot(j, k)
		if not found:
			raise KeyError('Key Error ' + repr(k))
		return self._table[s]._value

	def _bucket_delitem(self, j, k):
		found, s = self._find_slot(j, k)
		if not found:
			raise KeyError('Key Error ' + repr(k))
		self._table[s] = ProbeHashMap._AVAIL #Mark as available

	def _bucket_setitem(self, j, k, v):
		found, s = self._find_slot(j, k)
		if not found:
			self._table[s] = self._Item(k, v) #new item
			self._n += 1 #Increase size
		else:
			self._table[s]._value = v #overwrite existing item

	def __iter__(self):
		for j in range(len(self._table)):
			if not self._is_available(j):
				yield self._table[j]._key


class  SortedTableMap(MapBase):
	"""Map implementation via sorted table"""

	#---------------------------------Nonpublic Methods---------------------------------
	def _find_index(self, k, low, high):
		"""Return index of the leftmost item with key greater than or equal to k.
			Return high + 1 if no such item qualifies.

			That is, j will be returned such that:
			all items of slice table[low:j] have key < k
			all items of slice table[j:high+1] have key >= k
		"""
		if high < low:
			return high + 1 #No element qualifies
		else:
			mid = (low + high) // 2
			if k == self._table[mid]._key:
				return mid
			elif k < self._table[mid]._key:
				return self._find_index(k, low, mid - 1) #notice might return mid
			else:
				return self._find_index(k, mid + 1, high)


	#----------------------------------Public Methods-----------------------------------
	def __init__(self):
		"""Create empty table"""
		self._table = []

	def __len__(self):
		"""Return number of stored entries"""
		return len(self._table)

	def __getitem__(self, k):
		"""Return value associated with key k.
		Raise KeyError if not found"""
		j = self._find_index(k, 0, len(self) - 1)
		if j == len(self) or self._table[j]._key != j:
			raise KeyError('Key Error ' + repr(k))
		return self._table[j]._value

	def __setitem__(self, k, v):
		"""Assign value v to key k; overwriting if k is already present in map"""
		j = self._find_index(k, 0, len(self) - 1) 
		if j < len(self) and self._table[j]._key == k:
			self._table[j]._value = v #Overwrite
		else:
			self._table.insert(j, self._Item(k, v)) #Add new element

	def __delitem__(self, k):
		"""Delete item associated with key k.
		Raise KeyError if not found."""
		j = self._find_index(k, 0, len(self) - 1)
		if j == len(self) or self._table[j]._key != j:
			raise KeyError('Key Error ' + repr(k))
		self._table.pop(j) #Remove Item

	def __iter__(self):
		"""Iterate over keys stored in table (min to max)"""
		for item in self._table:
			yield item._key

	def __reversed__(self):
		"""Iterate over keys stored in table (max to min)"""
		for item in reversed(self._table):
			yield item._key

	def find_min(self):
		"""Return (key, value) tuple with minimun key (or None if empty)"""
		if len(self) > 0:
			return (self._table[0]._key, self._table[0]._value)
		else:
			return None
			
	def find_max(self):
		"""Return (key, value) tuple with maximun key (or None if empty)"""
		if len(self) > 0:
			return (self._table[-1]._key, self._table[-1]._value)
		else:
			return None
			
	def find_ge(self, k):
		"""Return (key, value) tuple with least key greater or equal than k"""
		j = self._find_index(k, 0, len(self) - 1) #key[j] >= k
		if j < len(self):
			return (self._table[j]._key, self._table[j]._value) 
		else:
			return None

	def find_gt(self, k):
		"""Return (key, value) tuple with least key strictly greater than k"""
		j = self._find_index(k, 0, len(self) - 1) #key[j] >= k
		if j < len(self) and self._table[j]._key == k:
			j += 1 #Advanced past match
		if j < len(self):
			return (self._table[j]._key, self._table[j]._value)
		else:
			return None

	def find_lt(self, k):
		"""Return (key, value) tuple with max key strictly smaller than k"""
		j = self._find_index(k, 0, len(self) - 1) #key[j] >= k
		if j > 0:
			return (self._table[j - 1]._key, self._table[j - 1]._value) 
		else:
			return None	

	def find_range(self, start, stop):
		"""Iterate all keys such that start <= key <= stop.
		If start is None, begin from mininum key of map.
		If stop is None, iterate until greatest key."""
		if start is None:
			j = 0
		else:
			j = self._find_index(start, 0, len(self) - 1)
		while j < len(self) and (stop is None or self._table[j]._key < stop):
			yield (self._table[j]._key, self._table[j]._value)
			j += 1


###à######################## UNIT TEST ######################################
if __name__ == "__main__":
	test = SortedTableMap()
	test[23] = 45
	test[1] = 22
	test[47] = 12
	#del test["a"]
	print(list(test.find_range(1, 25)))