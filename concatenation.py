#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
data concatenation
'''
import numpy
import operator
from numeric import isfloat, isint
from time_converter import convert_int
from patient.patient import Patient


class Concatenation(object):

    def __init__(self, dataio, domain, dti=False):
        self.dataio = dataio
        self.domain = domain
        # patient dimension
        # get a dictionary with each item pat_id : Patient
        if dti:
            self.patient_time_id = dataio.patient_id
            self.patient_info = dict() # pat_id : Patient
            self.patient_id = [pid[0] for pid in self.patient_time_id]
            self.dti_time = self.patient_time_id # pid, time, gid
        else:
            self.patient_id = dataio.patient_id
            self.patient_info = dict() # pat_id : Patient
            self.dti_time = None

        for pid in self.patient_id:
            self.patient_info[pid] = Patient()

        # feature dimension
        self.feature_name = dataio.feature.feature_name
        self.feature_list = dataio.feature.feature_list
        self.feature_dict = dataio.feature.feature_dict
        self.feature_len = dataio.feature.feature_len
        self.feature_range = dataio.feature.feature_range


    def get_records(self, tpl_list):
        # store the patient info
        pat_record = dict() # patient id : a list of (time stamp, feature val)
        for tpl in tpl_list:
            # print (tpl)
            if isint(tpl[2])==True:
                fval = int(tpl[2])
            elif isfloat(tpl[2])==True:
                fval = float(tpl[2])
            else:
                continue
            pat_id = tpl[0]
            time = convert_int(tpl[1])
            if pat_id not in self.patient_id:
                continue

            if pat_id not in pat_record:
                pat_record[pat_id] = list()
                pat_record[pat_id].append((time, fval))
            else:
                pat_record[pat_id].append((time, fval))
        # print (fname)
        return pat_record

    def get_concatenation(self): # concat all the records without considering the dti time
        for fname in self.feature_list:

            # get triple lists (patient id, time, feature value)
            if self.domain == 'motor' and fname in self.feature_name[self.domain]:
                tpl_list = self.dataio.feature.motor.feature_info[fname]
            elif self.domain == 'nonmotor' and fname in self.feature_name[self.domain]:
                tpl_list = self.dataio.feature.nonmotor.feature_info[fname]
            elif self.domain == 'all' and fname in self.feature_name['motor']:
                tpl_list = self.dataio.feature.motor.feature_info[fname]
            elif self.domain == 'all' and fname in self.feature_name['nonmotor']:
                tpl_list = self.dataio.feature.nonmotor.feature_info[fname]
            # store the patient info
            pat_record = self.get_records(tpl_list)

            # store the records into Patient
            fidx = self.feature_dict[fname] # index of feature dimension
            for pat_id, tf_list in pat_record.items():
                patient = self.patient_info[pat_id]
                # feature array
                for time, fval in tf_list:
                    if time not in patient.patient_rec:
                        patient.patient_rec[time] = numpy.zeros(self.feature_len, dtype='float32')-1 # defualt value is -1
                    patient.patient_rec[time][fidx] = fval
                self.patient_info[pat_id] = patient

        # store the labels into Patient
        tf_list = self.dataio.label['hy']
        pat_record = self.get_records(tf_list)
        for pat_id, tf_list in pat_record.items():
            patient = self.patient_info[pat_id]
            # hy vector
            for time, fval in tf_list:
                patient.patient_hy[time] = fval
            self.patient_info[pat_id] = patient
        return (self.patient_info, self.feature_len, self.feature_list, self.feature_range)
