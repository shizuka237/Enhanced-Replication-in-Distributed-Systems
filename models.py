
class DataSet(object):
	_count =0
	def __init__(self,loc, size, par=None,isprime=0):
		self._loc = loc
		self._size =size
		self._origBlockid =par
		self._isPrime = isprime
		self._id = DataSet._count
		DataSet._count+=1
		self._replicas = []
		self._nr =0
		self.cost =0

	def __str__(self):
		return self._link

	def ID(self):
		return self._origBlockid

	def size(self):
		return self._size

	def location(self):
		return self._loc

	def addReplica(self, rid):
		self._replicas.append(rid)
		self._nr+=1

	def resetReplicas(self):
		self._replicas=[]
		self._nr = 0

	def replicas(self):
		return self._replicas

	def location(self):
		return self._loc

	def isPrime(self):
		return self._isPrime

	def nr(self):
		return self._nr




class DataCentre(object):

	def __init__(self,lc,idd,stc = 1.0):
		self._location= lc
		self._storage_cost_ratio = stc
		self._id = idd

	def location(self):
		return self._location
		
	def __int__(self):
		return self._id

	def ID():
		return self._id

	def storage_cost_ratio(self):
		return self._storage_cost_ratio
