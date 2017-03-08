from models import DataCentre, DataSet
from graph import graph
from  random import choice
import matplotlib.pyplot as plt
N_days = 30

#radom Generators
def getRandom(minim,maxm):
	return choice(range(minim,maxm))

def getRandomLoc(notin):
	x = choice(range(0,101,30))
	y = choice(range(0,101,30))
	if (x,y) in notin:
		return getRandomLoc(notin)
	notin.append((x,y))
	return (x,y)

def getRandomEdge(nds,notin,maxdelay=10,maxrate=41):
	x = choice(range(1,nds+1))
	y = choice(range(1,nds+1))
	wt = choice(range(1,maxrate))
	delay = choice(range(1,maxdelay))
	if (x,y) in notin:
		return getRandomEdge(nds,notin)
	notin.append((x,y))
	return x,y,wt,delay

def getRamdomSize(max_dataSetSize):
	return choice(range(1000,max_dataSetSize))

def getRandomNode(nds):
	return choice(range(1,nds+1))

def getRandomStorageCost():
	return choice(range(1,1000))

############################################################################################


class networkSimulator():
	def __init__(self,centres= 20 , dataSets = 1000 , max_dataSetSize=10000 , max_edges=30):
		notin=[]
		self.datacentres = {i+1:DataCentre( getRandomLoc(notin),i+1, getRandomStorageCost()) for i in range(centres)}
		self.datasets={}
		for j in range(1,dataSets+1):
			self.datasets[j] = DataSet(getRandomNode(centres), getRamdomSize(max_dataSetSize) ,j, 1)
		#generating access frequency of node i to dataset j
		self._access_freq = [[getRandom(2,1000) for _ in range(dataSets+1)] for _ in range(centres+1)]
		#graph where edges denote unit transfer cost
		self._GraphNet = graph(self.datacentres.keys())

		occ = [[0 for _ in range(centres+1)] for _ in range(centres+1)]

		notin =[]
		for e in range(max_edges):
			x,y,wt,delay = getRandomEdge(centres,notin)
			if occ[x][y] ==0 :
				self._GraphNet.addEdge(x,y,(delay,wt))
				occ[x][y] = 1
				occ[y][x] = 1
		self.edges=notin

		#displaying data sets
		self._responseTime =[[1000000000 for _ in range(centres+1)] for _ in range(centres+1)]
		for i in range(1,centres+1):
			for j in range(i+1,centres+1):
				if i!=j :
					self._responseTime[i][j] = self._GraphNet.minimumCostPath(i,j,fct=0)#0 for dealy and 1 for cost
					self._responseTime[j][i] = self._responseTime[i][j]


	def showDataCentres(self,msg=None):
		fig, ax = plt.subplots(1, 1)
		ax.grid()

		print "Data Centres"
		for dc in self.datacentres.keys():
			(x,y) = self.datacentres[dc].location()
			print dc,(x,y)
			plt.scatter([x],[y],label=str(dc),color='r',s=400,alpha=0.5)
			ax.annotate('D'+str(dc),xy=(x,y),xytext=(x+1,y+1))

		print "DataSets"
		dsts = {}
		for ds in self.datasets.keys():
			lc = self.datasets[ds].location()
			(x,y) = self.datacentres[lc].location()
			print ds,(x,y)
			if (x,y) not in dsts.keys():
				dsts[(x,y)] = "-->"+str(lc)+":"
			dsts[(x,y)] +=  ', R'+str(ds)

		for (x,y),lb in dsts.iteritems():
			plt.scatter([x],[y],label=str(dc),color='b',s=100,alpha=0.5)
			ax.annotate(lb,xy=(x,y),xytext=(x-5,y-5))

		for (a,b) in self.edges:
			(x1,y1) = self.datacentres[a].location()
			(x2,y2) = self.datacentres[b].location()
			plt.plot([x1,x2],[y1,y2],color='b')
		if msg != None:
			print msg
		 
		plt.show()

	def totalCost(self):
		totalCost =0
		storageCost = 0
		networkCost =0
		for ds in self.datasets.keys():
				if self.datasets[ds].isPrime():
					self.datasets[ds].cost =0

		for dc in self.datacentres.keys():
			for ds in self.datasets.keys():
				if self.datasets[ds].isPrime():
					replicas = self.datasets[ds].replicas()
					dest = [ self.datasets[r].location() for r in replicas ]
					dest.append(self.datasets[ds].location())
					minratePath = self._GraphNet.minimumCostPath(dc,dest,fct=1)
					networkCost+= minratePath*self.datasets[ds].size()*self._access_freq[dc][ds]
					#print dc,minratePath*self.datasets[ds].size()*self._access_freq[dc][ds]
					self.datasets[ds].cost+=minratePath*self.datasets[ds].size()*self._access_freq[dc][ds]

		for ds in self.datasets.keys():
			lc = self.datasets[ds].location()
			storageCost+= self.datasets[ds].size() * self.datacentres[lc].storage_cost_ratio()
			self.datasets[self.datasets[ds].ID()].cost+=self.datasets[ds].size() * self.datacentres[lc].storage_cost_ratio()
			#if self.datasets[ds].isPrime():
				#print "Datasets :"+str(ds)+"  has cost imposing: "+str(self.datasets[ds].cost)

		totalCost = storageCost+networkCost
		return totalCost, networkCost, storageCost


	def isScarce(self, ds, acc_frq_th , rp_time_th):
		print "Scracity of Data source : "+str(ds)
		access_feq = 0
		#get total access freq of replicas
		for dc in self.datacentres.keys():
			access_feq += self._access_freq[dc][ds]

		#get the total response time for this replic
		response_time = 0
		rep_locations = [self.datasets[ds].location()]
		#get locations of all the replicas
		for rp in self.datasets[ds].replicas():
			lc = self.datasets[rp].location()
			rep_locations.append(lc)
		print "Replica Locations : ",rep_locations
		cts =0
		for dc in self.datacentres.keys():
			if dc not in rep_locations:
				th_rep= 1000000000
				for rp in rep_locations:
					th_rep = min(th_rep, self._responseTime[dc][rp])

				print "Response time to "+str(dc)+" : "+str(th_rep)
				response_time+=th_rep
		response_time = float(response_time)
		response_time/= len(rep_locations)
		response_time/=self.datasets[ds].size()
		access_feq = float(access_feq)/N_days
		print "Total Response time and Access Frequency ",response_time,access_feq
		

		if response_time > rp_time_th and access_feq > acc_frq_th :
			print "Hence Scarce "
			print "###########################################################################"
			return True
		print "Not Scarce"
		print "###########################################################################"
		return False

	def createReplica(self,location,par_id):
		newds = DataSet(location,self.datasets[par_id].size(),par_id,0)
		self.datasets[newds._count] = newds
		self.datasets[par_id].addReplica(newds._count)
		print DataSet._count



	def selectBestLocation(self,ds,suggested_centres):
		def_centre = self.datasets[ds].location()
		#we try to place out datasets to all the suggested loaction and find the cost after placing replica there
		res ={}
		locations = [def_centre]
		for rp in self.datasets[ds].replicas():
				lc = self.datasets[rp].location()
				locations.append(lc)
		for dcj in suggested_centres:
			if dcj not in locations:
				res[dcj]=0
				locations.append(dcj)
				for dci in self.datacentres.keys():
					if dci not in locations :
						minratePath = self._GraphNet.minimumCostPath(dci,locations,fct=1)
						res[dcj]+=minratePath*self.datasets[ds].size()*self._access_freq[dci][ds]
					res[dcj]+=self.datasets[ds].size() * self.datacentres[dci].storage_cost_ratio()
				locations.pop()
		return res

	def runOptimizer(self, max_replicas=3,AFTH=150, RPTH=0.01):
		scarce_sets =[]
		for  ds in self.datasets.keys():
			#determine if the current dataSet is scarce  source and no of replicas is less the max_allowed
			if self.datasets[ds].isPrime() and  self.isScarce(ds,AFTH,RPTH) and len(self.datasets[ds].replicas()) < max_replicas:
				#construct the graph having structure same as the original graph however having the edge cost according the
				#load on the each edge added while quering one of the replicas
				#the choice of repica has distribution same as distribution for channel availability
				scarce_sets.append(ds)

		print "scarce Data Sources : ",scarce_sets
		suggestions = self._GraphNet.findBestPositions()
		print "Suggested Positions :", suggestions
		for ds in scarce_sets:
			print "Current Cost Imposed by ",ds,self.datasets[ds].cost
			optimized_costs = self.selectBestLocation(ds,suggestions)
			print optimized_costs
			mini =min(optimized_costs, key=optimized_costs.get)
			print mini,optimized_costs[mini]
			if optimized_costs[mini] < self.datasets[ds].cost:
				self.createReplica(mini,ds)

		

if __name__ == '__main__':
	sim = networkSimulator(centres=15,dataSets=15,max_edges=15)
	
	sim.showDataCentres()
	pv = sim.totalCost()
	n_iter=5
	res = [pv]
	for i in range(n_iter):
		sim.runOptimizer(max_replicas=3,AFTH=150, RPTH=0.01)
		cur = sim.totalCost()
		res.append(cur)
		msg= "Print Current Costs : (Total : "+str(cur[0])+"  , Network : " + str(cur[1])+" , Storage : "+str(cur[2])+" , )"
		sim.showDataCentres(msg)	
	print res

	its =[i for i in range(n_iter+1)]
	Total = [r[0] for r in res]
	Ntwk = [r[1] for r in res]
	Storage = [r[2] for r in res]

	plt.plot(its, Ntwk)
	plt.title(' Network Cost ')
	plt.scatter(its, Ntwk)
	plt.show()


	plt.plot(its, Storage)
	plt.scatter(its, Storage)
	plt.title(' Storage Cost ')
	plt.show()

	plt.plot(its, Total)
	plt.scatter(its, Total)
	plt.title(' Total Cost ')
	plt.show()
	# Fine-tune figure; make subplots close to each other and hide x ticks for
	# all but bottom plot.
	

	














