import sys, os
import numpy as np
import IO

class Part : 
	def __init__(self,N,type):
		
		self.x 		= np.zeros(N)
		self.y 		= np.zeros(N)
		self.z 		= np.zeros(N)

		self.vx 	= np.zeros(N)
		self.vy 	= np.zeros(N)
		self.vz 	= np.zeros(N)

		self.idx 	= np.zeros(N)
		self.mass	= np.zeros(N)
		self.epot 	= np.zeros(N)
		self.ekin 	= np.zeros(N)

		self.age 	= np.zeros(N)


		self.isStar	= type


	def define(self, filePart, i):

		self.x[i]      = filePart[0]
		self.y[i]      = filePart[1]
		self.z[i]      = filePart[2]
	
		self.vx[i]     = filePart[3]
		self.vy[i]     = filePart[4]
		self.vz[i]     = filePart[5]

		self.idx[i]    = filePart[6]
		self.mass[i]   = filePart[7]
		self.epot[i]   = filePart[8]
		self.ekin[i]   = filePart[9]

		if self.isStar :
			self.age[i]    = filePart[10]


	def mask(self, part, ma):

		self.x 		= part.x[ma]
		self.y 		= part.y[ma]
		self.z 		= part.z[ma]

		self.vx 	= part.vx[ma]
		self.vy 	= part.vy[ma]
		self.vz 	= part.vz[ma]

		self.idx 	= part.idx[ma]
		self.mass	= part.mass[ma]
		self.epot 	= part.epot[ma]
		self.ekin 	= part.ekin[ma]
		
		if self.isStar :
			self.age 	= part.age[ma]	

	def append(self, part):
		self.x = np.append(self.x, part.x)		
		self.y = np.append(self.y, part.y)
		self.z = np.append(self.z, part.z)
		self.mass = np.append(self.mass, part.mass)
		if self.isStar :
			self.age = np.append(self.age, part.age)
			
		
def getN(filename):
	filePart = open(filename, "rb")
	N 	= np.fromfile(filePart, dtype=np.int32  ,count=1)[0]
	filePart.close()
	return N

def getNtot(filename, nProc):
	Ntot=0
	for proc in range(nProc):
		Ntot += getN(filename + ".p" + str(proc).zfill(5))

	return Ntot

def read1proc(filename):
	file = open(filename, "rb")	
	N = np.fromfile(file, dtype=np.int32  ,count=1)[0]
	a = np.fromfile(file, dtype=np.float32,count=1)[0]
	data = np.fromfile(file, dtype=np.float32)
	file.close()

	return N,a,data

def read(filename):
	
	if "star." in filename:
		star = 1
	else:
		star = 0
	s = 10 + star

	nProc = IO.getNproc(filename)

	print "Reading file ", filename
	Ntot = getNtot(filename, nProc)
	parts = Part(Ntot, star)
	print  Ntot, "Particles"

	i = 0
	for proc in range(nProc):

		N,a,data=read1proc(filename + ".p"+ str(proc).zfill(5)	)
	
		for j in range(0,data.shape[0],s):
			parts.define(data[j:j+s] ,i )
			i+=1

	print 'Read OK'
	return Ntot,a,parts

def findFirstStar(file):
	
	Ntot,a,parts = read(file)
		
	ind = np.argmin(parts.age)
	
	print parts.x[ind]
	print parts.y[ind]
	print parts.z[ind]
	
