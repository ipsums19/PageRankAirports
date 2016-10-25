#!/usr/bin/python

from collections import namedtuple
import time
import sys

class Edge:
    def __init__ (self, origin=None):
        self.originHash = dict({origin:1})

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)

    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)

edgeList = [] # list of Edge
edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport

def readAirports(fd):
    print "Reading Airport file from {0}".format(fd)
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print "There were {0} Airports with IATA code".format(cont)


def readRoutes(fd):
    print "Reading Routes file from {0}".format(fd)
    edgesTxt = open(fd, "r");
    for line in edgesTxt.readlines():
        temp = line.split(',')
        destino = temp[4]
        origen = temp[2]
        if destino in edgeHash:
            if origen in edgeHash[destino].originHash:
                edgeHash[destino].originHash[origen] += 1
            else:
                edgeHash[destino].originHash[origen] = 1
        else:
            e = Edge(origen)
            edgeHash[destino] = e
        print origen in airportHash
        airportHash[origen].outweight += 1

    edgeTxt.close()
    print "There were {0} Airports with IATA code".format(cont)

def sumWeigths(destino):
    sum = 0
    for origen, value in edgeHash[destino].originHash.iteritems():
        sum += [origen] * value / airportHash[origen].outweight
    return sum

P = dict()
def computePageRanks():
    # write your code
    n = len(airportList)
    for airport in airportHash:
        P[airport.name] = 1./n
    L = 0.8
    for a in range(10):
        Q = dict()
        for i in n:
            Q[i.name] = L * sumWeigths(i.name) + (1.-L)*n
        P = Q
    return 10

import operator
def outputPageRanks():
    sorted_P = sorted(P.items(), key=operator.itemgetter(1))
    for key, value in sorted_P:
        print key, value

def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print "#Iterations:", iterations
    print "Time of computePageRanks():", time2-time1


if __name__ == "__main__":
    sys.exit(main())
