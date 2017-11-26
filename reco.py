import numpy as np
from sklearn import neighbors
import pylab as pl
import scipy as sp
import pickle
import math
from mfcc import calc_mfcc
import sys

def safeLoad(filename):
	return pickle.load(open(filename, 'rb'))

def safeKeep(obj,filename):
	with open(filename, 'wb') as op:
		pickle.dump(obj,op,pickle.HIGHEST_PROTOCOL)

X =  np.array(safeLoad('trainvec.pkl'))
Y =  safeLoad('labels.pkl')
testX = ''
testY = ''
i = 0

song_n = 15
some_num = 25


def KL_divergence(p, q):
	# Skipped the log(det(sample.cov_inv)/det(test.sample.cov_inv)) coz core purpose is to calculate distance not
	# return sp.stats.entropy(p,q)
	p = np.transpose(np.reshape(p, (p.shape[0]/some_num,some_num)))
	q = np.transpose(q)
	dist = -song_n * 2
	dist += np.trace(np.linalg.inv(np.cov(p)).dot(np.cov(q)))
	# print(dist)
	temp = (np.mean(p,axis=1) - np.mean(q,axis=1))
	dist +=  temp.T.dot(np.linalg.inv(np.cov(p))).dot(temp)
	ans = abs(dist/2)
	# print ans
	return ans

def hellingers_distance(p,q):
	p = np.transpose(np.reshape(p, (p.shape[0]/some_num,some_num)))
	q = np.transpose(np.reshape(q, (q.shape[0]/some_num,some_num)))
	p_mean = np.mean(p,axis=1)
	q_mean = np.mean(q,axis=1)
	p_cov = np.cov(p)
	q_cov = np.cov(q)
	diff_mean = np.array((p_mean - q_mean))[np.newaxis]
	sum_cov = (p_cov + q_cov)/2
	exp_part = (-1/8)*(np.dot(np.dot(diff_mean, np.linalg.inv(sum_cov)), diff_mean.T))
	exp_part = np.exp(exp_part)
	scale_fac = math.pow((np.linalg.det(p_cov) * np.linalg.det(q_cov)), 0.25)
	scale_fac /= math.pow(np.linalg.det(sum_cov), 0.5)
	try:
		return math.sqrt(1 - (scale_fac * exp_part))
	except Exception:
		return 0

def runreco(x,y):
	global testX,testY
	X =  np.array(safeLoad('../trainvec.pkl'))
	Y =  safeLoad('../labels.pkl')
	testX = x
	testY = y
	best = []
	for l in range(0,len(Y)):
		if Y[l] == testY:
			dist = KL_divergence(X[l],testX)
			best.append((dist,l))

	best = sorted(best,reverse=True)[0:5]
	names = ['','','','','']
	import os
	train_dir = '../../Dataset/train'
	count = 0
	arr = []
	for root, dirs, files in os.walk(train_dir, topdown=False):
	    for filename in files:
	        arr.append((filename,root.split('/')[3]))
	        # if root.split('/')[3] == testY:
	        #     for i in range(5):
	        #         print best[i][1],count
	        #         if best[i][1] == count:
	        #             names[i] = filename
	        # count += 1

	for i in arr:
	    count += 1
	    for j in range(5):
	        if best[j][1] == count:
	            names[j] = i[0]
	return names
