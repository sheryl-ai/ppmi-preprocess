#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
data imputation
'''
import numpy as np
import operator


class Imputation(object):

    def __init__(self, patient_info, feature_len):
        self.feature_len = feature_len
        # patient dimension
        self.patient_info = patient_info
        self.patient_array, self.patient_time = self.get_array()
        self.patient_mask, self.patient_mask_idx = self.get_mask()


    def get_imputation(self, method='simple'):
        if method == 'simple':
            self.simple_imputation()
        # elif method == 'multiple': # can be extend to multiple imputation
        #     self.multiple_imputation()
        return (self.patient_array, self.patient_time)


    def simple_imputation(self):
        feat_median, pat_median = self.get_median()
        print ('The patient number is: ', len(self.patient_array))
        print ('The patient number with missing records: ', len(self.patient_mask_idx))
        for pat_id in self.patient_array:
            feat_array = self.patient_array[pat_id]
            if pat_id not in self.patient_mask_idx: # do not need imputation
                continue
            feat_mask_idx = self.patient_mask_idx[pat_id] # list of (row_idx, col_idx)

            for idx in range(len(feat_mask_idx[0])): # each position need imputation
                row_idx = feat_mask_idx[0][idx]
                col_idx = feat_mask_idx[1][idx]
                m, n = np.shape(feat_array)

                if int(feat_array[row_idx-1, col_idx]) != -1: # last occurrence carry forward strategy
                    feat_array[row_idx, col_idx] = feat_array[row_idx-1, col_idx]
                else:
                    if (row_idx < m-1) and int(feat_array[row_idx+1, col_idx]) != -1: # first occurrence carry backward strategy
                        feat_array[row_idx, col_idx] = feat_array[row_idx+1, col_idx]
                    else:
                        if int(pat_median[pat_id][col_idx]) != -1: # fill with patient median value
                            feat_array[row_idx, col_idx] = pat_median[pat_id][col_idx]
                        elif int(pat_median[pat_id][col_idx]) == -1: # fill with feature median value
                            feat_array[row_idx, col_idx] = feat_median[col_idx]
            self.patient_array[pat_id] = feat_array


    def get_array(self):
        patient_array = dict() # pat_id: feature value array
        patient_time = dict() # pat_id: record time list
        for pat_id in self.patient_info:
            patient_rec = self.patient_info[pat_id].patient_rec
            if len(patient_rec)==0:
                continue
            patient_rec = sorted(patient_rec.items(), key=operator.itemgetter(0))
            feat_array = [pr[1] for pr in patient_rec]
            patient_array[pat_id] = np.array(feat_array, dtype='float32')
            time_list = [pr[0] for pr in patient_rec]
            patient_time[pat_id] = np.array(time_list, dtype='int')
        return (patient_array, patient_time)


    def get_mask(self):
        patient_mask = dict() # 1 has value, 0 no value
        patient_mask_idx = dict() # missing values
        for pat_id in self.patient_array:
            feat_mask_idx = []
            feat_array = self.patient_array[pat_id]
            feat_mask_idx = np.where(feat_array == -1)
            idx_len = len(feat_mask_idx[0])
            if idx_len == 0:
                continue
            # store mask array for each patient, 1 has value, 0 no value
            shape = np.shape(feat_array)
            feat_mask = np.ones(shape, dtype='int')
            feat_mask[feat_mask_idx] = 0
            patient_mask[pat_id] = feat_array
            # store mask id (missing values) for each patient
            patient_mask_idx[pat_id] = feat_mask_idx
        return (patient_mask, patient_mask_idx)


    def get_median(self):
        # output: feat_median: an array of median value
        #         pat_median: a dict {pat id: {feature name: median value}}
        feat_median = np.zeros(self.feature_len)
        feat_value = dict()
        pat_median = dict() # pat_id: feature median
        for pat_id in self.patient_array:
            feat_array = self.patient_array[pat_id]
            pf_median = np.zeros(self.feature_len)-1
            for col in range(self.feature_len):
                # compute patient median feature value
                rows = np.where(feat_array[:, col]!=-1)
                rows = rows[0]
                if len(rows) == 0:
                    continue
#                print (feat_array[rows, col])
                pf_median[col] = np.round(np.median(feat_array[rows, col]))
#                print (numpy.round(numpy.median(feat_array[rows, col])))
                # store total feature value
                if col not in feat_value:
                    feat_value[col] = list()
                feat_value[col].extend(feat_array[rows, col])
#                print (feat_value[col])
            pat_median[pat_id] = pf_median

        # compute global meidan
        for col in feat_value.keys():
            feat_median[col] = np.round(np.median(feat_value[col]))
        return (feat_median, pat_median)
