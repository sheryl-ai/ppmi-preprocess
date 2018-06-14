# -*- coding: utf-8 -*-

import csv, codecs

from feature.feature import Feature
from time_converter import convert_dti_time

class DataIO(object):

    def __init__(self, filepath, mappath, domain):
        self.filepath = filepath
        self.mappath = mappath
        self.domain = domain
        self.patient_id = list() # pat_id
        self.feature = Feature(filepath) # feature_info and other statistics
        self.label = {'hy':list(), 'mci':list()}

    def load_patient_id(self, dti=None):
        if None == dti:
            f = codecs.open(self.filepath + 'patient_id.csv', 'r', 'utf-8')
            reader = csv.reader(f)
            line_ctr = 0
            for row in reader:
                # table title
                if line_ctr < 1:
                    table_ttl = dict(zip(row, range(len(row))))
                    line_ctr += 1
                    continue

                pid = row[table_ttl['PATNO']]
                self.patient_id.append(pid)
                line_ctr += 1
            f.close()
        else:
            f = codecs.open(self.mappath + 'dti_time', 'r', 'utf-8')
            reader = csv.reader(f)
            line_ctr = 0
            for row in reader:
                # table title
                if line_ctr < 1:
                    table_ttl = dict(zip(row, range(len(row))))
                    line_ctr += 1
                    continue

                pid = row[table_ttl['subject_id']]
                time = row[table_ttl['time']]
                gid = row[table_ttl['subj_ID']]
                time = convert_dti_time(time)
                gid = int(gid)
                self.patient_id.append((pid, time, gid))
                line_ctr += 1
            f.close()

    def load_feature(self, ftype=None, fname=None, featname=None):
        self.feature.load_feature(ftype, fname, featname)

    def load_label(self, ftype=None, fname=None, featname=None):
        return self.feature.load_label(ftype, fname, featname)

    def read_data(self):
        self.load_patient_id()
        if self.domain == 'motor':
            self.load_feature('motor', 'MDS UPDRS PartII')
            self.load_feature('motor', 'MDS UPDRS PartIII')
        elif self.domain == 'nonmotor':
            self.load_feature('nonmotor', 'MDS UPDRS PartI')
            # self.load_feature('nonmotor', 'BJLO')
            # self.load_feature('nonmotor', 'LNS')
            self.load_feature('nonmotor', 'MoCA')
            # self.load_feature('nonmotor', 'QUIP')
            # self.load_feature('nonmotor', 'HVLT')
            # self.load_feature('nonmotor', 'ESS')
            # self.load_feature('nonmotor', 'GDS')
            # self.load_feature('nonmotor', 'RBD')
            # self.load_feature('nonmotor', 'STAI')
        elif self.domain == 'all':
            self.load_feature('motor', 'MDS UPDRS PartII')
            self.load_feature('motor', 'MDS UPDRS PartIII')
            self.load_feature('nonmotor', 'MDS UPDRS PartI')
            self.load_feature('nonmotor', 'MoCA')
        self.feature.get_feature_name(self.domain)
        # print (self.feature.feature_dict)

    def read_label(self):
        self.label['hy'] = self.load_label('motor', 'MDS UPDRS PartIII', 'hy')
