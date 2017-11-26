import numpy as np
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
# from total_arrange import get_data
import pickle
# A1, Y, Ate, Yte = get_data('dataset3.csv', 4, 'hot')
def safeLoad(filename):
	return pickle.load(open(filename, 'rb'))

def safeKeep(obj,filename):
	with open(filename, 'wb') as op:
		pickle.dump(obj,op,pickle.HIGHEST_PROTOCOL)

def train():
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
	X = feature

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
	testX = feature

	def change(arr):
		if arr=='pop':
			return [0,0,0,1]
		elif arr=='jazz':
			return [0,1,0,0]
		elif arr=='metal':
			return [0,0,1,1]
		else:
			return [1,0,0,0]

	labels = []
	for i in Y:
		labels.append(change(i))
	Y = labels

	testlabels = []
	for i in testY:
		testlabels.append(change(i))
	testY = testlabels
	#
	np.set_printoptions(threshold=np.nan)
	X = preprocessing.scale(X)
	testX = preprocessing.scale(testX)
	np.random.seed(7)
	#
	model = Sequential()
	model.add(Dense(20, input_dim=225, init='uniform', activation='relu'))
	for i in range(9):
	    model.add(Dense(40, init='uniform', activation='relu'))
	model.add(Dense(4, init='uniform', activation='sigmoid'))

	model.compile(loss='binary_crossentropy', optimizer='adam',
	              metrics=['accuracy'])

	model.fit(X, Y, nb_epoch=27, batch_size=1)
	model.save('model.h5')

<<<<<<< HEAD
scores = model.evaluate(X, Y)
print "Training Accuracy ",scores[1]*100

predictions = model.predict(testX)
scores = model.evaluate(testX, testY)
print "Testing Accuracy ",scores[1]*100

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
=======
	scores = model.evaluate(X, Y)
	print "\nTraining Accuracy ",scores[1]*100,"\n"

	predictions = model.predict(testX)
	scores = model.evaluate(testX, testY)
	print "\nTesting Accuracy ",scores[1]*100,"\n"

def test(x):
	model = load_model('../model.h5')
	some_num = 25
	# i = np.transpose(np.reshape(i,(i.shape[0]/some_num,some_num)))
	i = np.transpose(x)
	cov = np.cov(i)
	cov = cov[0:8][:]
	cov = cov.flat[:]
	arr = [len(cov) + some_num]
	arr[0:some_num] = np.mean(i,axis=1)
	arr[some_num:some_num+len(cov)] = cov
	# print np.array(arr).shape
	arr = np.array(arr)
	arr = np.reshape(arr,(1,225))
	pred = model.predict(arr)
	return pred
>>>>>>> a1e435f6efc564d83511a2536d82f5d4c56dc8c5
