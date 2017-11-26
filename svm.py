from sklearn.svm import NuSVC
import numpy as np
from sklearn import preprocessing
import pickle
import sklearn.metrics as metrics

# nu = 0.5

def safeLoad(filename):
	return pickle.load(open(filename, 'rb'))

def safeKeep(obj, filename):
	with open(filename, 'wb') as op:
		pickle.dump(obj.op, pickle.HIGHEST_PROTOCOL)

X = np.array(safeLoad('trainvec.pkl'))
Y = safeLoad('labels.pkl')
testX = np.array(safeLoad('testvec.pkl'))
testY = np.array(safeLoad('testlabel.pkl'))


clf = NuSVC(kernel = 'rbf', nu = 0.0001, degree=5)

X = preprocessing.scale(X)
testX = preprocessing.scale(testX)

clf.fit(X, Y)

predVal = clf.predict(testX)

pop = []
jazz = []
metal = []
classical = []

for i,val in enumerate(testY):
	if val == 'pop':
		pop.append([val,predVal[i]])
	elif val =='jazz':
		jazz.append([val,predVal[i]])
	elif val == 'metal':
		metal.append([val,predVal[i]])
	else:
		classical.append([val,predVal[i]])

pop_accuracy = metrics.accuracy_score(pop[:][0],pop[:][1])
jazz_accuracy = metrics.accuracy_score(jazz[:][0],jazz[:][1])
metal_accuracy = metrics.accuracy_score(metal[:][0],metal[:][1])
classical_accuracy = metrics.accuracy_score(classical[:][0],classical[:][1])

print "Pop accuracy:", pop_accuracy
print "Jazz accuracy:",jazz_accuracy
print "Metal accuracy:",metal_accuracy
print "Classical accuracy:",classical_accuracy
print "Overall accuracy:",metrics.accuracy_score(testY,predVal)
# print metrics.f1_score(testY,predVal, average='macro')
