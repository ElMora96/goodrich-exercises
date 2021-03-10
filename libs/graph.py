class Graph:
	"""Simple Graph implemented using an adjacency map"""

	#-----------------------------Nested Vertex Class---------------------------
	class Vertex:
		"""Lightweight vertex structure for a Graph"""
		__slots__ = '_element' #Streamline memory usage
		
		def __init__(self, x):
			"""Do not use this constructor. Instead use Graph.insert_vertex(x)"""
			self._element = x

		def element(self):
			"""Return element associated with this vertex"""
			return self._element

		def __hash__(self):
			return hash(id(self)) #Enables using Vertex as Map Key

		#-----------------------------Nested Edge Class---------------------------
	class Edge:
		"""LightWeight edge structure for a Graph"""
		__slots__ = '_element', '_origin', '_destination'

		def __init__(self, u, v, x):
			"""Do not use this constructor. Instead use Graph.insert_edge(u,v,x)"""
			self._origin = u
			self._destination = v
			self._element = x

		def endpoints(self):
			"""Return tuple (u,v) for vertices u and v"""
			return (self._origin, self._destination)

		def element(self):
			"""Return element associated with this edge"""
			return self._element

		def opposite(self, v):
			"""Return vertex opposite to v in this edge"""
			return self._destination if v is self._origin else self._origin

		def __hash__(self):
			return hash((self._origin, self._destination)) #will allow edge to be a map key

	#--------------------Main Graph Methods------------------------------------		
	def __init__(self, directed = False):
		"""Create an empty graph (undirected by default)."""
		self._outgoing = {}
		#Only create second map for directed, else use alias
		self._incoming = {} if directed else self._outgoing

	def is_directed(self):
		"""Return True if graph is directed.
		Property is based on the original declaration of the graph, 
		not its contents."""
		return self._outgoing is not self._incoming

	def vertex_count(self):
		"""Return number of vertices in the graph"""
		return len(self._outgoing)

	def vertices(self):
		"""Return an iteration of vertices in the graph"""
		return self._outgoing.keys()

	def edge_count(self):
		"""Return the number of edges in the graph"""
		total = sum(len(self._outgoing[v]) for v in self._outgoing)
		# for undirected graphs, make sure not to double-count edges
		return total if self.is_directed() else total // 2

	def edges(self):
		"""Return the set with all edges of the graph"""
		result = set()
		for secondary_map in self._outgoing.values():
			result.update(secondary_map.values())
		return result

	def get_edge(self, u, v):
		"""Return the edge from u to v, or None if not adjacent."""
		return self._outgoing[u].get(v)

	def degree(self, v, outgoing = True):
		"""Return number of (outgoing) edges incident to vertex v in the graph.
		If graph is directed, optional parameter used to count incoming edges"""
		adj = self._outgoing[v] if outgoing else self._incoming[v]
		return len(adj)

	def incident_edges(self, v, outgoing = True):
		"""Iterate over (outgoing) edges incident to vertex v in the graph.
		If graph is directed, optional parameter used to request incoming edges."""
		adj = self._outgoing[v] if outgoing else self._incoming[v]
		for edge in adj.values():
			yield edge

	def insert_vertex(self, x = None):
		"""Insert and return new vertex with element x"""
		v = self.Vertex(x) #instantiate new vertex
		self._outgoing[v] = {}
		if self.is_directed():
			self._incoming[v] = {} #need distinct map for incoming edges
		return v

	def insert_edge(self, u, v, x = None):
		"""Insert and return a new Edge from u to v with auxiliary element x"""
		e = self.Edge(u, v, x)
		self._outgoing[u][v] = e
		self._incoming[v][u] = e
		return e


def DFS(g, u, discovered):
	"""
	Perform Depth-First Search over graph g starting at vertex u.
	discovered is a dictionary mapping each vertex to the edge that was used to
	discover it during the DFS. (u should be ”discovered” prior to the call.)
	Newly discovered vertices will be added to the dictionary as a result.
	Can be run as:
	result = {u: None}
	DFS(g, u, result)
	"""
	
	for e in g.incident_edges(u):
		v = e.opposite(u) #Opposite vertex
		if v not in discovered:
			discovered[v] = e
			DFS(g, v, discovered)


def construct_path(u, v, discovered):
	"""Reconstruct the (directed) path from u to v,+
	examining the discovery dictionary produced by DFS"""
	path =  [] #default empty path
	if v in discovered:
			#Build list from v to u; then reverse it
			path.append(v)
			trav = v #temporary variable
			while trav is not u:
				e = discovered[trav]
				parent = e.opposite(v)
				path.append(parent)
				trav = parent
			path.reverse() #reverse path
	return path

def DFS_complete(g):
	"""Perform DFS for entire graph g and return forest as a dictionary.
	Result maps each vertex v to the edge that was used to discover it;
	vertices that are roots of a DFS tree are mapped to None."""
	forest = {}
	for u in g.vertices():
		if u not in forest:
			forest[u] = None
			DFS(g, u, forest)
	return forest