import pickle
from math import sqrt
from random import randrange
from random import seed 
import numpy as np 
import sklearn.metrics as metrics

def testSplit(index, val, data):
	l, r = list(), list()
	for i in data:
		if i[index] < val:
			l.append(i)
		else:
			r.append(i)
	return l, r


def ginIndex(grps, classes):
	noOfTimes = float(sum([len(grp) for grp in grps]))
	ginVal = 0.0
	for grp in grps:
		size = float(len(grp))
		if size == 0:
			continue
		score = 0.0
		for i in classes:
			poi = [row[-1] for row in grp].count(i) / size
			score += poi * poi
		ginVal += (1.0 - score) * (size / noOfTimes)
	return ginVal

def to_terminal(g):
	result = [row[-1] for row in g]
	return max(set(result), key = result.count)

def doSplit(data, noOfFeatues):
	ind, val, score, grps = 999, 999, 999, None
	classVal = list(set(row[-1] for row in data))
	features = list()

	while len(features) < noOfFeatues:
		index = randrange(len(data[0]) - 1)
		if index in features:
			continue
		elif index not in features:
			features.append(index)
	for index in features:
		for row in data:
			groups = testSplit(index, row[index], data)
			ginVal = ginIndex(groups, classVal)
			if ginVal < score:
				ind, val, score, grps = index, row[index], ginVal, groups
	return {'index': ind, 'value': val, 'groups': grps}


def split(node, maxDepth, minSize, noOfFeatues, depth):
	l, r = node['groups']
	del(node['groups'])

	if not l or not r:
		node['left'] = node['right'] = to_terminal(l + r)
		return

	if depth >= maxDepth:
		node['left'], node['right'] = to_terminal(l), to_terminal(r)
		return
	if len(l) > minSize:
		node['left'] = doSplit(l, noOfFeatues)
		split(node['left'], maxDepth, minSize, noOfFeatues, depth+1)
	else:
		node['left'] = to_terminal(l)

	if len(r) > minSize:
		node['right'] = doSplit(r, noOfFeatues)
		split(node['right'], maxDepth, minSize, noOfFeatues, depth+1)
	else: 
		node['right'] = to_terminal(r)

def subsample(data, ratio):
	noOfSamp = round(len(data) * ratio)
	sample = list()
	while len(sample) < noOfSamp:
		index = randrange(len(data))
		sample.append(data[index])
	return sample


def buildTree(train, maxDepth, minSize, noOfFeatues):
	root = doSplit(train, noOfFeatues)
	split(root, maxDepth, minSize, noOfFeatues, 1)
	return root 

def crossValSplit(dataset, nFolds):
	split = list()
	copy = list(dataset)
	foldSize = int(len(dataset) / nFolds)
	for i in range(nFolds):
		fold = list()
		while len(fold) < foldSize:
			index = randrange(len(copy))
			fold.append(copy.pop(index))
		split.append(fold)
	return split

# def acc_score(real, predVal):
# 	corr = 0
# 	for i in range(len(real)):
# 		if real[i] == predVal[i]:
# 			corr += 1
# 	return corr / float(len(real)) * 100.0

def runAlgo(dataset, algo, nFolds, *args):
	scores = list()
	folds = crossValSplit(dataset, nFolds)
	for fold in folds:
		testSet = list()
		trainSet = list(folds)
		trainSet.remove(fold)
		trainSet = sum(trainSet, [])
		for row in fold:
			temp = list(row)
			testSet.append(temp)
			temp[-1] = None
		predVal = algo(trainSet, testSet, *args)
		real = [row[-1] for row in fold]
		# acc = acc_score(real, predVal)
		acc = metrics.accuracy_score(real,predVal)
		scores.append(acc)
	return scores

def predict(node, row):
	if row[node['index']] >= node['value']:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']
	else:
		if isinstance(node['left'], dict):
			return predict(node['left'], row)
		else:
			return node['left']

def bagging_pred(trees, row):
	predVal = [predict(tree, row) for tree in trees]
	return max(set(predVal), key = predVal.count)

def subsample(dataset, ratio):
	sample = list()
	noOfSamp = round(len(dataset) * ratio)
	while len(sample) < noOfSamp:
		index = randrange(len(dataset))
		sample.append(dataset[index])
	return sample


def randomForest(train, test, maxDepth, minSize, sampleSize, n_trees, noOfFeatues):
	trees = list()
	for i in range(n_trees):
		# sample = list()
		# n_samp = round(len(dataset) * sampleSize)
		# while len(sample) < n_samp:
		# 	index = randrange(len(dataset))
		# 	sample.append(dataset[index])
		sample = subsample(train, sampleSize)
		tree = buildTree(sample, maxDepth, minSize, noOfFeatues)
		trees.append(tree)
	predVal = [bagging_pred(trees, row) for row in test]
	return predVal



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

seed(2)

dataset = X
for i, item in enumerate(dataset):
	item.append(Y[i])

maxDepth = 10
minSize = 1
nFolds = 5
sampleSize = 1.0
noOfFeatues = int(sqrt(len(dataset[0])-1))

for i in [50]:
	scores = runAlgo(dataset, randomForest, nFolds, maxDepth, minSize, sampleSize, i, noOfFeatues)
	print ('no of Trees: %d' % i)
	print ('Scores: %s' % scores)
	print('Mean Accuracy: %.3f%%' % (sum(scores * 100)/float(len(scores))))