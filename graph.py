from copy import deepcopy

class graph():
	def __init__(self,nodes,adj=None):
		self._g={}
		self._gw={}
		if adj != None :
			self._g = adj
		for nd in nodes:
			self._g[nd] =[]
			self._gw[nd] =[]
	
	def addEdge(self,x,y,wt):
		#print x,y,w
		self._g[x].append(y)
		self._g[y].append(x)
		self._gw[x].append(wt)
		self._gw[y].append(wt)
		return

	def make_mst(self, cur,vis,MST,cost,par,parc,fct):
		vis[cur] = 1
		if(par[cur]!=cur):
			MST.append( (par[cur],cur,parc[cur]) )

		for i  in range(len(self._g[cur])):
			nb = self._g[cur][i]
			nbw = self._gw[cur][i][fct]
			if vis[nb]==0 and cost[nb] > cost[cur]+ nbw:
				cost[nb] = cost[cur] + nbw
				par[nb] = cur
				parc[nb] = nbw

		#print "\n"
		nd = cur
		mincost = 1000000000
		for j in self._g.keys():
				if vis[j]==0 and cost[j] < mincost:
					nd = j
					mincost = cost[j]
		
		if nd !=cur :
			self.make_mst(nd,vis,MST,cost,par,parc,fct)

		
		
	def miniumSpanningTree(self,fct=0):
		nodes =self._g.keys()
		#print nodes
		MST = []
		#waiting = heap()
		cur = nodes[0]
		vis={k:0 for k in nodes}
		print vis
		cost ={k:1000000000 for k in nodes}
		par ={k:0 for k in nodes}
		parc ={k:0 for k in nodes}
		cost[cur] = 0
		par[cur] =cur
		self.make_mst(cur,vis,MST,cost,par,parc,fct)
		return MST

	def dijkastra(self,cur, vis , cost, dest,par ,fct):
		vis[cur]=1
		if type(dest) is list  and cur in dest:
			tmp = cur
			while par[cur]!=cur:
				#print cur,"<--",
				cur = par[cur]
			#print cur
			return cost[tmp]
		elif(type(dest) is not list and cur==dest):
			while par[cur]!=cur:
				#print cur,"<--",
				cur = par[cur]
			#print cur
			return cost[dest]

		for i  in range(len(self._g[cur])):
			nb = self._g[cur][i]
			nbw = self._gw[cur][i][fct]
			if vis[nb]==0 and cost[nb] > cost[cur]+ nbw:
				cost[nb] = cost[cur] + nbw
				par[nb] = cur
		nd = cur
		mincost = 1000000000
		for j in self._g.keys():
				if vis[j]==0 and cost[j] < mincost:
					nd = j
					mincost = cost[j]
		if nd != cur :
			return self.dijkastra(nd, vis , cost , dest, par,fct)
		return 1000000000

	def minimumCostPath(self, src, dest,fct=0):
		nodes =self._g.keys()
		cur = src
		vis={k:0 for k in nodes}
		cost ={k:1000000000 for k in nodes}
		par ={k:0 for k in nodes}
		cost[cur] = 0
		par[cur] =cur
		return self.dijkastra(cur,vis,cost,dest,par,fct)
		

	
	
	def show(self):
		edges = []
		for r in self._g.keys():
			for j in self._g[r]:
				if (r,j) not in edges and (j,r) not in edges:
					edges.append((r,j))
		
		for (x,y) in edges:
			print x,"-----",y

	def findBestPositions(self):
		deg = {k:len(self._g[k]) for k in self._g.keys()}
		gp = deepcopy(self._g)
		nodes=[]
		while 1:
			maxi = gp.keys()[0]
			for nd in gp.keys():
				if deg[nd] > deg[maxi]:
					maxi = nd
			nodes.append(maxi)
			for nb in gp[maxi]:
				deg[nb]-=1
				if deg[nb] == 0  and nb in gp.keys():
					del gp[nb]	
			if 	maxi in gp.keys():
				del gp[maxi]
			#print gp
			if len(gp)==0:
				break
		return nodes




########################################################################################



		


if __name__ == "__main__":
	n = int(raw_input())
	nodes = [(i+1) for i in range(n)]
	G = graph(nodes)
	E = int(raw_input())
	for i in range(E):
		x,y,d,w = [int(v) for v in raw_input().split()]
		G.addEdge(x,y,(d,w))
	#G.show()
	x,y = [int(v) for v in raw_input().split()]
	print G.minimumCostPath(x,y)
	'''
	M = G.miniumSpanningTree()
	print M
	MST = graph(nodes)
	for (x,y,w) in M:
		MST.addEdge(x,y,w)
	MST.show()
	print MST.findBestPositions()
	'''




