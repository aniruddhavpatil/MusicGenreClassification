import numpy as np
from sklearn import neighbors
import pylab as pl
import scipy as sp
import pickle
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import sklearn.metrics as metrics



NNList = [1,3,5,7,9,11]

def safeLoad(filename):
	return pickle.load(open(filename, 'rb'))

def safeKeep(obj,filename):
	with open(filename, 'wb') as op:
		pickle.dump(obj,op,pickle.HIGHEST_PROTOCOL)

X =  np.array(safeLoad('trainvec.pkl'))
Y =  safeLoad('labels.pkl')
testX = np.array(safeLoad('testvec.pkl'))
testY = np.array(safeLoad('testlabel.pkl'))
i = 0
# def klmetrix(p,q):
# 	global i
# 	p = abs(min(p)) + p
# 	q = abs(min(q)) + q
# 	pnorm = p/max(p)
# 	qnorm = q/max(q)
# 	# print sum(pnorm),sum(qnorm)
# 	h = np.finfo(float).eps
# 	kl1 = pnorm * np.log2((pnorm + h)/(qnorm + h))
# 	kl2 = qnorm * np.log2((qnorm + h)/(pnorm + h))
# 	dist = sum(kl1 + kl2)
# 	# s = 0
# 	# # for i,val in enumerate(kl1):
# 	# # 	s += val
# 	# # 	print s,val
# 	# # 	# print val
# 	# # print s
# 	# x = sp.stats.entropy(pnorm,qnorm) + sp.stats.entropy(qnorm,pnorm)
# 	# # print x
# 	# print dist,i
# 	i += 1
# 	return dist
song_n = 15
some_num = 25

def KL_auxillary(p,q):
	# Skipped the log(det(sample.cov_inv)q/det(test.sample.cov_inv)) coz core purpose is to calculate distance not
	# return sp.stats.entropy(p,q)

	p = np.transpose(np.reshape(p, (p.shape[0]/some_num,some_num)))
	q = np.transpose(np.reshape(q, (q.shape[0]/some_num,some_num)))
	p_cov = np.cov(p)
	q_cov = np.cov(q)

	p_det = np.linalg.det(p_cov)
	q_det = np.linalg.det(q_cov)

	if q_det == 0:
		q_det = 1


	dist = -song_n * 2
	q_cov_inv = np.linalg.inv(q_cov)

	dist += np.trace(q_cov_inv.dot(p_cov))
	# print(dist)
	temp = (np.mean(p,axis=1) - np.mean(q,axis=1))
	dist += np.transpose(temp).dot(q_cov_inv).dot(temp)
	# dist +=  temp.T.dot(np.linalg.inv(np.cov(p))).dot(temp)
	ans = abs(dist/2)
	return ans

def KL_divergence(p, q):
	ans = KL_auxillary(p,q) + KL_auxillary(q,p)
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


predictionsKL = []
predictionsHellinger = []
for i in NNList:
	knn=neighbors.KNeighborsClassifier(n_neighbors=i,metric=KL_divergence)
	knn.fit(X, Y)
	prediction = knn.predict(testX)
	accuracy = metrics.accuracy_score(testY,prediction)
	predictionsKL.append(accuracy)
	print "KL=",accuracy

	knn=neighbors.KNeighborsClassifier(n_neighbors=i,metric=hellingers_distance)
	knn.fit(X, Y)
	prediction = knn.predict(testX)
	accuracy = metrics.accuracy_score(testY,prediction)
	predictionsHellinger.append(accuracy)
	print "Hellinger=",accuracy
	print "Done with nn=",i

print predictionsKL
print predictionsHellinger

plt.plot(NNList,predictionsKL, 'r--')
plt.plot(NNList,predictionsHellinger,'b--')
red_patch = mpatches.Patch(color='red', label='KL Divergence')
blue_patch = mpatches.Patch(color='blue', label='Hellinger\'s Distance')
plt.legend(handles=[red_patch,blue_patch])
plt.xlabel('Number of nearest neighbors')
plt.ylabel('Accuracies (0-1)')
plt.show()
# print X.shape
# knn.fit(X, Y)
# # safeKeep(knn, 'knn.pkl')
#
# prediction = knn.predict(testX)
# correct = 0
#
# for i,val in enumerate(prediction):
# 	if val == testY[i]:
# 		correct += 1
# 	print val,testY[i]
#
# print float(correct)/testY.shape[0]
