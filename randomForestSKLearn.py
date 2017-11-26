import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
import sklearn.metrics as metrics

def safeLoad(filename):
	return pickle.load(open(filename, 'rb'))

def safeKeep(obj,filename):
	with open(filename, 'wb') as op:
		pickle.dump(obj,op,pickle.HIGHEST_PROTOCOL)


X =  np.array(safeLoad('trainvec.pkl'))
Y =  safeLoad('labels.pkl')
testX = np.array(safeLoad('testvec.pkl'))
testY = np.array(safeLoad('testlabel.pkl'))

forest = RandomForestClassifier(max_depth=100,random_state=0)
forest.fit(X,Y)

ans = forest.predict(testX)

# print ans
for i, val in enumerate(ans):
    print testY[i],val

print metrics.accuracy_score(testY,ans)
