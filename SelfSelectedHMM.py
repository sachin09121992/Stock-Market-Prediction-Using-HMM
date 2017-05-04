import numpy as np
from hmmlearn import hmm
import re
from yahoo_finance import Share
import warnings
warnings.filterwarnings("ignore")

def read_data():
	f=open('dow_jones_index.data','r')
	records=f.read().split('\n')[1:-1]
	prices={}
	for i in records:
		tup=i.split(',')[:7]
		try:
			prices[tup[1]].append([float(tup[3][1:]),float(tup[4][1:]),float(tup[5][1:]),float(tup[6][1:])])
		except:
			prices[tup[1]]=[[float(tup[3][1:]),float(tup[4][1:]),float(tup[5][1:]),float(tup[6][1:])]]
	#print prices
	data_tuple={}
	for company in prices:
		for i in prices[company]:
			tup=[(i[3]-i[0])/i[0], (i[1]-i[0])/i[0], (i[2]-i[0])/i[0]]
			try:
				data_tuple[company].append(tup)
			except:
				data_tuple[company]=[tup]
	#print data_tuple
	for company in data_tuple:
		data_tuple[company]=np.array(data_tuple[company])
	return [data_tuple, prices]

def createModel(data, index):
	
	#model = hmm.GMMHMM(n_components=4,n_mix=5, covariance_type="full",n_iter=10)
	model = hmm.GaussianHMM(n_components=4, covariance_type="full",n_iter=10)
	#print(data)
	model.fit([data[:-index]])
	states=model.predict(data[:-index])
	#print(states)
	#print(len(data))
	#print(model.transmat_)
	#print(model.startprob_)
	#print(model.predict_proba(data))
	#print
	#print(model.score(data))
	#predict(model,data, index)
	return model
	
def predict(model, data, index):
	max_score=0.0
	max_change=0.0
	max_high=0.0
	max_low=0.0
	for fracChange in range(-100,108,8):
		a=fracChange/1000.0
		for fracHigh in range(0,11):
			b=fracHigh/100.0
			for fracLow in range(0,11):
				c=fracLow/100.0
				s=model.score(np.vstack([data[:-index], [a,b,c]]))
				if(s>max_score):
					max_score=s
					max_change=a
					max_high=b
					max_low=c
	return [max_change,max_high,max_low]
	print data[-index]


def evaluate(data, prices):
	n=13
	sum=0.0
	for i in range(1,2):
		model=createModel(data,i)
		[max_change,max_high,max_low]=predict(model, data, i)
		open_price=prices[-i][0]
		actual_close_price=prices[-i][3]
		predicted_close_price=max_change*open_price+open_price
		print actual_close_price, predicted_close_price
		print abs(actual_close_price- predicted_close_price)/actual_close_price
		return abs(actual_close_price- predicted_close_price)/actual_close_price



	'''
	model2 = hmm.GMMHMM(n_components=4,n_mix=5, covariance_type="full",n_iter=10,params="st")
	model2.startprob_ = np.array([0.25, 0.25, 0.25,0.25])
	model2.transmat_ = np.array([[0.25, 0.25, 0.25,0.25],[0.25, 0.25, 0.25,0.25],[0.25, 0.25, 0.25,0.25],[0.25, 0.25, 0.25,0.25]])
	'''
	'''
	model = hmm.GaussianHMM(n_components=3, covariance_type="full",n_iter=10)
	model.startprob_ = np.array([0.6, 0.3, 0.1])
	model.transmat_ = np.array([[0.7, 0.2, 0.1],[0.3, 0.5, 0.2],[0.3, 0.3, 0.4]])
	model.means_ = np.array([[0.0, 0.0, 0.0], [3.0, -3.0, 3.0], [5.0, 10.0, 15.0]])
	model.covars_ = np.tile(np.identity(3), (3, 1, 1))
	X, Z = model.sample(100)
	print(X)
	print(type(X))
	print(model.fit([X]))
	'''


def yahoo():
	aa=Share('AA')
	axp=Share('AXP')
	ba=Share('BA')
	bac=Share('BAC')
	aa_data=aa.get_historical('2017-03-18','2017-04-24')
	#print aa_data
	axp_data=axp.get_historical('2017-03-18','2017-04-24')
	ba_data=ba.get_historical('2017-03-18','2017-04-24')
	bac_data=bac.get_historical('2017-03-18','2017-04-24')
	data_tuple={}
	prices={}
	for i in aa_data:
		temp=[]
		temp.append(float(i['Open']))
		temp.append(float(i['High']))
		temp.append(float(i['Low']))
		temp.append(float(i['Close']))
		#temp.append(i['Date'])
		try:
			prices['AA'].append(temp)
		except:
			prices['AA']=[temp]
	prices['AA']=prices['AA'][::-1]

	for i in axp_data:
		temp=[]
		temp.append(float(i['Open']))
		temp.append(float(i['High']))
		temp.append(float(i['Low']))
		temp.append(float(i['Close']))
		#temp.append(i['Date'])
		try:
			prices['AXP'].append(temp)
		except:
			prices['AXP']=[temp]
	prices['AXP']=prices['AXP'][::-1]

	for i in ba_data:
		temp=[]
		temp.append(float(i['Open']))
		temp.append(float(i['High']))
		temp.append(float(i['Low']))
		temp.append(float(i['Close']))
		#temp.append(i['Date'])
		try:
			prices['BA'].append(temp)
		except:
			prices['BA']=[temp]
	prices['BA']=prices['BA'][::-1]

	for i in bac_data:
		temp=[]
		temp.append(float(i['Open']))
		temp.append(float(i['High']))
		temp.append(float(i['Low']))
		temp.append(float(i['Close']))
		#temp.append(i['Date'])
		try:
			prices['BAC'].append(temp)
		except:
			prices['BAC']=[temp]
	prices['BAC']=prices['BAC'][::-1]
	for company in prices:
		for i in prices[company]:
			tup=[(i[3]-i[0])/i[0], (i[1]-i[0])/i[0], (i[2]-i[0])/i[0]]
			try:
				data_tuple[company].append(tup)
			except:
				data_tuple[company]=[tup]
	#print data_tuple
	for company in data_tuple:
		data_tuple[company]=np.array(data_tuple[company])
	return [data_tuple, prices]

#print data



if __name__ == '__main__':
	#[data_tuple, prices]=read_data()
	stocks=['AA','AXP', 'BA','BAC']
	[data_tuple, prices]=yahoo()
	error=0.0
	print prices
	for stock in stocks:
		error+=evaluate(data_tuple[stock],prices[stock])
	error=error/len(stocks)
	print error

