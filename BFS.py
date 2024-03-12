#Nathaniel Bagchee 3/17/2023
from collections import deque
'''Initializing a vertex class to use for the breadth/depth first search'''
class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}
        self.color = 'white'

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def add(self, key):
        '''This method adds the vertex'''
        self.numVertices += 1
        new = Vertex(key)
        self.vertList[key] = new
        return new

    def getVertex(self, n):
        '''This function returns the found vertex'''
        if n in self.vertList: return self.vertList[n]
        else: return None

    def __contains__(self, v):
        return v in self.vertList.values()

    def addEdge(self, f, t, weight=0):
        '''Adds the edge to the graph'''
        if f not in self.vertList:
            self.add(f)
        if t not in self.vertList:
            self.add(t)
        self.vertList[f].addNeighbor(self.vertList[t], weight)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

    def breadth_first_search(self, s):
        '''Used to search through the queue'''
        for j in self:
            j.color = 'orange'
        q = deque()
        self.vertList[s].color = 'gray'
        q.append(self.vertList[s])
        p = []
        while q:
            u = q.popleft()
            p.append(u.id)
            #Unqueing them if been through
            for j in u.getConnections():
                if j.color == 'orange':
                    j.color = 'gray'
                    q.append(j)
            u.color = 'black'

        return p

    def depth_first_search(self):
        for c in self: c.color = 'white'
        listy = []
        # Recursive function for each vertex that has not been through
        for c in self:
            if c.color == 'white': self.DFS(c, listy)
        return listy

    def DFS(self, vid, path):
        #  Adds it to the path
        vid.color = 'blue'
        path.append(vid.id)
        # Recurison for vertices that haven't been visited
        for v in vid.getConnections():
            if v.color == 'white': self.DFS(v, path)
        vid.color = 'black'
'''Testing script'''
if __name__ == '__main__':

    g = Graph()
    for i in range(6):
        g.add

    g.addEdge(0,1)
    g.addEdge(0,5)
    g.addEdge(1,2)
    g.addEdge(2,3)
    g.addEdge(3,4)
    g.addEdge(3,5)
    g.addEdge(4,0)
    g.addEdge(5,4)
    g.addEdge(5,2)

    for v in g:
        print(v)

    assert (g.getVertex(0) in g) == True
    assert (g.getVertex(6) in g) == False

    print(g.getVertex(0))
    assert str(g.getVertex(0)) == '0 connectedTo: [1, 5]'

    print(g.getVertex(5))
    assert str(g.getVertex(5)) == '5 connectedTo: [4, 2]'

    path = g.breadth_first_search(0)
    print('BFS traversal by discovery time (preordering): ', path)
    assert path == [0, 1, 5, 2, 4, 3]

    path = g.depth_first_search()
    print('DFS traversal by discovery time (preordering): ', path)
    assert path == [0, 1, 2, 3, 4, 5]
