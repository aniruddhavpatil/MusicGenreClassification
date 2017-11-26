from sklearn import mixture as gmm
import numpy as np 
import pickle
from math import sqrt
import sklearn.metrics as metrics

def safeLoad(filename):
	return pickle.load(open(filename, 'rb'))

X =  np.array(safeLoad('trainvec.pkl'))
Y =  safeLoad('labels.pkl')
testX = np.array(safeLoad('testvec.pkl'))
testY = np.array(safeLoad('testlabel.pkl'))

feature = []
some_num = 25

for i in X:
	i = np.transpose(np.reshape(i,(i.shape[0]/some_num,some_num)))
	cov = np.cov(i)
	cov = cov[0:8][:]
	cov = cov.flat[:]
	arr = [len(cov) + some_num]
	arr[0:some_num] = np.mean(i,axis=1)
	arr[some_num:some_num+len(cov)] = cov
	feature.append(arr)
X = np.array(feature)

feature = []

for i in testX:
	i = np.transpose(np.reshape(i,(i.shape[0]/some_num,some_num)))
	cov = np.cov(i)
	cov = cov[0:8][:]
	cov = cov.flat[:]
	arr = [len(cov) + some_num]
	arr[0:some_num] = np.mean(i,axis=1)
	arr[some_num:some_num+len(cov)] = cov
	feature.append(arr)
testX = np.array(feature)


# for i in 
# X = np.reshape(X,(X.shape[0]/some_num,some_num))

# print len(Y)
print testX.shape
train_Y_new = []
for i in Y:
	if i == 'pop':
		train_Y_new.append(0)
	elif i == 'classical':
		train_Y_new.append(1)
	elif i == 'jazz':
		train_Y_new.append(2)
	else:
		train_Y_new.append(3)

test_Y_new = []
for i in testY:
	if i == 'pop':
		test_Y_new.append(0)
	elif i == 'classical':
		test_Y_new.append(1)
	elif i == 'jazz':
		test_Y_new.append(2)
	else:
		test_Y_new.append(3)

for i in range(50):
	gmMod = gmm.GaussianMixture(n_components=4, covariance_type='full')
	gmMod.fit(X, train_Y_new)
	predVal = gmMod.predict(testX)

print metrics.accuracy_score(test_Y_new, predVal)
