import copy
import geopy.distance
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):

        self._grafo = nx.Graph()
        self.nodes = []
        self._idMapStates = {}

        self._bestPath = []
        self._bestDistanza = 0

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

        for t in DAO.getAllEdgesWeightMio(anno, shape):
            stato1 = self._idMapStates[t[0]]
            stato2 = self._idMapStates[t[1]]
            peso = t[2]

            if peso > 0:
                self._grafo.add_edge(stato1, stato2, weight=peso)

        #Per il punto 2:
        for e in self._grafo.edges( data=True):
            self._grafo[e[0]][e[1]]["distance"] = self.getDistanzaDueStati(e[0], e[1])

        return self._grafo

    def getDetailsGraph(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    # ------------------------------------------------------------------------------------------------------------------------------------------
    def getPesiAdiacenti(self):

        lista=[]
        for nodo in self._grafo.nodes():
            pesoTot = 0
            for vicino in self._grafo.neighbors(nodo):
                pesoTot += self._grafo[nodo][vicino]['weight']
            lista.append( (nodo, pesoTot) )

        return lista

    # ------------------------------------------------------------------------------------------------------------------------------------------
    def camminoOttimo(self):
        #massimizza distanza, sempre crescente
        self._bestPath=[]
        self._bestDistanza=0
        parziale=[]

        for nodo in self.nodes:
            parziale.append(nodo)
            self._ricorsione(parziale)
            parziale.pop()

        ris=[]
        for i in range( 0, len(self._bestPath)-1):
            peso = self._grafo[self._bestPath[i]][self._bestPath[i+1]]["weight"]
            distanza = self._grafo[self._bestPath[i]][self._bestPath[i+1]]["distance"]
            ris.append( (self._bestPath[i], self._bestPath[i+1], peso, distanza) )

        return self._bestPath, self._bestDistanza, ris

    # -------------------------------------------------------------------------------------------------------------------------------------------
    def _ricorsione(self, parziale):

        #è ammissibile (crescente --> lo guardi dopo nei vincoli)
        #è la migliore
        distanza = self.getDistanza(parziale)
        if distanza > self._bestDistanza:
            self._bestDistanza = distanza
            self._bestPath = copy.deepcopy(parziale)

        else:
        #continua a cercare
            ultimo = parziale[-1]
            for vicino in self._grafo.neighbors(ultimo):
                #vincoli
                if len(parziale)==1: #primo nodo, ha solo 1 arco
                    parziale.append(vicino)
                    self._ricorsione( parziale)
                    parziale.pop()
                else:
                    if vicino not in parziale and (self._grafo[ultimo][vicino]["weight"] >
                                                   self._grafo[parziale[-2]][parziale[-1]]["weight"]):
                        parziale.append(vicino)
                        self._ricorsione(parziale)
                        parziale.pop()

    # -------------------------------------------------------------------------------------------------------------------------------------------
    def getDistanza(self, listaNodi):

        distanza=0
        if len(listaNodi)==1:
            return 0
        for i in range(0, len(listaNodi)-1):
            distanza += self._grafo[listaNodi[i]][listaNodi[i+1]]["distance"]
        return distanza

    def getDistanzaDueStati(self, s1, s2):
        coord1 = (s1.Lat, s1.Lng)
        coord2 = (s2.Lat, s2.Lng)
        distanza = geopy.distance.distance(coord1, coord2).km
        return distanza
    # -------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    m = Model()
    m.buildGraph(2010, "circle")
    print( m.getDetailsGraph() )
    print( m.getPesiAdiacenti() )
