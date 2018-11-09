import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import sys
import random
import math
K=7		#default K value
MaxI=800	#default limit on iterations
MVThresh = .05	#movement threshold

class Cluster:
	def __init__(self, num, x, y):
		self.Num = num
		self.X = x
		self.Y = y
		self.schools = []

	def addSch(self, S):
		self.schools.append(S)
	def getNo(self):
		return self.Num

	def setX(self, x):
		self.X = x
	def getX(self):
		return self.X

	def setY(self, y):
		self.Y = y
	def getY(self):
		return self.Y
	def printC(self):
		print("%d\t%f\t%f" %(self.Num, self.X, self.Y))
		for s in self.schools:
			s.printS()
class School:
	def __init__(self, name, x, y):
		self.name = name
		self.X = x
		self.Y = y
		self.clusterNo = -1
	def setCluster(self, A):
		self.clusterNo = A
	def getCluster(self):
		return self.clusterNo
	def getName(self):
		return self.name
	def getX(self):
		return self.X
	def getY(self):
		return self.Y
	def printS(self):
		print("--%s" %(self.name))

def cleanData(str):
	file = open(str, "r")
	lines = file.readlines()
	file.close()
	names = []
	data = []
	for line in lines:
		line = line.replace("\n", "")
		line = line.replace("[","")
		line = line.replace("]","")
		if(line[0]=='|'):
			names.append(line)
		else:
			data.append(line)
	temp = []
	for index, line in enumerate(names):
		temp = line.split('|')
		names[index] = temp[2]
	temp = []
	for index, line in enumerate(data):
		temp = line.replace(" ", "")
		temp = temp.split(',')
		for i, a in enumerate(temp):
			temp[i] = float(temp[i])
		data[index] = temp
	Schools = []
	for index, name in enumerate(names):
		A = School(name, data[0][index], data[1][index])
		Schools.append(A)
	return Schools

def Dis(clu, S):
	return (math.sqrt((clu.getX() - S.getX())**2+(clu.getY() - S.getY())**2))

def Mindex(D):
	A = math.inf
	out = 0
	for index, i in enumerate(D):
		if(i < A):
			A = i
			out = index
	return out

def Kmeans(clusters, SCH, itter):
	if(itter == MaxI):	#safety net
		return MaxI
	tmp = []
	#figure out where each school clusters to
	for S in SCH:
		for c in clusters:
			tmp.append(Dis(c, S))
		clusters[Mindex(tmp)].addSch(S)
		tmp.clear()

	Xavg = 0
	Yavg = 0
	MV = 0
	for c in clusters:
		MV = 0
		for S in c.schools:
			Xavg += S.getX()
			Yavg += S.getY()
		if(len(c.schools) != 0):
			c.setX(Xavg/len(c.schools))
			c.setY(Yavg/len(c.schools))
		Xavg = 0
		Yavg = 0
		if(len(c.schools)!= 0 and np.sqrt((Xavg/len(c.schools))**2+(Yavg/len(c.schools))**2) < MVThresh):
			MV+=1
		c.schools.clear()

	if(MV == K-1):
		return itter
	A=0
	A = Kmeans(clusters, SCH, itter+1)
#	for C in clusters:
#		C.printC()

	return A
def MinInter(clusters, S):
	tmp = []
	for c in clusters:
		for A in c.schools:
			A.setCluster(c.getNo)
	for sc in S:
		for sch in S:
			if(sc.getCluster() != sch.getCluster()):
				tmp.append(math.sqrt((sc.getX() - sch.getX())**2+(sc.getY() - sch.getY())**2))
	return min(tmp)
#def MaxIntra(clusters):
#	out = 0
#	i=0
#	k=0
#	tmp = []
#	for c in clusters:
#		while(i < len(c.schools)-1):
#			k=i+1
#			while(k < len(c.schools)):
#				tmp.append(math.sqrt((c.schools[i].getX() - c.schools[k].getX())**2+(c.schools[i].getY() - c.schools[k].getY())**2))
#				k+=1
#			i+=1
#	return max(tmp)

def PlotD(Sch, clus):
	plt.figure()
	col = ['bo','go','ro','co','mo','yo','ko']
	Ccol = ['b+','g+','r+','c+','m+','y+','k+']
	X = []
	Y = []
	i=0
	for c in clus:
		plt.plot(c.getX(), c.getY(), Ccol[i%len(Ccol)])
		for S in c.schools:
			X.append(S.getX())
			Y.append(S.getY())
		plt.plot(X,Y, col[i%len(col)])
		X.clear()
		Y.clear()
		i+=1
#	for S in Sch:
#		X.append(S.getX())
#		Y.append(S.getY())
#	plt.plot(X,Y, 'ro')
	legend = 'K value = %d'%(K)
	leg = plt.legend([legend], loc='best', borderpad=0.3,
		shadow=False, prop=matplotlib.font_manager.FontProperties(size='small'),
		markerscale=0.4)
	leg.get_frame().set_alpha(0.4)
	plt.ylabel("pca1")
	plt.xlabel("pca2")
	outF = "cluster.png"
	plt.savefig(outF)
	plt.close()
def CLUSTER():
	if(len(sys.argv) < 2):
		print("usage: python3 Kmeans.py [input_file]")
		return
	sc = cleanData(sys.argv[1])

	ra = []
	for x in range(K):
		ra.append(random.randint(0, len(sc)-1))
#	print(ra)
	clu = []
	#set up initial cluster
	for x in range(0, K):
		A = Cluster(x,sc[ra[x]].getX(), sc[ra[x]].getY())
		clu.append(A)

	OUT = Kmeans(clu, sc, 0)
	tmp = []
	for S in sc:
		for c in clu:
			tmp.append(Dis(c, S))
		clu[Mindex(tmp)].addSch(S)
		tmp.clear()
	for C in clu:
		C.printC()
	print(OUT)
	A = MinInter(clu, sc)
	B = MaxIntra(clu)
	PlotD(sc, clu)
	print("minimal intercluster distance = %f" %(A))
	print("Maximum intracluster distance = %f" %(B))
	print("Dunn index = %f" %(B/A))
#	print("SCHOOLS")
#	for line in sc:
#		line.printS()

CLUSTER()
