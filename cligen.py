#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
sequential clinical data generation for dti data
'''
import numpy as np
import scipy.io as sio
import operator
from time_converter import convert_int

bad_mri_id = [523, 524, 639, 643, 647, 767]
delete_sid = [373] + bad_mri_id

class CliGen(object):

    def __init__(self, feature_list, feature_range, dti_time=None):
        if dti_time:
            self.dti_time = dti_time # pid, time, gid
            dti_subject_id = self.load_subject("dti_fact")
            self.id_map_ = dict(zip(dti_subject_id, range(len(dti_subject_id)))) # map to the index of pairs

        self.subject_array = dict()
        self.subject_label = dict()
        self.seq_length = dict()
        self.feature_list = feature_list
        self.feature_range = feature_range

    def load_subject(self, view):
        # print(view + '_subject_id.mat')
        sid = sio.loadmat(view + '_subject_id.mat')[view + '_subject_id'][0, :]
        subject_id = [i for i in sid if i not in delete_sid]
        return subject_id

    def get_data(self, patient_array, patient_time, time=None, dti=False):
        if None == time:
            self.subject_array = patient_array
        elif True == dti:
            # load dti subjects
            for dt in self.dti_time:
                pid = dt[0]
                time = dt[1]
                gid = dt[2]
                if pid not in patient_array or pid not in patient_time:
                    continue
                feat_array = patient_array[pid]
                feat_time = patient_time[pid]
                index = np.argmin(np.abs(feat_time - time))
                if gid not in self.id_map_:
                    continue
                self.subject_array[self.id_map_[gid]] = feat_array[:index+1,:]
                seq_len = self.subject_array[self.id_map_[gid]].shape[0]
                if seq_len not in self.seq_length:
                    self.seq_length[seq_len] = 0
                self.seq_length[seq_len] += 1
        else: # same end time point for all the patients
            time = convert_int(time)
            for pid, feat_array in patient_array.items():
                feat_time = patient_time[pid]
                index = np.argmin(np.abs(feat_time - time))
                self.subject_array[pid] = feat_array[:index+1,:]
                seq_len = self.subject_array[pid].shape[0]
                if seq_len not in self.seq_length:
                    self.seq_length[seq_len] = 0
                self.seq_length[seq_len] += 1
        return self.subject_array


    def get_label(self, patient_info, type, time=None, dti=False):
        if None == time:
            for pid in patient_info.keys():
                if type == 'hy':
                    patient_label = patient_info[pid].patient_hy
                elif type == 'mci':
                    patient_label = patient_info[pid].patient_mci
                if len(patient_label) == 0: # no labels for the patient
                    continue
                patient_label = sorted(patient_label.items(), key=operator.itemgetter(0))
                label_vector = np.array([pl[1] for pl in patient_label])
                label_time = np.array([pl[0] for pl in patient_label])
                self.subject_label[pid] = patient_label[-1][1]
        elif True == dti:
            for dt in self.dti_time:
                pid = dt[0]
                time = dt[1]
                gid = dt[2]
                if pid not in patient_info:
                    continue
                if type == 'hy':
                    patient_label = patient_info[pid].patient_hy
                elif type == 'mci':
                    patient_label = patient_info[pid].patient_mci

                if len(patient_label) == 0: # no labels for the patient
                    continue
                patient_label = sorted(patient_label.items(), key=operator.itemgetter(0))
                label_vector = np.array([pl[1] for pl in patient_label])
                label_time = np.array([pl[0] for pl in patient_label])
                index = np.argmin(np.abs(label_time - time))
                if gid not in self.id_map_:
                    continue
                self.subject_label[self.id_map_[gid]] = label_vector[index]
        else:
            time = convert_int(time)
            for pid in patient_info.keys():
                if type == 'hy':
                    patient_label = patient_info[pid].patient_hy
                elif type == 'mci':
                    patient_label = patient_info[pid].patient_mci
                if len(patient_label) == 0: # no labels for the patient
                    continue
                patient_label = sorted(patient_label.items(), key=operator.itemgetter(0))
                label_vector = np.array([pl[1] for pl in patient_label])
                label_time = np.array([pl[0] for pl in patient_label])
                index = np.argmin(np.abs(label_time - time))
                self.subject_label[pid] = label_vector[index]
        return self.subject_label

    def get_binarization(self):
        new_subject_array = dict()
        _f_map = dict()
        new_fidx = 0
        for sid, feat_array in self.subject_array.items():
            seq_len = feat_array.shape[0]
            fidx = 0
            for fname in self.feature_list:
                col_num = self.feature_range[fname]
                temp_array = np.zeros((seq_len, col_num), dtype=int)
                for s in range(seq_len):
                    fval = int(feat_array[s, fidx])
                    temp_array[s, fval] = 1
                if sid not in new_subject_array:
                    new_subject_array[sid] = temp_array
                else:
                    new_subject_array[sid] = np.concatenate((new_subject_array[sid], temp_array), axis=1)
                fidx += 1

        # comptue an index map for the old and new feature list
        new_fidx = 0
        for i, fname in enumerate(self.feature_list):
            col_num = self.feature_range[fname]
            for j in range(col_num):
                _f_map[new_fidx] = i
                new_fidx += 1

        # change the stored value as index of features, then the size should be (number of sequence x length of feature list)
        feat_len = len(self.feature_list)
        new_feat_len = new_subject_array[sid].shape[1]
        new_subject_idx_array = dict()
        for sid, feat_array in new_subject_array.items():
            seq_len = feat_array.shape[0]
            temp_array = np.zeros((seq_len, feat_len), dtype=int)
            for i in range(seq_len):
                for j in range(new_feat_len):
                    if feat_array[i, j] == 1:
                        if temp_array[i, _f_map[j]] != 0:
                            print ('Error!')
                        temp_array[i, _f_map[j]] = j
            new_subject_idx_array[sid] = temp_array

        self.subject_array = new_subject_idx_array
        return self.subject_array
