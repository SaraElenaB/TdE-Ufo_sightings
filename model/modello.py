import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):

        self._grafo = nx.Graph()
        self.nodes = []
        self._idMapStates = {}

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllShapes(self):
        return DAO.getAllShapes()

    # ------------------------------------------------------------------------------------------------------------------------------------------
    def buildGraph(self, anno, shape):

        self._grafo.clear()
        self.nodes = DAO.getAllNodes()
        self._grafo.add_nodes_from(self.nodes)

        for n in self.nodes:
            self._idMapStates[n.id]=n

        for t in DAO.getAllEdgesWeight(anno, shape):
            stato1 = self._idMapStates[t[0]]
            stato2 = self._idMapStates[t[1]]
            peso = t[2]

            if peso > 0:
                self._grafo.add_edge(stato1, stato2, weight=peso)

        return self._grafo

    def getDetailsGraph(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    # ------------------------------------------------------------------------------------------------------------------------------------------
    def getPesiAdiacenti(self):

        lista=[]
        for nodo in self._grafo.nodes():
            peso_total = 0
            for vicino in self._grafo.neighbors(nodo):
                peso_total += self._grafo[nodo][vicino]['weight']
            lista.append( (nodo, peso_total) )

        return lista

    # ------------------------------------------------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    m = Model()
    m.buildGraph(2010, "circle")
    print( m.getDetailsGraph() )
