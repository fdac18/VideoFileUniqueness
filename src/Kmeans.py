import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys
import random
import math
import csv

K=7		#default K value
MaxI=800	#default limit on iterations
MVThresh = .05	#movement threshold
NPCA = 2	#number of PCAs to look through

#class used to organize data by cluster
class Cluster:
	def __init__(self, num, x, y):
		self.Num = num
		self.X = x	#x-center of the cluster
		self.Y = y	#y-center of the cluster
		self.frames = []

	def addFrames(self, F):
		self.frames.append(F)
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
		for f in self.frames:
			f.printS()

#class to hold frame data
class Frame:
	def __init__(self, fNo, x, y):
		self.FrameNo = fNo
		self.X = x	#x value of the corresponding PCA
		self.Y = y	#y value of the corresponding PCA
#		self.Frame = Fr.copy();	#have the frame on hand if necessary
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


def getData(str):
	data = []
	with open(str) as CSV_:
		d = csv.reader(CSV_, delimiter=',')
		for i, row in enumerate(d):
			if(i!=0):
				for index, R in enumerate(row):
					try:
						row[index] = int(R)
					except:
						continue
				data.append(row)
				print(row)
#       print(data)
	return data

def Dis(clu, S):
	#return the distance of the cluster and the Frame
	return (math.sqrt((clu.getX() - S.getX())**2+(clu.getY() - S.getY())**2))

def Mindex(D):
	#return the minimum index of a distance
	A = math.inf
	out = 0
	for index, i in enumerate(D):
		if(i < A):
			A = i
			out = index
	return out

def Kmeans(clusters, Frames, itter):
	if(itter == MaxI):	#safety net
		return MaxI
	tmp = []
	#figure out where each school clusters to
	for F in Frames:
		for c in clusters:
			tmp.append(Dis(c, F))
		clusters[Mindex(tmp)].addFrame(F)
		tmp.clear()

	Xavg = 0
	Yavg = 0
	MV = 0
	#set the position of the cluster to the average of the schools closest to it
	for c in clusters:
		c.frames.clear()
		MV = 0
		#get the average
		for F in c.frames:
			Xavg += F.getX()
			Yavg += F.getY()
		#find if the cluster has no frames
		if(len(c.frames) != 0):
			c.setX(Xavg/len(c.frames))
			c.setY(Yavg/len(c.frames))
		else:
			print("cluster %d has no nearby frames in itteration %d" %(c.Num, itter))

		Xavg = 0
		Yavg = 0
		if((len(c.frames)!= 0) and (math.sqrt((Xavg/len(c.frames))**2+(Yavg/len(c.frames))**2) < MVThresh)):
			MV+=1

	if(MV == K-1):
		return itter
	A=0
	A = Kmeans(clusters, Frmaes, itter+1)
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
def CLUSTER(data): #pixel data comes in in 2d vector, only way to do svd

	#perform svd, need to decide on some issues
	U, SIG, VT= np.linalg.svd(data, full_matrices=True)

	ra = []
	#select K random frames for K-means
	for x in range(K):
		ra.append(random.randint(0, len(data)-1))
	clu = []
	#set up initial cluster based on the random frames
	for x in range(0, K):
		A = Cluster(x, data[ra[x]].getX(), data[ra[x]].getY())
		clu.append(A)
	Fr = []
	#make the frame containers
	for i in range(0, len(VT[0])-1):
		Fr.append(i,VT[0][i], VT[1][i])
	OUT = Kmeans(clu, Fr, 0)
	tmp = []
#	for F in Fr:
#		for c in clu:
#			tmp.append(Dis(c, F))
#		clu[Mindex(tmp)].addFrame(F)
#		tmp.clear()
	for C in clu:
		C.printC()
	print(OUT)
	A = MinInter(clu, points)
	B = MaxIntra(clu)
	PlotD(points, clu)
	print("minimal intercluster distance = %f" %(A))
	print("Maximum intracluster distance = %f" %(B))
	print("Dunn index = %f" %(B/A))

D = getData(sys.argv[1])
CLUSTER(D)
