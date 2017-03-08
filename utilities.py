


def getStorageCost(datacentre, dataSet):
	return dataSet.size * n_days * datacentre.storage_cost_ratio


def getTransferCost(datacentre1 , datacentre2, size):
	return getMinimumCost(datacentre1,datacentre2)*size

#dataset = object of data block type
#dataCentres = object of type data Cntre dictionary where key is name
#defaultCenter = position of primary position of datablock 
#response time : matrix telling response type if query is from node i to j
def selectBestLocation(dataSet,suggested_centres,dataCentres,response_time, preset_avg_response_time):
	def_centre = dataSet.location()
	total_access_time = {k:0.0 for k in list(dataCentres)}
	total_response_time = {k:0.0 for k in list(dataCentres)}
	avg_response_time = {k:0.0 for k in list(dataCentres)}
	transfer_cost = {k:1000000000.0 for k in list(dataCentres)}
	storageCost ={k:getStorageCost(dataCentres[k],dataSet) for k in list(dataCentres)}

	for dcj in suggested_centres:
		if dcj != def_centre:
			for dci in dataCentres.keys():
				if dci != def_centre and dci != dcj :
					total_response_time[dcj] +=  get_total_access_time(dcj)*min(response_time[dci][defaultCenter],
						                                                    response_time[dci][dcj])
					total_access_time[dcj] += get_total_access_time(dcj)
		avg_response_time[dcj] = float(total_response_time[dcj])/total_access_time[dcj]

		if avg_response_time[dcj] > preset_avg_response_time:
			continue

		else :
			transfer_cost[dcj] = 0
			total_access_time[dcj]=0
			for dci in dataCentres.keys():
				if dci != defaultCenter and dci != dcj :
					tc_dci_dcj = getTransferCost(dci,dcj,dataSet.size())#compute using definition 5
					tc_dci_dco = getTransferCost(dci,def_centre,dataSet.size())#compute using definition 5
					transfer_cost[dcj] += total_access_time[dci]*min(tc_dci_dco,tc_dci_dcj)
					total_access_time[dcj]+=total_access_time[dci]

			if transfer_cost[dcj]+storageCost[dcj] < transfer_cost[m]+storageCost[m]:
				m = dcj
	return m,transfer_cost[m]+storageCost[m]




