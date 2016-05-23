#! /usr/bin/env python
############################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
###########################################################################
"""
Brief:

Authors: ictmcg(com@baidu.com)
Date:    2015/04/21 21:49:03
File:    train_gbdt.py
"""
import numpy as np
import scipy.sparse
import xgboost as xgb
import sys

dtrain = xgb.DMatrix(sys.argv[1])
dtest = xgb.DMatrix(sys.argv[2])
dpred = sys.argv[3]
max_dep = int(sys.argv[4])
num_tree = int(sys.argv[5])
dwatch = xgb.DMatrix(sys.argv[6])
weight = int(sys.argv[7])
#'''
param = {'max_depth':max_dep , 'silent':1, 'gamma':0.05, \
        'eval_metric':'error', 'booster':'gbtree'}
param['scale_pos_weight'] = weight
param['eta'] = 0.15
param['objective'] = 'binary:logistic'
param['nthread'] = 40
watchlist  = [(dwatch,'eval'), (dtrain,'train')]
num_round = num_tree
bst = xgb.train(param, dtrain, num_round, watchlist)
feature_map = bst.get_fscore()
print len(feature_map)
dict= sorted(feature_map.iteritems(), key=lambda d:d[1], reverse = True)
print dict
bst.save_model('local_gbdt_train.model')
#'''
# dump model with feature map
bst.dump_model('dump.raw.txt')

preds = bst.predict(dtest)

f = open(dpred,'w')
for pred_val in preds:
    f.write(str(pred_val)+'\n')
f.close()


# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
