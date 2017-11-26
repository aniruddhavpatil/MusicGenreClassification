import scipy as sp
import numpy as np
import pickle
import random
import math
import scipy.spatial.distance

def safeLoad(filename):
	return pickle.load(open(filename, 'rb'))

def safeKeep(obj,filename):
	with open(filename, 'wb') as op:
		pickle.dump(obj,op,pickle.HIGHEST_PROTOCOL)

dictionary = {}
dictionary[0] = "braycurtis"
dictionary[1] = "canberra"
dictionary[2] = "chebyshev"
dictionary[3] = "cityblock"
dictionary[4] = "correlation"
dictionary[5] = "cosine"
dictionary[6] = "euclidian"
dictionary[7] = "hamming"
dictionary[8] = "mahalanobis"

class K_Means:

	def __init__(self,k=4,tolerance=0.001,max_iterations=500,dist_type = 0):
		self.k = k
		#when difference b/w old and new centroids is tolerance, we stop
		self.tolerance = tolerance
		self.max_iterations = max_iterations
		self.dist_type = dist_type

	def calc_distance(self,p,q):
		if self.dist_type == 0:
			return scipy.spatial.distance.braycurtis(p,q)
		elif self.dist_type == 1:
			return scipy.spatial.distance.canberra(p,q)
		elif self.dist_type == 2:
			return scipy.spatial.distance.chebyshev(p,q)
		elif self.dist_type == 3:
			return scipy.spatial.distance.cityblock(p,q)
		elif self.dist_type == 4:
			return scipy.spatial.distance.correlation(p,q)
		elif self.dist_type == 5:
			return scipy.spatial.distance.cosine(p,q)
		elif self.dist_type == 6:
			return scipy.spatial.distance.euclidean(p,q)
		elif self.dist_type == 7:
			return scipy.spatial.distance.hamming(p,q)
		
	

	def normalize(self,p):
		min_p = min(p)
		p = p - min_p
		sum_p = sum(p)
		p = p/sum_p
		#print sum(p)
		return p

	def KL_auxillary(self,p,q):
		# Skipped the log(det(sample.cov_inv)q/det(test.sample.cov_inv)) coz core purpose is to calculate distance not
		# return sp.stats.entropy(p,q)
		some_num = 25
		song_n = 15
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


	def KL_dist(self,p,q):
		return self.KL_auxillary(p,q) + self.KL_auxillary(q,p)


	def fit(self,data):
		
		#initializing first k as centroids
		self.centroids = {}
		#hard coding centroid based on prior best results
		numbers = [159,37,86,280]
		nums_picked = []
		#print
		#print "initial centroids used : ",
		i = 0
		while True:
			if len(nums_picked) == 4:
				break
			else:
				num = random.randint(0,len(data)-1)
				if num not in nums_picked:
					nums_picked.append(num)
					#print num," ", 
					self.centroids[i] = data[num]
					i+=1
		
		#loop for each iteration
		for i in range(self.max_iterations):
			self.classifications = {}

			#lists for each cluster
			for j in range(self.k):
				self.classifications[j] = []

			#assigning each datapoint to a cluster
			for featureset in data:
				distances = [self.calc_distance(featureset,self.centroids[centroid]) for centroid in self.centroids]
                		classification = distances.index(min(distances))
                		self.classifications[classification].append(featureset)
	
			prev_centroids = self.centroids
			
			#recalculating centroids
			for classification in self.classifications:
				self.centroids[classification] = np.average(self.classifications[classification],axis=0)

			optimized = True
			
			#checking if not much change in centroids
			for c in self.centroids:
				old_centroid = prev_centroids[c]
				new_centroid = self.centroids[c]
				if np.sum((old_centroid - new_centroid)/old_centroid*100.0) > self.tolerance:
					optimized = False
				else:
					pass
			
			#break if optimized
			if optimized:
				break

	def predict(self,data):
		array = []
		for featureset in data:
			distances = [self.calc_distance(featureset,self.centroids[centroid]) for centroid in self.centroids]
			classification = distances.index(min(distances))
			array.append(classification)
		
		return array


if __name__ == '__main__':

	
	best_acc = 0
	avg_acc = 0



	for m in range(0,100):

		#print "iter - ", m
	
		X =  np.array(safeLoad('trainvec.pkl'))
		Y =  np.array(safeLoad('labels.pkl'))
		testX = np.array(safeLoad('testvec.pkl'))
		testY = np.array(safeLoad('testlabel.pkl'))
		clf = K_Means(dist_type = 0)
		clf.fit(X)
		predictions_train = clf.predict(X) 
		predictions_test = clf.predict(testX)
		#list saying how many times a particular label(0,1,2,3)[based on index of the list] is predicted by kmeans when it is actually (classical,pop,metal,jazz)
		#this is all on training thing cz we are assigning the actual labels(classical ... ) to the (0,1,..) of kmeans based on majority
		list_classical = []
		list_pop = []
		list_jazz = []
		list_metal = []
		labels_used_up = []

		#initialising
		for i in range(0,4):
			list_classical.append(0)
			list_jazz.append(0)
			list_metal.append(0)
			list_pop.append(0)
			labels_used_up.append(0)

		#according to kmeans predictions our lists now have number of times a particular label (0,1,2,3) is predicted how many times it actually was (classical...)
		for i in range(0,len(predictions_train)):
			if Y[i] == 'classical':
				list_classical[int(predictions_train[i])] += 1
			elif Y[i] == 'jazz':
				list_jazz[int(predictions_train[i])] += 1
			elif Y[i] == 'pop':
				list_pop[int(predictions_train[i])] += 1
			else:
				list_metal[int(predictions_train[i])] += 1

		# print "classical", list_classical
		# print "jazz", list_jazz
		# print "pop", list_pop
		# print "metal", list_metal

		#dict of the map
		dict_labels = {}
		inv_dict = {}

		dict_labels['metal'] = -1
		dict_labels['pop'] = -1
		dict_labels['jazz'] = -1
		dict_labels['classical'] = -1

		max_metal = max(list_metal)
		max_metal_index = list_metal.index(max_metal)
		dict_labels['metal'] = max_metal_index
		inv_dict[max_metal_index] = 'metal'
		labels_used_up[max_metal_index] = -1

		# print dict_labels
		# print labels_used_up

		#assigning map based on majority since observation shows pop and metal do best job assigning for them first

		while dict_labels['pop'] == -1:
			max_pop = max(list_pop)
			max_pop_index = list_pop.index(max_pop)
			if labels_used_up[max_pop_index] == -1:
				list_pop[max_pop_index] = -1
			else:
				dict_labels['pop'] = max_pop_index
				inv_dict[max_pop_index] = 'pop'
				labels_used_up[max_pop_index] = -1

		while dict_labels['jazz'] == -1:
			max_jazz = max(list_jazz)
			max_jazz_index = list_jazz.index(max_jazz)
			if labels_used_up[max_jazz_index] == -1:
				list_jazz[max_jazz_index] = -1
			else:
				dict_labels['jazz'] = max_jazz_index
				inv_dict[max_jazz_index] = 'jazz'
				labels_used_up[max_jazz_index] = -1

		while dict_labels['classical'] == -1:
			#print "here"
			max_classical = max(list_classical)
			max_classical_index = list_classical.index(max_classical)
			#print max_classical_index
			if labels_used_up[max_classical_index] == -1:
				list_classical[max_classical_index] = -1
			else:
				dict_labels['classical'] = max_classical_index
				inv_dict[max_classical_index] = 'classical'
				labels_used_up[max_classical_index] = -1

		#print dict_labels

		#calculating accuracy on test data

		num_correct = 0
		num_wrong = 0
		num_classical_correct = 0
		num_jazz_correct = 0
		num_pop_correct = 0
		num_metal_correct = 0
		num_real_classical = 0
		num_real_metal = 0
		num_real_pop = 0
		num_real_jazz = 0

		for i in range(0,len(predictions_test)):
			
			if testY[i] == 'classical':
				num_real_classical += 1
				if inv_dict[predictions_test[i]] == 'classical':
					num_classical_correct += 1

			if testY[i] == 'pop':
				num_real_pop += 1
				if inv_dict[predictions_test[i]] == 'pop':
					num_pop_correct += 1
			
			if testY[i] == 'metal':
				num_real_metal += 1
				if inv_dict[predictions_test[i]] == 'metal':
					num_metal_correct += 1
			
			if testY[i] == 'jazz':
				num_real_jazz += 1
				if inv_dict[predictions_test[i]] == 'jazz':
					num_jazz_correct += 1







			if predictions_test[i] == dict_labels[testY[i]]:
				num_correct += 1
		
			else:
				num_wrong += 1


		accuracy = num_correct/float(num_correct + num_wrong)
		if accuracy > best_acc:
			best_acc = accuracy
		avg_acc += accuracy
		print m, " : accuracy - ", accuracy
		print "classical_accuray - ", num_classical_correct/float(num_real_classical)
		print "metal_accuray - ", num_metal_correct/float(num_real_metal)
		print "pop_accuray - ", num_pop_correct/float(num_real_pop)
		print "jazz_accuray - ", num_jazz_correct/float(num_real_jazz)


	print "best accuracy - ", best_acc
	print "avg_acc - ", avg_acc

	