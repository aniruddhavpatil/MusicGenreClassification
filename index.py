import os
import sys
import numpy as np
from mfcc import calc_mfcc
from nn import test
from reco import runreco
import pickle

class Setup:
    def __init__(self):
        self.X = []
        self.Y = []
        self.testX = []
        self.testY = []
        pass

    def check(self):
        if len(sys.argv) < 2:
            print 'Usage :- python index.py mode train_dir(optional) test_dir(optional)'
            return False
        return True

    def extract_features(self,filename):
        feature_vec = calc_mfcc(filename)
        return feature_vec

    def train(self,label,feature_vec):
        self.X.append(feature_vec.flat[:])
        self.Y.append(label)
        # print feature_vec.flat[:],label

    def test(self,label,feature_vec):
        self.testX.append(feature_vec.flat[:])
        self.testY.append(label)

    def initData(self):
        train_dir = sys.argv[1]
        test_dir = sys.argv[2]
        for root, dirs, files in os.walk(train_dir, topdown=False):
            for filename in files:
                label = str(root.split('/')[-1])
                feature_vec = self.extract_features(os.path.join(root,filename))
                self.train(label,feature_vec)
                print filename, "Done"

        for root, dirs, files in os.walk(test_dir, topdown=False):
            for filename in files:
                label = str(root.split('/')[-1])
                feature_vec = self.extract_features(os.path.join(root,filename))
                self.test(label,feature_vec)

    def safeKeep(self,obj,filename):
    	with open(filename, 'wb') as op:
    		pickle.dump(obj,op,pickle.HIGHEST_PROTOCOL)


def run(c,filename='',genre=''):
    if c == 'normal':
        setup = Setup()
        if not setup.check():
            exit()
        setup.initData()
        setup.safeKeep(setup.X, 'trainvec.pkl')
        setup.safeKeep(setup.testX, 'testvec.pkl')
        setup.safeKeep(setup.testY, 'testlabel.pkl')
        setup.safeKeep(setup.Y, 'labels.pkl')
    elif c == 'nn':
        return test(calc_mfcc(filename))
    elif c == 'reco':
        return runreco(calc_mfcc(filename), genre)

# run()
